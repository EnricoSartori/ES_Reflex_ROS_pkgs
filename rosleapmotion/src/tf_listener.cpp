#include <ros/ros.h>
#include <stdio.h>
#include <iostream>
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <geometry_msgs/Vector3.h>
#include <string>
#include <reflex_msgs/HandCommand.h>

int main(int argc, char* argv[])
{
    ros::init(argc, argv, "hand_tf_listener");
    ros::NodeHandle nh;

    ros::Publisher reflex_commander_pub = nh.advertise<reflex_msgs::HandCommand>("reflex_commander", 1000);

    tf::TransformListener listener;
    tf::StampedTransform transform_f1;
    tf::StampedTransform transform_f2;
    tf::StampedTransform transform_f3;

    // To debug lookupTransform
    static tf::TransformBroadcaster br;
    tf::StampedTransform f1;
    tf::StampedTransform f2;
    tf::StampedTransform plane;

    ros::Rate rate(30.0);
    while (ros::ok()) {

        reflex_msgs::HandCommand msg;

        /**
            Nomi dei frame (tf) pubblicati da leap motion 
            che mi servono per ricavare gli angoli delle dita che mi interessano:
            
            - hand_ground                       (world)
            - right_hand                        (plane)
            - right_hand_index_intermediate     (finger_1)
            - right_hand_middle_intermediate    (finger_2)
            - right_hand_thumb_intermediate     (finger_3)
        */

        try{
            //listener.lookupTransform("/plane", "/world", ros::Time(0), plane);
            listener.lookupTransform("/right_hand_index_intermediate", "/right_hand", ros::Time(0), transform_f1);
            listener.lookupTransform("/right_hand_middle_intermediate", "/right_hand", ros::Time(0), transform_f2);
            listener.lookupTransform("/right_hand_thumb_intermediate", "/right_hand", ros::Time(0), transform_f3);
        } catch (tf::TransformException &ex) {
            ROS_ERROR("%s",ex.what());
            ros::Duration(1.0).sleep();
            continue;
        }

        /** 
        // Publish the transformation matrix to do visual debugging in rviz

        transform_f1.child_frame_id_ = "MYF1";
        transform_f2.child_frame_id_ = "MYF2";
        br.sendTransform(transform_f1);
        br.sendTransform(transform_f2);
        */
        
        // Per il pollice devo applicare una trasformazione statica
        //  in modo da orientare nel modo corretto il sistema di riferimento rispettivo
        tf::Matrix3x3 m(transform_f3.getRotation());
        double roll, pitch, yaw;
        m.getRPY(roll, pitch, yaw);

        tf::Quaternion tRotate;
        tRotate.setRPY(1.57, 0, -yaw);

        transform_f3.setRotation(transform_f3.getRotation() * tRotate);

        transform_f3.child_frame_id_ = "MY_THUMB";
        br.sendTransform(transform_f3);

        // getAngle() : restituisce la componente theta della rappresentazione asse angolo della rotazione

        double angle_0 = transform_f1.getRotation().getAngle();
        double angle_1 = transform_f2.getRotation().getAngle();
        double angle_2 = transform_f3.getRotation().getAngle();
        
        

        msg.angles[0] = angle_0;
        msg.angles[1] = angle_1;
        msg.angles[2] = angle_2;
        reflex_commander_pub.publish(msg); 

        //printf("0: %f - 1: %f - 2: %f\n", msg.angles[0], msg.angles[1], msg.angles[2]);

        ros::spinOnce();
        rate.sleep();
    }
}
