#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import rospy
import numpy as np
import threading
import os, time
import face_recognition

from std_msgs.msg import Int8, UInt8, Int32, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBoxes

# color set
blue_color  = (255,0,0)
green_color = (0,255,0)
red_color   = (0,0,255)
black_color = (0,0,0)
white_color = (255,255,255)


class isyn:
    def __init__(self):
        print("init start")
        rospy.init_node('detect_tracking', anonymous=True)

        #bebop info
        #sub
        #self.opencv_img_sub = rospy.Subscriber('/image_raw', Image, self.callback_opencv)
        self.opencv_img_sub = rospy.Subscriber('/bebop/image_raw', Image, self.callback_opencv)

        #with bebop
        #sub
        self.bebop_mode_sub = rospy.Subscriber('/bebop_mode', UInt8, self.callback_bebop_mode)
        self.bebop_status_sub = rospy.Subscriber('/bebop_status', Int32,self.callback_bebop_status, queue_size=5)
        self.bebop_req_save_image_sub = rospy.Subscriber('/bebop_req_save_image',Int8,self.callback_bebop_req_save_image, queue_size=5)
        #pub
        self.person_to_drone_Alignment_pub = rospy.Publisher('/person_to_drone_Alignment', String, queue_size=5)
        self.isyn_status_pub = rospy.Publisher('/status_isyn', Int32, queue_size=1)
        self.found_person_pub = rospy.Publisher("/found_person", Int8, queue_size=1)
        self.isyn_save_image_clear_pub = rospy.Publisher('/isyn_save_image_clear',Int8,queue_size=1)

        #with darknet
        #sub
        self.found_object_sub = rospy.Subscriber('/darknet_ros/found_object', Int8, self.callback_found_object)
        self.bounding_sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.callback_darknet)
        #pub
        self.image_pub = rospy.Publisher("/send_to_image", Image, queue_size = 5)

        #init
        self.selecting_sub_image = "raw"  # you can choose image type "compressed", "raw"
        self.bridge = CvBridge()
        self.box = BoundingBoxes()
        self.detect_object_mid = []
        self.curr_bebop_req_save_image = 0
        #init isyn
        self.curr_isyn_status_msg = 0
        self.curr_bebop_status_msg = 0
        self.found_person_msg = 0
        self.found_object = 0
        #init flagf
        self.scshot_clear_msg = 0
        self.error_check_num = 0

        # detect_face_init
        self.known_face_encodings = []
        self.known_face_names = []
        dirname = '/home/ksshin/knowns'
        files = os.listdir(dirname)
        for filename in files:
            self.name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                print(self.name)
                self.known_face_names.append(self.name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        # height,width
        self.height = 480
        self.width = 856

        # point center
        self.point_x_center = self.width / 2
        self.point_y_center = self.height / 2

        print("init clear")

    def callback_opencv(self, image_msg):
        if self.selecting_sub_image == "compressed":
            # converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            self.cv_image = cv2.imdecode(np_arr, cv2.COLOR_BGR2RGB)
        elif self.selecting_sub_image == "raw":
            self.cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.cv_image, "bgr8"))


    def callback_darknet(self,found_object_xy_data):
        self.found_object_xy = found_object_xy_data

    def callback_found_object(self,found_object_num_data):
        self.found_object = found_object_num_data.data

    def callback_bebop_mode(self,bebop_mode_data):
        self.bebop_mode = bebop_mode_data.data

    def callback_bebop_status(self,bebop_status_data):
        self.curr_bebop_status_msg = bebop_status_data.data

    def callback_bebop_req_save_image(self,bebop_req_save_image_data):
        self.curr_bebop_req_save_image = bebop_req_save_image_data.data

    def open_face(self):
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(self.cv_image, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame,
                                                                  self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings,
                                                           face_encoding)
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
            # Scale back up face locations since the frame we detected in was scaled to 1/2 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(self.cv_image, (left, top), (right, bottom), red_color, 1)
            # Draw a label with a name below the face
            cv2.rectangle(self.cv_image, (left, bottom - 15), (right, bottom), red_color,
                          cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.cv_image, name, (left + 6, bottom - 6), font, 0.5, white_color,
                        1)

    def isyn_change_stat(self):
        if self.curr_bebop_status_msg == 0:
            self.curr_isyn_status_msg = 0

        if self.curr_bebop_status_msg == 1 and self.cv_image.any():
            self.curr_isyn_status_msg = 1

        if self.curr_bebop_status_msg == 2 and self.cv_image.any() and self.found_object >= 0:
            self.curr_isyn_status_msg = 2

        if self.curr_bebop_status_msg == 3 and self.cv_image.any() and self.found_object >= 1:
            self.curr_isyn_status_msg = 3

        # if self.curr_bebop_status_msg == 5 and self.cv_image.any() and self.found_object >= 1 and self.scshot_clear_msg == 0:
        #     self.curr_isyn_status_msg = 4


    #thread func
    def person_detect(self):
        while(1):
            time.sleep(0.1)
            #change_isyn_status
            self.isyn_change_stat()

            # send msg of isyn status
            self.isyn_status_pub.publish(self.curr_isyn_status_msg)
            self.found_person_pub.publish(self.found_person_msg)

            # draw center_point
            self.cv_image = self.cv_image
            self.cv_image = cv2.line(self.cv_image, (self.point_x_center, self.point_y_center),
                                     (self.point_x_center, self.point_y_center), red_color, 5)

            try:
                self.sort_found_object = []
                for i in range(0, len(self.found_object_xy.bounding_boxes), 1):
                    self.sort_found_object.append(self.found_object_xy.bounding_boxes[i])

                for i in range(1, len(self.sort_found_object), 1):
                    if self.sort_found_object[i].xmin > self.sort_found_object[i - 1].xmin:
                        tmp = self.sort_found_object[i - 1]
                        self.sort_found_object[i - 1] = self.sort_found_object[i]
                        self.sort_found_object[i] = tmp

                self.x_min = []
                self.y_min = []
                self.x_max = []
                self.y_max = []

                for i in range(0, len(self.sort_found_object), 1):
                    if self.sort_found_object[i].probability >= 0.50:
                        self.x_min.append(self.sort_found_object[i].xmin)
                        self.y_min.append(self.sort_found_object[i].ymin)
                        self.x_max.append(self.sort_found_object[i].xmax)
                        self.y_max.append(self.sort_found_object[i].ymax)

                if self.found_object != 0:
                    # detect_person number
                    self.found_person_msg = self.found_object

                    for i in range(0, len(self.x_min), 1):
                        # set person detect bounding box middle
                        self.mid_x = (self.x_min[i] + self.x_max[i]) / 2
                        self.mid_y = (self.y_min[i] + self.y_max[i]) / 2

                        # text detect image name
                        cv2.putText(self.cv_image, 'Person {} '.format(i), (int(self.mid_x) - 40, int(self.mid_y)), cv2.FONT_HERSHEY_DUPLEX,
                                    0.7, white_color, 1)

                        # draw rectangle
                        self.cv_image = cv2.rectangle(self.cv_image, (self.x_min[i], self.y_min[i]), (self.x_max[i], self.y_max[i]),
                                                 red_color, 1)

                        self.detect_object_mid.append(self.mid_x - self.point_x_center)


                    #publish person_to_drone_Alignment
                    if self.detect_object_mid :
                        self.detect_object_mid = str(self.detect_object_mid)
                        self.person_to_drone_Alignment_pub.publish(self.detect_object_mid)
                        self.detect_object_mid = []

                    if self.curr_bebop_req_save_image == 1:
                        dirname = '/home/ksshin/Getimage/'
                        files = os.listdir(dirname)
                        file_num = len(files)
                        self.cv_image_capture = self.cv_image
                        cv2.imwrite('/home/ksshin/Getimage/somebody{}.jpg'.format(file_num), self.cv_image_capture,
                                    params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
                        self.scshot_clear_msg = 1
                        self.isyn_save_image_clear_pub.publish(self.scshot_clear_msg)
                        print("clear screen shot")

                    elif self.curr_bebop_req_save_image == 0:
                        self.scshot_clear_msg = 0
                        self.isyn_save_image_clear_pub.publish(self.scshot_clear_msg)

                elif self.found_object == 0:
                        self.detect_object_mid = 'not data'
                        self.person_to_drone_Alignment_pub.publish(self.detect_object_mid)
                        self.detect_object_mid = []

                # start face_recognition
                self.open_face()

            except AttributeError as e:
                self.error_check_num = self.error_check_num + 1
                if self.error_check_num >= 25:
                    print("wait darknet data or check your bebop mode")
                    print(e)
                    self.error_check_num = 0

            # show display
            cv2.imshow("opencv", self.cv_image), cv2.waitKey(1)

if __name__ == "__main__":
    try:
        isyn_pj = isyn()
        threading1 = threading.Thread(target=isyn_pj.person_detect)
        threading1.daemon = True
        threading1.start()
        rospy.spin()

    except KeyboardInterrupt:
        print("main program exit")

    except rospy.ROSInterruptException as e:
        print("ROS program exit")