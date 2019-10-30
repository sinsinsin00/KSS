#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty, Bool, UInt8, Int32
import rospy, os, time, sys, termios, select, atexit, math
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios


class Bebop:
    def __init__(self):
        rospy.init_node('bebop_move', anonymous=True)

        self.found_object_sub = rospy.Subscriber('/found_person', Bool, self.callback_found_person)
        self.person_to_drone_Alignment_sub = rospy.Subscriber('/person_to_drone_Alignment', Int32, self.callback_person_to_drone_Alignment)


        self.bebop_mode_pub = rospy.Subscriber('/bebop_mode', UInt8)
        self.pub_land = rospy.Publisher('/bebop/land', Empty, queue_size=1)
        self.pub_takeoff = rospy.Publisher('/bebop/takeoff', Empty, queue_size=1)
        self.bebop_control_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=5)

        self.empty_msg = Empty()
        self.bebop_speed = 0
        self.msg = Twist()
        self.bebop_init_status = 0
        self.thresh_Alignment_max = 30
        self.thresh_Alignment_min = -30
        self.angular_speed = 0.05


    def callback_bebop_move(self,bebop_curr_speed_data):
        self.bebop_linear_x_speed = bebop_curr_speed_data.twist.twist.linear.x

        # print(self.bebop_linear_x_speed)


        if self.bebop_init_status == 0:
            self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
            self.bebop_init_status = 1

        set_Alignment_flag = 0
        while (set_Alignment_flag == 0):

            if (self.curr_Alignment < self.thresh_Alignment_max and self.curr_Alignment > self.thresh_Alignment_min):
                self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                set_Alignment_flag = 1
            elif(self.curr_Alignment < self.thresh_Alignment_max):
                self.msg.angular.z = self.angular_speed
                self.msg.angular.x = self.msg.angular.y = 0
            elif(self.curr_Alignment > self.thresh_Alignment_min):
                self.msg.angular.z = - self.angular_speed
                self.msg.angular.x = self.msg.angular.y = 0

            self.bebop_control_pub.publish(self.msg)


    def take_off(self):
        rospy.sleep(1)
        self.pub_takeoff.publish(self.empty_msg)
        print("bebop_will_take_off")

    def land(self):
        rospy.sleep(1)
        self.pub_land.publish(self.empty_msg)
        print("bebop_is_landing")

    def sub_odom(self):
        self.speed = rospy.Subscriber('/bebop/odom', Twist, self.callback_bebop_move)

    def callback_person_to_drone_Alignment(self,Alignment_data):
        self.curr_Alignment = Alignment_data

    def callback_found_person(self,found_person_data):
        self.curr_Found_person = found_person_data


def getKey():
    if os.name == 'nt':
      return msvcrt.getch()
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def key_control():
    print("thread in")
    while (1):
        key = getKey()
        if key == 't':
            print("thread take off call")
            bebop.take_off()
        elif key == 'q':
            print("thread landing call")
            bebop.land()
            break
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        if os.name != 'nt':
            settings = termios.tcgetattr(sys.stdin)
        bebop = Bebop()
        print("init complete")
        threading1 = threading.Thread(target=key_control)
        threading1.daemon = True
        threading1.start()
        print("thread start")
        rospy.spin()





    except KeyboardInterrupt :
        print("main program exit")

    except rospy.ROSInterruptException as e:
        print("ROS program exit")




