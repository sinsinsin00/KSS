#!/usr/bin/env python

import cv2
import rospy
import numpy as np
import sys, select, os
import tty, termios

from std_msgs.msg import Int8
from turtlesim.msg import Pose
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBoxes


#color set
blue_color = (255,0,0)
green_color = (0,255,0)
red_color = (0,0,255)
white_color = (255,255,255)
black_color = (0,0,0)



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

class darknet:
    def __init__(self):
        rospy.init_node('detect_tracking', anonymous=True)
        self.selecting_sub_image = "raw"  # you can choose image type "compressed", "raw"
        self.bridge = CvBridge()
        self.msg = Twist()
        self.rate = rospy.Rate(5)
        self.box = BoundingBoxes()
        self.control_flag = 0


    def callback_darknet(self,data):
        self.x_min = []
        self.y_min = []
        self.x_max = []
        self.y_max = []

        for i in range(0,len(data.bounding_boxes),1):
            if data.bounding_boxes[i].Class == 'person':
                self.x_min.append(data.bounding_boxes[i].xmin)
                self.y_min.append(data.bounding_boxes[i].ymin)
                self.x_max.append(data.bounding_boxes[i].xmax)
                self.y_max.append(data.bounding_boxes[i].ymax)

    def callback_opencv(self, image_msg):
        if self.selecting_sub_image == "compressed":
            # converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        # set image height width
        height, width, channels = cv_image.shape

        # point center
        self.point_x_center = 320
        self.point_y_center = 240

        # circle center
        self.circle_x_center = width / 2
        self.circle_y_center = height / 2

        # turtlebot control flag
        key = getKey()
        if key == 'q':
            self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
            self.control_flag = 0

        if key == 'f':
            self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
            self.control_flag = 1


        found_object_max = self.found_object.data
        if found_object_max != 0:
            for i in range(0,len(self.x_min),1):
                try :
                    person_num = i
                    '''
                    print("only person {}".format(i))
                    print(self.x_min[i])
                    print(self.y_min[i])
                    print(self.x_max[i])
                    print(self.y_max[i])
                    print("mid values")
                    print(self.mid_x)
                    print(self.mid_y)
                    print(self.circle_y_center)
                    print(self.circle_x_center)
                    print(self.point_x_center)
                    '''
                    

                    self.mid_x = (self.x_min[0] + self.x_max[0]) / 2
                    self.mid_y = (self.y_min[0] + self.y_max[0]) / 2

                    #text detect image name
                    cv2.putText(cv_image, 'person', (int(self.mid_x)- 40, int(self.mid_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    #draw circle
                    cv_image = cv2.circle(cv_image,(self.circle_x_center,self.circle_y_center),10,white_color,1)
                    #draw point
                    cv_image = cv2.line(cv_image, (self.point_x_center, self.point_y_center), (self.point_x_center, self.point_y_center), red_color, 5)
                    #draw rectangle
                    cv_image = cv2.rectangle(cv_image,(self.x_min[0],self.y_min[0]),(self.x_max[0],self.y_max[0]),red_color,2)


                    #control detect object following
                    if person_num == 0:
                        detect_object_mid = self.mid_x - self.point_x_center
                        tresh_linear_max = 50
                        tresh_linear_min = -50
                        angular_speed = 0.05

                        print("detect_object_mid : ",detect_object_mid)
                        print("control_flag : ",self.control_flag)

                        if self.control_flag == 1:
                            if detect_object_mid < tresh_linear_max and detect_object_mid > tresh_linear_min:
                                self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
                            elif detect_object_mid > tresh_linear_max:
                                self.msg.angular.z = -angular_speed
                                self.msg.angular.x = self.msg.angular.y = 0
                            elif detect_object_mid < tresh_linear_min:
                                self.msg.angular.z = angular_speed
                                self.msg.angular.x = self.msg.angular.y = 0

                        self.pub.publish(self.msg)
                        self.rate.sleep()


                except IndexError as e :
                    print(e)
        # show display
        cv2.imshow("opencv", cv_image)
        # cv2.imshow('opencv', cv2.resize(cv_image, (800, 450)))
        cv2.waitKey(3)

    def callback_found_object(self,data):
        self.found_object = data

    def sub_bounding_box(self):
        self.sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet)

    def sub_opencv_img(self):
        self.sub = rospy.Subscriber('/raspicam_node/image_raw', Image, self.callback_opencv)

    def sub_found_object(self):
        self.sub = rospy.Subscriber('/darknet_ros/found_object', Int8, self.callback_found_object)

    def pub_control_turtlebot(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    try:
        x = darknet()
        x.sub_found_object()
        x.sub_opencv_img()
        x.sub_bounding_box()
        x.pub_control_turtlebot()
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting Down")
        cv2.destroyAllWindows()


    except KeyboardInterrupt :
        print("main program exit")


    except rospy.ROSInterruptException as e:
        print("ROS program exit")

