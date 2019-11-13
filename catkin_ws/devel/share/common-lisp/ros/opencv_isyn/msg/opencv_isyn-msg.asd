
(cl:in-package :asdf)

(defsystem "opencv_isyn-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "isyn" :depends-on ("_package_isyn"))
    (:file "_package_isyn" :depends-on ("_package"))
    (:file "isyn_data" :depends-on ("_package_isyn_data"))
    (:file "_package_isyn_data" :depends-on ("_package"))
  ))