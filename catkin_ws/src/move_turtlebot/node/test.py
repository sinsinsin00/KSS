#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move(msg):
	# declair Twist type object name 'msg'
	print(msg.transforms[0].transform.rotation.z)

	#print self.msg.angular.z


if __name__ == '__main__':
    try:
		rospy.init_node('test_print', anonymous=True)
		msg = Twist()
		# declair publisher name:pub, topic:'/turtle1/cmd_vel', type:Twist
		sub = rospy.Subscriber('/tf', Twist, move)
		rospy.spin()
        #move()
    except rospy.ROSInterruptException: pass
