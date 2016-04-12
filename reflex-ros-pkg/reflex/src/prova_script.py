#!/usr/bin/env python

import rospy
import serial
from std_msgs.msg import String
from reflex_msgs.msg import Hand
import time

def callback(hand):
	# hand contiene tutti i dati inviati al topic /reflex_hand dalla mano
	# vogliamo estrarre i dati relativi alle pressioni e pubblicarli tramite topic ad arduino
	# i valori da passati non hanno bisogno di ulteriori calcoli da parte di arduino
    
    # Posso passare i dati ad arduino in due modi:
    # 1 - Scrivendo dati semplici su su un topic e facendoli scrivere da rosserial

    #pub.publish(values_to_token(phalanx_values(hand)))

    # 2 - Scrivendo i dati direttamente sulla seriale

    print 'ciao'

 



def values_to_token(values):
    token = 'B '
    for i in values:
        #token += str(int(i)) 
        token += '{:03}'.format(int(i))
        token += ' '
    token += 'E'
    return token

def phalanx_values(hand):
    result = [0,0,0,0,0,0]
    for i in range(0,3):
        # i-esimo dito
        finger = hand.finger[i].pressure
        result[i*2] = abs(mymin(finger[:5]))
        result[i*2+1] = abs(mymin(finger[5:9]))
    return result

def mymin(list):
    ret = 0
    for i in list:
        if i > 100 or i < -255: 
            return -255
    return min(list)

def openSerial(port=None, baud=57600):
    try:
        global serialport 
        serialport = serial.Serial(port, baud, timeout=2.5)
        serialport.timeout = 0.01
    except SerialException as e:
        rospy.logerr("Error opening serial: %s", e)
        rospy.signal_shutdown("Error opening serial: %s" % e)
        raise SystemExit   

if __name__ == '__main__':

    serialport = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    while 1:
        serialport.write('B 255 255 255 255 255 255 E\n')
    serialport.close()

    #try:
    # openSerial('/dev/ttyACM0')
    # if serialport._isOpen:
    #     while 1:
    #         try:
    #             serialport.flushInput()
    #             serialport.write("B 255 255 255 255 255 255 E")
    #         except SerialException as e:
    #             rospy.logerr("Error writing on serial: %s", e)
    #     rospy.init_node('handListener')
    #     rospy.Rate(10)
    #     pub = rospy.Publisher('/hand_to_arduino', String, queue_size=10)
    #     rospy.Subscriber('/reflex_hand', Hand, callback)
        
    #     while not rospy.is_shutdown():
    #         rospy.spin()

     # except rospy.ROSInterruptException:
     #     pass