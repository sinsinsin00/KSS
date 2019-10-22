#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import rospy
import numpy as np
import sys, select, os
import tty, termios
import face_recognition


from std_msgs.msg import Int8
from turtlesim.msg import Pose
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBoxes


# color set
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
        self.msg = Twist()
        self.rate = rospy.Rate(5)
        self.box = BoundingBoxes()
        self.control_flag = 0
        # mode
        self.start_object_detect = 0

        # detect_face_init
        self.known_face_encodings = []
        self.known_face_names = []
        dirname = '/home/ksshin/knowns'
        files = os.listdir(dirname)
        for filename in files:
            self.name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(self.name)
                pathname = os.path.join(dirname, filename)
                print(pathname)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        # point center
        self.point_x_center = 320
        self.point_y_center = 240

        # height,width
        self.height = 480
        self.width = 640

        # circle center
        self.circle_x_center = self.width / 2
        self.circle_y_center = self.height / 2



    def callback_opencv(self, image_msg):
        if self.selecting_sub_image == "compressed":
            # converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        # set image height width
        #height, width, channels = cv_image.shape
        key = cv2.waitKey(1) & 0xFF
        # turtlebot control flag

        if key == ord("s"):
            self.start_object_detect = 1
        if key == ord("q"):
            self.start_object_detect = 0

        if self.start_object_detect == 1:
            found_object_max = self.found_object_num.data
            if found_object_max != 0 :
                for i in range(0,len(self.x_min),1):
                        # print information
                        # print("person detect number : ", i)
                        print("control_flag         : ", self.control_flag)

                        # set person detect bounding box middle
                        self.mid_x = (self.x_min[0] + self.x_max[0]) / 2
                        self.mid_y = (self.y_min[0] + self.y_max[0]) / 2

                        # turtle control stop
                        if key == ord("0"):
                            self.control_flag = 0
                            self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
                            self.pub.publish(self.msg)
                        # turtle control start
                        if key == ord("1"):
                            self.control_flag = 1
                            self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
                            self.pub.publish(self.msg)

                        # Resize frame of video to 1/4 size for faster face recognition processing
                        small_frame = cv2.resize(cv_image, (0, 0), fx=0.5, fy=0.5)
                        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                        rgb_small_frame = small_frame[:, :, ::-1]

                        # Only process every other frame of video to save time
                        if self.process_this_frame:
                            # Find all the faces and face encodings in the current frame of video
                            self.face_locations = face_recognition.face_locations(rgb_small_frame)
                            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                            self.face_names = []
                            for face_encoding in self.face_encodings:
                                # See if the face is a match for the known face(s)
                                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                                min_value = min(distances)

                                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                                # 0.6 is typical best performance.
                                self.name = "Unknown"
                                if min_value < 0.6:
                                    index = np.argmin(distances)
                                    self.name = self.known_face_names[index]

                                self.face_names.append(self.name)

                        self.process_this_frame = not self.process_this_frame

                        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                            top *= 2
                            right *= 2
                            bottom *= 2
                            left *= 2

                            # Draw a box around the face
                            cv2.rectangle(cv_image, (left, top), (right, bottom), (0, 0, 255), 1)
                            # Draw a label with a name below the face
                            cv2.rectangle(cv_image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(cv_image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


                        #text detect image name
                        cv2.putText(cv_image, 'person', (int(self.mid_x)- 40, int(self.mid_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        # draw rectangle
                        cv_image = cv2.rectangle(cv_image, (self.x_min[0], self.y_min[0]), (self.x_max[0], self.y_max[0]),red_color, 2)
                        #draw circle
                        cv_image = cv2.circle(cv_image,(self.circle_x_center,self.circle_y_center),10,white_color,1)
                        #draw point
                        cv_image = cv2.line(cv_image, (self.point_x_center, self.point_y_center), (self.point_x_center, self.point_y_center), red_color, 5)

                        #control detect object following
                        if self.control_flag == 1:
                            detect_object_mid = self.mid_x - self.point_x_center
                            tresh_linear_max = 20
                            tresh_linear_min = -20
                            angular_speed = 0.05

                            print("detect_object_mid    : ", detect_object_mid)

                            if detect_object_mid < tresh_linear_max and detect_object_mid > tresh_linear_min:
                                self.msg.angular.z = self.msg.angular.x = self.msg.angular.y = 0
                                '''if self.name == "Unknown":
                                    dirname = '/home/ksshin/knowns/'
                                    files = os.listdir(dirname)
                                    file_num = len(files)
                                    cv_image_capture = cv_image
                                    cv2.imwrite('/home/ksshin/image/img{}.jpg'.format(file_num),cv_image_capture,params=[cv2.IMWRITE_PNG_COMPRESSION,0])'''

                            elif detect_object_mid > tresh_linear_max:
                                self.msg.angular.z = -angular_speed
                                self.msg.angular.x = self.msg.angular.y = 0
                            elif detect_object_mid < tresh_linear_min:
                                self.msg.angular.z = angular_speed
                                self.msg.angular.x = self.msg.angular.y = 0
                            self.pub.publish(self.msg)



        # show display
        cv2.imshow("opencv", cv_image)
        
    def callback_darknet(self,found_object_xy):
        self.x_min = []
        self.y_min = []
        self.x_max = []
        self.y_max = []

        for i in range(0,len(found_object_xy.bounding_boxes),1):
            self.x_min.append(found_object_xy.bounding_boxes[i].xmin)
            self.y_min.append(found_object_xy.bounding_boxes[i].ymin)
            self.x_max.append(found_object_xy.bounding_boxes[i].xmax)
            self.y_max.append(found_object_xy.bounding_boxes[i].ymax)

    def callback_found_object(self,found_object_num_data):
        self.found_object_num = found_object_num_data

    def sub_bounding_box(self):
        self.sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet,queue_size = 10)

    def sub_opencv_img(self):
        self.sub = rospy.Subscriber('/raspicam_node/image_raw', Image, self.callback_opencv, queue_size = 10)

    def sub_found_object(self):
        self.sub = rospy.Subscriber('/darknet_ros/found_object', Int8, self.callback_found_object,queue_size = 10)

    def pub_control_turtlebot(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    try:
        x = darknet()
        x.sub_opencv_img()
        x.sub_found_object()
        x.sub_bounding_box()
        x.pub_control_turtlebot()
        rospy.spin()


    except KeyboardInterrupt :
        print("main program exit")


    except rospy.ROSInterruptException as e:
        print("ROS program exit")

