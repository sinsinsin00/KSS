#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import rospy
import numpy as np
import threading
import sys, select, os, time
import face_recognition
import matplotlib

from std_msgs.msg import Int8, UInt8, Int32, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBoxes
from bebop_msgs.msg import Ardrone3PilotingStateAltitudeChanged
from bebop_msgs.msg import CommonCommonStateBatteryStateChanged
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

class mornitor:
    def __init__(self):
        rospy.init_node('mornitoring', anonymous=True)
        self.bebop_mode_sub = rospy.Subscriber('/bebop_mode', UInt8, self.callback_bebop_mode)
        self.bebop_status_sub = rospy.Subscriber('/bebop_status', Int32, self.callback_bebop_status, queue_size=5)
        self.bebop_odom_sub = rospy.Subscriber('/bebop/odom', Odometry, self.callback_bebop_odom, queue_size=5)
        self.bebop_altitude_sub = rospy.Subscriber('/bebop/states/ardrone3/PilotingState/AltitudeChanged',Ardrone3PilotingStateAltitudeChanged, self.callback_bebop_takeoff_stat,queue_size=1)
        self.bebop_battery_sub = rospy.Subscriber('/bebop/states/common/CommonState/BatteryStateChanged',CommonCommonStateBatteryStateChanged,self.callback_bebop_battery_stat,queue_size=1)
        self.dk_found_object_sub = rospy.Subscriber('/darknet_ros/found_object', Int8, self.callback_found_object)
        self.dk_bounding_sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet)

        self.isyn_person_to_drone_Alignment_sub = rospy.Subscriber('/person_to_drone_Alignment', String,self.callback_person_to_drone_Alignment)
        self.isyn_status_sub = rospy.Subscriber('/status_isyn', Int32, self.callback_isyn_status, queue_size=1)
        self.isyn_found_object_sub = rospy.Subscriber('/found_person', Int8, self.callback_found_person)
        self.isyn_save_image_clear_sub = rospy.Subscriber('/isyn_save_image_clear', Int8,self.callback_isyn_save_image_clear, queue_size=1)


        #init isyn
        self.curr_isyn_status_msg = 0
        self.curr_bebop_status_msg = 0
        self.found_person_msg = 0
        self.found_object = 0

        # init bebop
        self.curr_angular_speed = 0.1
        self.curr_isyn_status_msg = 0
        self.curr_Found_person = 0
        self.curr_Alignment = 0

        self.found_object_xy = 0
        self.split_Alignment_data = 'not data'
        self.curr_bebop_battery_stat = 'not data'


    def callback_bebop_mode(self,bebop_mode_data):
        self.curr_bebop_mode = bebop_mode_data.data

    def callback_bebop_status(self,bebop_status_data):
        self.curr_bebop_status_msg = bebop_status_data.data

    def callback_bebop_odom(self,bebop_odom_data):
        self.curr_bebop_odom_z = bebop_odom_data.pose.pose.orientation.z

    def callback_bebop_takeoff_stat(self,bebop_takeoff_stat_data):
        if bebop_takeoff_stat_data.altitude > 0:
            self.curr_bebop_takeoff_stat = 'take off'
        else:
            self.curr_bebop_takeoff_stat = 'land'

    def callback_bebop_battery_stat(self,bebop_bettery_stat_data):
        self.curr_bebop_battery_stat = bebop_bettery_stat_data.percent


    def callback_found_object(self,found_object_num_data):
        self.found_object = found_object_num_data.data

    def callback_darknet(self,found_object_xy_data):
        self.found_object_xy = found_object_xy_data

    def callback_person_to_drone_Alignment(self,Alignment_data):
        self.curr_Alignment = Alignment_data.data
        if self.curr_Alignment != 0 and self.curr_Alignment != 'not data':
            self.split_Alignment_data = self.curr_Alignment[1:-1]
            self.split_Alignment_data = map(int,self.split_Alignment_data.split(','))
        elif self.curr_Alignment == 'not data':
            self.split_Alignment_data = 'not data'

    def callback_bebop_req_save_image(self,bebop_req_save_image_data):
        self.curr_bebop_req_save_image = bebop_req_save_image_data

    def callback_isyn_status(self,isyn_status_data):
        self.curr_isyn_status_msg = isyn_status_data.data

    def callback_found_person(self,found_person_data):
        self.curr_found_person = found_person_data.data

    def callback_isyn_save_image_clear(self,isyn_save_image_clear):
        self.curr_isyn_save_image_clear = isyn_save_image_clear


    def monitoring_thread(self):
        while(1):
            try:
                print("#"*50)
                print('bebop_mode                   :       [{}] '.format(self.curr_bebop_mode))
                print('bebop_stat                   :       [{}] '.format(self.curr_bebop_status_msg))
                print('isyn_stat                    :       [{}] '.format(self.curr_isyn_status_msg))
                print('bebop_takeoff_stat           :       [{}] '.format(self.curr_bebop_takeoff_stat))
                print('bebop battery stat           :       [{}] '.format(self.curr_bebop_battery_stat))
                print('Alignment data               :       [{}] '.format(self.split_Alignment_data))

                #print("detect location :    [{}] ".format(self.found_object_xy.bounding_boxes))

                print("#" * 50)
                rospy.sleep(0.3)
                os.system('clear')
            except AttributeError:
                w = 'wait'
                print(w.center(50,' '))
                print("#" * 50)
                rospy.sleep(1)
                os.system('clear')


if __name__  == "__main__":
    try:
        mt = mornitor()
        mt_thread = threading.Thread(target=mt.monitoring_thread)
        mt_thread.daemon = True
        mt_thread.start()
        rospy.spin()

    except KeyboardInterrupt as e:
        print(e)
        print("good bye")