#!/usr/bin/env python

import cv2
import rospy
import numpy as np

from turtlesim.msg import Pose
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBoxes
from darknet_ros_msgs.msg import found_object
#color set
blue_color = (255,0,0)
green_color = (0,255,0)
red_color = (0,0,255)
white_color = (255,255,255)
black_color = (0,0,0)


class darknet:
    def __init__(self):
        rospy.init_node('detect_tracking', anonymous=True)
        self.selecting_sub_image = "raw"  # you can choose image type "compressed", "raw"
        self.bridge = CvBridge()

        self.rate = rospy.Rate(10)
        self.box = BoundingBoxes()


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
        print(len(self.x_min))
        if len(self.x_min) != 0:
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


                    if person_num == 0:
                        if self.point_x_center == self.mid_x:
                            print("mid_X : ", self.mid_x, "dis_x_center : ", self.point_x_center)

                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break

                except IndexError as e :
                    print(e)

        # show display
        cv2.imshow('window', cv2.resize(cv_image, (800, 450)))

    def callback_found_object(self,found_object_data):
        print(found_object_data)


    def sub_bounding_box(self):
        self.sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet)

    def sub_opencv_img(self):
        self.sub = rospy.Subscriber('/image_raw', Image, self.callback_opencv, queue_size=1)

    def sub_found_object(self):
        self.sub = rospy.Subscriber('/found_object', found_object, self.callback_found_object, queue_size=1)


if __name__ == '__main__':
    try:
        x = darknet()
        x.sub_opencv_img()
        x.sub_bounding_box()
        rospy.spin()

    except KeyboardInterrupt :
        print("main program exit")

    except rospy.ROSInterruptException as e:
        print("ROS program exit")

