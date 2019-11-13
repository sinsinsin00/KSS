;; Auto-generated. Do not edit!


(when (boundp 'opencv_isyn::isyn_data)
  (if (not (find-package "OPENCV_ISYN"))
    (make-package "OPENCV_ISYN"))
  (shadow 'isyn_data (find-package "OPENCV_ISYN")))
(unless (find-package "OPENCV_ISYN::ISYN_DATA")
  (make-package "OPENCV_ISYN::ISYN_DATA"))

(in-package "ROS")
;;//! \htmlinclude isyn_data.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass opencv_isyn::isyn_data
  :super ros::object
  :slots (_header _image_header _opencv_isyn ))

(defmethod opencv_isyn::isyn_data
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:image_header __image_header) (instance std_msgs::Header :init))
    ((:opencv_isyn __opencv_isyn) (let (r) (dotimes (i 0) (push (instance opencv_isyn::isyn :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _image_header __image_header)
   (setq _opencv_isyn __opencv_isyn)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:image_header
   (&rest __image_header)
   (if (keywordp (car __image_header))
       (send* _image_header __image_header)
     (progn
       (if __image_header (setq _image_header (car __image_header)))
       _image_header)))
  (:opencv_isyn
   (&rest __opencv_isyn)
   (if (keywordp (car __opencv_isyn))
       (send* _opencv_isyn __opencv_isyn)
     (progn
       (if __opencv_isyn (setq _opencv_isyn (car __opencv_isyn)))
       _opencv_isyn)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; std_msgs/Header _image_header
    (send _image_header :serialization-length)
    ;; opencv_isyn/isyn[] _opencv_isyn
    (apply #'+ (send-all _opencv_isyn :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; std_msgs/Header _image_header
       (send _image_header :serialize s)
     ;; opencv_isyn/isyn[] _opencv_isyn
     (write-long (length _opencv_isyn) s)
     (dolist (elem _opencv_isyn)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; std_msgs/Header _image_header
     (send _image_header :deserialize buf ptr-) (incf ptr- (send _image_header :serialization-length))
   ;; opencv_isyn/isyn[] _opencv_isyn
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _opencv_isyn (let (r) (dotimes (i n) (push (instance opencv_isyn::isyn :init) r)) r))
     (dolist (elem- _opencv_isyn)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get opencv_isyn::isyn_data :md5sum-) "e35d1c33611162fb0cd98a5345208bd6")
(setf (get opencv_isyn::isyn_data :datatype-) "opencv_isyn/isyn_data")
(setf (get opencv_isyn::isyn_data :definition-)
      "Header header
Header image_header
isyn[] opencv_isyn

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: opencv_isyn/isyn
int32 isyn_stat
int32 detect_person_num


")



(provide :opencv_isyn/isyn_data "e35d1c33611162fb0cd98a5345208bd6")


