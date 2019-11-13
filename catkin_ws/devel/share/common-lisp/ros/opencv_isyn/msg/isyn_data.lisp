; Auto-generated. Do not edit!


(cl:in-package opencv_isyn-msg)


;//! \htmlinclude isyn_data.msg.html

(cl:defclass <isyn_data> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (image_header
    :reader image_header
    :initarg :image_header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (opencv_isyn
    :reader opencv_isyn
    :initarg :opencv_isyn
    :type (cl:vector opencv_isyn-msg:isyn)
   :initform (cl:make-array 0 :element-type 'opencv_isyn-msg:isyn :initial-element (cl:make-instance 'opencv_isyn-msg:isyn))))
)

(cl:defclass isyn_data (<isyn_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <isyn_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'isyn_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name opencv_isyn-msg:<isyn_data> is deprecated: use opencv_isyn-msg:isyn_data instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <isyn_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader opencv_isyn-msg:header-val is deprecated.  Use opencv_isyn-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'image_header-val :lambda-list '(m))
(cl:defmethod image_header-val ((m <isyn_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader opencv_isyn-msg:image_header-val is deprecated.  Use opencv_isyn-msg:image_header instead.")
  (image_header m))

(cl:ensure-generic-function 'opencv_isyn-val :lambda-list '(m))
(cl:defmethod opencv_isyn-val ((m <isyn_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader opencv_isyn-msg:opencv_isyn-val is deprecated.  Use opencv_isyn-msg:opencv_isyn instead.")
  (opencv_isyn m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <isyn_data>) ostream)
  "Serializes a message object of type '<isyn_data>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'image_header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'opencv_isyn))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'opencv_isyn))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <isyn_data>) istream)
  "Deserializes a message object of type '<isyn_data>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'image_header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'opencv_isyn) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'opencv_isyn)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'opencv_isyn-msg:isyn))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<isyn_data>)))
  "Returns string type for a message object of type '<isyn_data>"
  "opencv_isyn/isyn_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'isyn_data)))
  "Returns string type for a message object of type 'isyn_data"
  "opencv_isyn/isyn_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<isyn_data>)))
  "Returns md5sum for a message object of type '<isyn_data>"
  "e35d1c33611162fb0cd98a5345208bd6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'isyn_data)))
  "Returns md5sum for a message object of type 'isyn_data"
  "e35d1c33611162fb0cd98a5345208bd6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<isyn_data>)))
  "Returns full string definition for message of type '<isyn_data>"
  (cl:format cl:nil "Header header~%Header image_header~%isyn[] opencv_isyn~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: opencv_isyn/isyn~%int32 isyn_stat~%int32 detect_person_num~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'isyn_data)))
  "Returns full string definition for message of type 'isyn_data"
  (cl:format cl:nil "Header header~%Header image_header~%isyn[] opencv_isyn~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: opencv_isyn/isyn~%int32 isyn_stat~%int32 detect_person_num~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <isyn_data>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'image_header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'opencv_isyn) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <isyn_data>))
  "Converts a ROS message object to a list"
  (cl:list 'isyn_data
    (cl:cons ':header (header msg))
    (cl:cons ':image_header (image_header msg))
    (cl:cons ':opencv_isyn (opencv_isyn msg))
))
