#!/usr/bin/env python

import rospy
from darknet_ros_msgs.msg import BoundingBoxes
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class darknet:
    def __init__(self):
        rospy.init_node('detect_tracking', anonymous=True)
        self.selecting_sub_image = "raw"  # you can choose image type "compressed", "raw"
        self.bridge = CvBridge()

        self.rate = rospy.Rate(10)
        self.box = BoundingBoxes()


    def callback_darknet(self,data):
        num = 0
        for i in range(0,len(data.bounding_boxes),1):
            if data.bounding_boxes[i].Class == 'person':
                self.x_min = data.bounding_boxes[i].xmin
                self.y_min = data.bounding_boxes[i].ymin
                self.x_max = data.bounding_boxes[i].xmax
                self.y_max = data.bounding_boxes[i].ymax

    def sub_bounding_box(self):
        self.sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet)


    def callback_opencv(self, image_msg):
        if self.selecting_sub_image == "compressed":
            # converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        for i in range(0,len(self.xmin),1):
            print("only person")
            print(self.xmin[i])
            print(self.ymin[i])
            print(self.xmax[i])
            print(self.ymax[i])

        cv2.imshow('cv_img', cv_image), cv2.waitKey(1)

    def sub_opencv_img(self):
        self._sub = rospy.Subscriber('raspicam_node/image_raw', Image, self.callback_opencv, queue_size=1)


if __name__ == '__main__':
    try:
        x = darknet()
        x.sub_bounding_box()
        x.sub_opencv_img()
        rospy.spin()

    except KeyboardInterrupt :
        print ("main program exit")

    except rospy.ROSInterruptException as e:
        print ("ROS program exit")

