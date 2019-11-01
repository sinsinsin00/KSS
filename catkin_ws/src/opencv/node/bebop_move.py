#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import rospy, os, time, sys, termios, select, atexit, math

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty, Bool, UInt8, Int32
from bebop_msgs.msg import Ardrone3PilotingStateAltitudeChanged


if os.name == 'nt':
  import msvcrt
else:
  import tty, termios


class Bebop:
    def __init__(self):
        rospy.init_node('bebop_move', anonymous=True)

        # bebop info
        self.odom_sub = rospy.Subscriber('/bebop/odom', Odometry, self.callback_bebop_odom, queue_size=5)
        self.altitude_sub = rospy.Subscriber('/bebop/states/ardrone3/PilotingState/AltitudeChanged',Ardrone3PilotingStateAltitudeChanged,self.callback_bebop_takeoff_stat,queue_size = 10)

        # communication with isyn
        self.person_to_drone_Alignment_sub = rospy.Subscriber('/person_to_drone_Alignment', Int32,
                                                              self.callback_person_to_drone_Alignment)
        self.isyn_status_sub = rospy.Subscriber('/status_isyn', Int32,self.callback_isyn_status, queue_size=10)
        self.found_object_sub = rospy.Subscriber('/found_person', Bool, self.callback_found_person)

        self.bebop_mode_pub = rospy.Publisher('/bebop_mode', UInt8,queue_size=5)
        self.bebop_status_pub = rospy.Publisher('bebop_status',Int32,queue_size = 10)

        # bebop control
        self.pub_land = rospy.Publisher('/bebop/land', Empty, queue_size=1)
        self.pub_takeoff = rospy.Publisher('/bebop/takeoff', Empty, queue_size=1)
        self.bebop_control_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=5)

        # init
        self.empty_msg = Empty()
        self.msg = Twist()
        self.thresh_Alignment_max = 30
        self.thresh_Alignment_min = -30
        self.error_check_num = 0

        # init bebop
        self.bebop_speed = 0
        self.angular_speed = 0.05
        self.set_Alignment_flag = 0
        self.curr_isyn_status = 0
        self.point_local_scan_clear = 0
        self.curr_Found_person = 0
        self.check_isyn_dis = 0

        # pub msgs
        self.bebop_mode_msg = 0
        self.curr_bebop_status_msg = 0

    def take_off(self):
        rospy.sleep(1)
        self.pub_takeoff.publish(self.empty_msg)
        print("bebop_will_take_off")

    def land(self):
        rospy.sleep(1)
        self.pub_land.publish(self.empty_msg)
        print("bebop_is_landing")

    def callback_bebop_odom(self,bebop_odom_data):
        self.curr_bebop_odom_z = bebop_odom_data.pose.pose.orientation.z

    def callback_person_to_drone_Alignment(self,Alignment_data):
        self.curr_Alignment = Alignment_data.data

    def callback_found_person(self,found_person_data):
        self.curr_Found_person = found_person_data

    def callback_bebop_takeoff_stat(self,bebop_takeoff_stat_data):
        self.curr_bebop_takeoff_stat = bebop_takeoff_stat_data

    def callback_isyn_status(self,isyn_status_data):
        self.curr_isyn_status = isyn_status_data

    # thread func
    def bebop_move(self):
        while(1):
            time.sleep(0.1)
            #send msg of bebop status
            if self.curr_bebop_takeoff_stat.altitude == 0:
                self.curr_bebop_status_msg = 0
            elif self.curr_bebop_takeoff_stat.altitude > 0 and self.curr_isyn_status == 0:
                self.curr_bebop_status_msg = 1
                self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                self.bebop_control_pub.publish(self.msg)
            elif self.curr_bebop_takeoff_stat.altitude > 0 and self.curr_isyn_status == 2:
                self.curr_bebop_status_msg = 2
            elif self.curr_bebop_takeoff_stat.altitude > 0 and self.curr_isyn_status == 3:
                self.curr_bebop_status_msg = 3

            # send msg of isyn status
            self.bebop_mode_pub.publish(self.bebop_mode_msg)
            self.bebop_status_pub.publish(self.curr_bebop_status_msg)


            if self.curr_bebop_status_msg == 2 and self.point_local_scan_clear == 0:
                limit_orientation_z = self.curr_bebop_odom_z
                while(self.curr_bebop_odom_z > 0) :
                    self.msg.angular.z = self.angular_speed
                    self.bebop_control_pub.publish(self.msg)

                    if self.curr_Found_person == True:
                        self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                        self.bebop_control_pub.publish(self.msg)
                        self.point_local_scan_clear = 1
                        self.curr_bebop_status_msg = 3
                        break
                    rospy.sleep(0.033)

                while(self.curr_bebop_odom_z < 0) :
                    self.msg.angular.z = self.angular_speed
                    self.bebop_control_pub.publish(self.msg)

                    if self.curr_Found_person == True:
                        self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                        self.bebop_control_pub.publish(self.msg)
                        self.point_local_scan_clear = 1
                        self.curr_bebop_status_msg = 3
                        break
                    rospy.sleep(0.033)


                self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                self.bebop_control_pub.publish(self.msg)
                self.point_local_scan_clear = 1


            try:
                print(self.curr_Alignment)
            except AttributeError:
                self.error_check_num =  self.error_check_num + 1
                if self.error_check_num >= 50:
                    print("wait Alignment data")
                    self.error_check_num = 0

            if self.curr_bebop_status_msg == 3 and self.curr_isyn_status == 3:
                while (self.set_Alignment_flag == 1):
                    if (self.curr_Alignment < self.thresh_Alignment_max and self.curr_Alignment > self.thresh_Alignment_min):
                        self.msg.angular.x = self.msg.angular.y = self.msg.angular.z = 0
                    elif(self.curr_Alignment < self.thresh_Alignment_max):
                        self.msg.angular.z = self.angular_speed
                        self.msg.angular.x = self.msg.angular.y = 0
                    elif(self.curr_Alignment > self.thresh_Alignment_min):
                        self.msg.angular.z = - self.angular_speed
                        self.msg.angular.x = self.msg.angular.y = 0

                    self.bebop_control_pub.publish(self.msg)
                    rospy.sleep(0.05)
            '''
            # display isyn_status
            self.check_isyn_dis += 1
            if self.check_isyn_dis == 10:
                if self.curr_isyn_status == 1:
                    print('isyn is up')
                elif self.curr_isyn_status == 2:
                    print('detect person change bebop tracking mode')
                    self.set_Alignment_flag = 1'''



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
    while (1):
        key = getKey()
        if key == 't':
            print("thread take off call")
            bebop.take_off()
        elif key == 'q':
            print("thread landing call")
            bebop.land()
            break
        elif key == 'a':
            print('change bebop stop detecting mode num 0  ')
            bebop.bebop_mode_msg = 0
        elif key == 's':
            print('change bebop detecting mode num 2')
            bebop.bebop_mode_msg = 2
        elif key == 'd':
            print('change bebop detecting mode num 3')
            bebop.bebop_mode_msg = 3


        time.sleep(0.1)

if __name__ == "__main__":
    try:
        if os.name != 'nt':
            settings = termios.tcgetattr(sys.stdin)
        bebop = Bebop()
        key_thread = threading.Thread(target=key_control)
        key_thread.daemon = True
        key_thread.start()
        bebop_move_thread = threading.Thread(target=bebop.bebop_move)
        bebop_move_thread.daemon = True
        bebop_move_thread.start()
        rospy.spin()

    except KeyboardInterrupt :
        print("main program exit")

    except rospy.ROSInterruptException as e:
        print("ROS program exit")




