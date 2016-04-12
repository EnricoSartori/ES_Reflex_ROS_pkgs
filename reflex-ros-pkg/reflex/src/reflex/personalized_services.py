
import rospy

from std_srvs.srv import Empty

from reflex_base import ReFlex
from reflex_msgs.msg import Hand
from reflex_msgs.srv import CommandHand, MoveFinger, MovePreshape

class GraspFingertipsService:
    def __init__(self, obj):
        self.obj = obj
        self.locked = False

    def __call__(self, req):
        rospy.loginfo("reflex_base:GraspFingertipsService:")
        if self.locked:
            rospy.loginfo("\tService locked at the moment (in use), try later")
            return (0, -1)
        else:
            self.locked = True
            start_time = rospy.Time.now()
            # DO SOMETHING
            self.obj.command_smarts(*['solid_fingertips_contact'])
            #
            end_time = rospy.Time.now()
            self.locked = False
            # TODO: Use more in-depth return statements than 1 and 0
            #return (1, end_time - start_time)
            return []

