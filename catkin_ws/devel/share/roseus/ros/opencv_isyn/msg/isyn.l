;; Auto-generated. Do not edit!


(when (boundp 'opencv_isyn::isyn)
  (if (not (find-package "OPENCV_ISYN"))
    (make-package "OPENCV_ISYN"))
  (shadow 'isyn (find-package "OPENCV_ISYN")))
(unless (find-package "OPENCV_ISYN::ISYN")
  (make-package "OPENCV_ISYN::ISYN"))

(in-package "ROS")
;;//! \htmlinclude isyn.msg.html


(defclass opencv_isyn::isyn
  :super ros::object
  :slots (_isyn_stat _detect_person_num ))

(defmethod opencv_isyn::isyn
  (:init
   (&key
    ((:isyn_stat __isyn_stat) 0)
    ((:detect_person_num __detect_person_num) 0)
    )
   (send-super :init)
   (setq _isyn_stat (round __isyn_stat))
   (setq _detect_person_num (round __detect_person_num))
   self)
  (:isyn_stat
   (&optional __isyn_stat)
   (if __isyn_stat (setq _isyn_stat __isyn_stat)) _isyn_stat)
  (:detect_person_num
   (&optional __detect_person_num)
   (if __detect_person_num (setq _detect_person_num __detect_person_num)) _detect_person_num)
  (:serialization-length
   ()
   (+
    ;; int32 _isyn_stat
    4
    ;; int32 _detect_person_num
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _isyn_stat
       (write-long _isyn_stat s)
     ;; int32 _detect_person_num
       (write-long _detect_person_num s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _isyn_stat
     (setq _isyn_stat (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _detect_person_num
     (setq _detect_person_num (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get opencv_isyn::isyn :md5sum-) "53ead95707388c06e60c290dfef01194")
(setf (get opencv_isyn::isyn :datatype-) "opencv_isyn/isyn")
(setf (get opencv_isyn::isyn :definition-)
      "int32 isyn_stat
int32 detect_person_num


")



(provide :opencv_isyn/isyn "53ead95707388c06e60c290dfef01194")


