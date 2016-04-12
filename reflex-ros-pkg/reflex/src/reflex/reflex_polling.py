#!/usr/bin/env python

import rospy
from reflex_msgs.msg import HandCommand
from time import sleep

from reflex_base_services import *

K = 1.1785 # Costante moltiplicativa per mappare correttamente l'angolo comandato con il proximal della ReFlex

class ReFlex_Polling(ReFlex):

    def __init__(self):
        super(ReFlex_Polling, self).__init__()
        

        def callback(data):
            # data is a HandCommand variable
            # self.move_finger(0, data.angles[0]) # INDICE (DITO 0) DISABILITATO
    	    # self.move_finger(1, data.angles[1])
            # self.move_finger(2, data.angles[2])

            angle = data.angles[0] # * K
            if (angle > 3.14): 
                angle = 3.14
            self.move_finger(1, angle) # Mappo l'indice sul pollice della ReFlex


            
        rospy.Subscriber("reflex_commander", HandCommand, callback)
        # spin: this function generate the polling
        rospy.spin()

if __name__ == '__main__':
	rospy.init_node('ReflexPollingNode')
	reflex_hand = ReFlex_Polling()
