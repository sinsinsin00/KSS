// Auto-generated. Do not edit!

// (in-package opencv_isyn.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class isyn {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.isyn_stat = null;
      this.detect_person_num = null;
    }
    else {
      if (initObj.hasOwnProperty('isyn_stat')) {
        this.isyn_stat = initObj.isyn_stat
      }
      else {
        this.isyn_stat = 0;
      }
      if (initObj.hasOwnProperty('detect_person_num')) {
        this.detect_person_num = initObj.detect_person_num
      }
      else {
        this.detect_person_num = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type isyn
    // Serialize message field [isyn_stat]
    bufferOffset = _serializer.int32(obj.isyn_stat, buffer, bufferOffset);
    // Serialize message field [detect_person_num]
    bufferOffset = _serializer.int32(obj.detect_person_num, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type isyn
    let len;
    let data = new isyn(null);
    // Deserialize message field [isyn_stat]
    data.isyn_stat = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [detect_person_num]
    data.detect_person_num = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'opencv_isyn/isyn';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '53ead95707388c06e60c290dfef01194';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 isyn_stat
    int32 detect_person_num
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new isyn(null);
    if (msg.isyn_stat !== undefined) {
      resolved.isyn_stat = msg.isyn_stat;
    }
    else {
      resolved.isyn_stat = 0
    }

    if (msg.detect_person_num !== undefined) {
      resolved.detect_person_num = msg.detect_person_num;
    }
    else {
      resolved.detect_person_num = 0
    }

    return resolved;
    }
};

module.exports = isyn;
