import sys, rospy, math
from collections import deque

class MsgQueue:
	#params:
	#	delay: delay of the video in seconds
	def __init__(self, frame_per_second, delay, cb):
		self.frame_per_second = frame_per_second
		self.size = self.sizeWithDelay(delay)
		self.queue = deque(list(), self.size)
		self.callback = cb

	def push(self, data):
		if len(self.queue) == self.queue.maxlen:
			self.callback(self.queue[0])
		self.queue.append(data)

	def sizeWithDelay(self, delay):
		if float(delay) != float(0):
			return math.floor(float(delay) * self.frame_per_second)
		return 1

