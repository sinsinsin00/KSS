// Auto-generated. Do not edit!

// (in-package opencv_isyn.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let isyn = require('./isyn.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class isyn_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.image_header = null;
      this.opencv_isyn = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('image_header')) {
        this.image_header = initObj.image_header
      }
      else {
        this.image_header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('opencv_isyn')) {
        this.opencv_isyn = initObj.opencv_isyn
      }
      else {
        this.opencv_isyn = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type isyn_data
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [image_header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.image_header, buffer, bufferOffset);
    // Serialize message field [opencv_isyn]
    // Serialize the length for message field [opencv_isyn]
    bufferOffset = _serializer.uint32(obj.opencv_isyn.length, buffer, bufferOffset);
    obj.opencv_isyn.forEach((val) => {
      bufferOffset = isyn.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type isyn_data
    let len;
    let data = new isyn_data(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [image_header]
    data.image_header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [opencv_isyn]
    // Deserialize array length for message field [opencv_isyn]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.opencv_isyn = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.opencv_isyn[i] = isyn.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += std_msgs.msg.Header.getMessageSize(object.image_header);
    length += 8 * object.opencv_isyn.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'opencv_isyn/isyn_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e35d1c33611162fb0cd98a5345208bd6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
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
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new isyn_data(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.image_header !== undefined) {
      resolved.image_header = std_msgs.msg.Header.Resolve(msg.image_header)
    }
    else {
      resolved.image_header = new std_msgs.msg.Header()
    }

    if (msg.opencv_isyn !== undefined) {
      resolved.opencv_isyn = new Array(msg.opencv_isyn.length);
      for (let i = 0; i < resolved.opencv_isyn.length; ++i) {
        resolved.opencv_isyn[i] = isyn.Resolve(msg.opencv_isyn[i]);
      }
    }
    else {
      resolved.opencv_isyn = []
    }

    return resolved;
    }
};

module.exports = isyn_data;
