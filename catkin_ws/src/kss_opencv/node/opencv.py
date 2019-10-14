#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
writer = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))



class Gray():
    def __init__(self):
        self.selecting_sub_image = "raw" # you can choose image type "compressed", "raw"
 
        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/raspicam_node/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/darknet_ros/detection_image', Image, self.callback, queue_size=1)
 
        self.bridge = CvBridge()
 
    def callback(self, image_msg):

        if self.selecting_sub_image == "compressed":
            #converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
 
        cv2.imshow('cv_img', cv_image), cv2.waitKey(1)
        ret, img_color = cap.read()
        writer.write(img_color)
    def main(self):
        rospy.spin()
 
if __name__ == '__main__':
    rospy.init_node('gray')
    node = Gray()
    node.main()
    cap.release()
    writer.release()
    cv2.destroyAllWindows()


