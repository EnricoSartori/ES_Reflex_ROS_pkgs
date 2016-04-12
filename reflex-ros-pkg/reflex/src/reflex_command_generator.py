#!/usr/bin/env python

import rospy
import sys, tty, termios
from reflex_msgs.msg import HandCommand
from time import sleep

hand_cmd = HandCommand()
hand_cmd.angles = [0,0,0]


def read_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

if __name__ == '__main__':
	rospy.init_node('ReflexComSenderNode')
	pub = rospy.Publisher('reflex_commander', HandCommand, queue_size=10)

	r = rospy.Rate(10)
	while not rospy.is_shutdown():
		ch = read_char()

		if (ch == '+' and hand_cmd.angles[0] < 3.14):
			hand_cmd.angles[0] = round(hand_cmd.angles[0] + 0.05, 2)
		elif (ch == '-' and hand_cmd.angles[0] > 0):
			hand_cmd.angles[0] = round(hand_cmd.angles[0] - 0.05, 2)
		elif (ch == 'q'):
			exit()
		
		pub.publish(hand_cmd)
		print(hand_cmd.angles)

        r.sleep()
