#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot:

    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.rate = rospy.Rate(10)
        self.pose = Pose()
        self.msg  = Twist()

    def check_msgs_callbf(self,data):

        print data.pose.pose.position.x
        print data.pose.pose.position.y
        print data.twist.twist.linear.x
        print data.twist.twist.linear.y

        print data.twist.twist.angular.x
        print data.twist.twist.angular.y
        rospy.sleep(0.01)


    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def input_msgs_callbf(self):
        pass

    def main_func(self):

        self.sub = rospy.Subscriber('/odom', Odometry, self.check_msgs_callbf)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        end_point_x = data.pose.pose.position.x + self.goal_pose.x
        end_point_y = data.pose.pose.position.y + self.goal_pose.y

        self.goal_pose.x = input("input x : ")
        self.goal_pose.y = input("input y : ")

        distance_tolerance = input("Set your tolerance: ")

        while True:
            self.msg.linear.x = self.linear_vel(self.goal_pose)
            self.msg.linear.y = self.msg.linear.z = 0
            # Angular velocity in the z-axis.
            self.msg.angular.z = self.angular_vel(self.goal_pose)
            self.msg.angular.x = self.msg.angular.y = 0

            self.pub.publish(self.msg)
            self.rate.sleep()

            if data.pose.pose.position.x <= end_point_x and data.pose.pose.position.y <= end_point_y:
                self.msg.linear.x = self.msg.linear.x = 0
                self.msg.linear.y = self.msg.linear.z = 0
                # Angular velocity in the z-axis.
                self.msg.angular.z = self.msg.angular.x = 0
                self.msg.angular.x = self.msg.angular.y = 0
                self.pub.publish(self.msg)

                break
        rospy.sleep(1)
        rospy.spin()


if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.main_func()

    except KeyboardInterrupt :
        print "main program exit"

    except rospy.ROSInterruptException as e:
        print "ROS program exit"

