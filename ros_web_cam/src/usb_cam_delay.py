#!/usr/bin/env python

import sys, rospy, math
from collections import deque
from sensor_msgs.msg import Image

FRAME_PER_SECOND = 25

class ImageQueue:
	#params:
	#	delay: delay of the video in seconds
	def __init__(self, delay, cb):
		self.size = sizeWithDelay(delay)
		self.queue = deque(list(), self.size)
		self.callback = cb

	def push(self, data):
		if len(self.queue) == self.queue.maxlen:
			self.callback(self.queue[0])
		self.queue.append(data)

	# usb_cam node publish 25 msg per second in /usb_cam/image_raw
	
def sizeWithDelay(delay):
	if delay != 0:
		return math.floor((float)(delay) * FRAME_PER_SECOND)
	return 1

def image_received_cb(image):
	global imageQueue
	imageQueue.push(image)

def send_image_cb(image):
	# TODO: pubblico nel topic l'immagine
	pub.publish(image)

def main(argv):
	global imageQueue, pub
	delay = 0
	if len(argv) > 0:
		delay = argv[0]
	rospy.init_node('usb_cam_tester')
	pub = rospy.Publisher('/image_raw_with_delay', Image, queue_size=10)
	imageQueue = ImageQueue(delay, send_image_cb)
	rospy.Subscriber('/usb_cam/image_raw', Image, image_received_cb)
	rospy.spin()
	

if __name__ == "__main__":
	main(sys.argv[1:])