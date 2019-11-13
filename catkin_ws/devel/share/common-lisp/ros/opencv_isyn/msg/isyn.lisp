; Auto-generated. Do not edit!


(cl:in-package opencv_isyn-msg)


;//! \htmlinclude isyn.msg.html

(cl:defclass <isyn> (roslisp-msg-protocol:ros-message)
  ((isyn_stat
    :reader isyn_stat
    :initarg :isyn_stat
    :type cl:integer
    :initform 0)
   (detect_person_num
    :reader detect_person_num
    :initarg :detect_person_num
    :type cl:integer
    :initform 0))
)

(cl:defclass isyn (<isyn>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <isyn>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'isyn)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name opencv_isyn-msg:<isyn> is deprecated: use opencv_isyn-msg:isyn instead.")))

(cl:ensure-generic-function 'isyn_stat-val :lambda-list '(m))
(cl:defmethod isyn_stat-val ((m <isyn>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader opencv_isyn-msg:isyn_stat-val is deprecated.  Use opencv_isyn-msg:isyn_stat instead.")
  (isyn_stat m))

(cl:ensure-generic-function 'detect_person_num-val :lambda-list '(m))
(cl:defmethod detect_person_num-val ((m <isyn>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader opencv_isyn-msg:detect_person_num-val is deprecated.  Use opencv_isyn-msg:detect_person_num instead.")
  (detect_person_num m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <isyn>) ostream)
  "Serializes a message object of type '<isyn>"
  (cl:let* ((signed (cl:slot-value msg 'isyn_stat)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'detect_person_num)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <isyn>) istream)
  "Deserializes a message object of type '<isyn>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'isyn_stat) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'detect_person_num) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<isyn>)))
  "Returns string type for a message object of type '<isyn>"
  "opencv_isyn/isyn")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'isyn)))
  "Returns string type for a message object of type 'isyn"
  "opencv_isyn/isyn")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<isyn>)))
  "Returns md5sum for a message object of type '<isyn>"
  "53ead95707388c06e60c290dfef01194")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'isyn)))
  "Returns md5sum for a message object of type 'isyn"
  "53ead95707388c06e60c290dfef01194")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<isyn>)))
  "Returns full string definition for message of type '<isyn>"
  (cl:format cl:nil "int32 isyn_stat~%int32 detect_person_num~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'isyn)))
  "Returns full string definition for message of type 'isyn"
  (cl:format cl:nil "int32 isyn_stat~%int32 detect_person_num~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <isyn>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <isyn>))
  "Converts a ROS message object to a list"
  (cl:list 'isyn
    (cl:cons ':isyn_stat (isyn_stat msg))
    (cl:cons ':detect_person_num (detect_person_num msg))
))
