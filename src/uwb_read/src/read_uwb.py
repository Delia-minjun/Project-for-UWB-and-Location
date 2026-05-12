#!/usr/bin/env python3
import rospy
import serial
from std_msgs.msg import String

def uwb_publisher():
    # 初始化 ROS 节点
    rospy.init_node('uwb_reader_node', anonymous=True)
    pub = rospy.Publisher('uwb_data_raw', String, queue_size=10)
    
    # 配置串口
    ser = serial.Serial('/dev/ttyACM0', 921600, timeout=1)
    
    rospy.loginfo("Reading UWB data from /dev/ttyACM0...")
    
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            raw_data=ser.read(ser.in_waiting)
            # 读取一行数据
            # line = ser.readline().decode('utf-8', errors='ignore').strip()
            # if line:
            rospy.loginfo(f"Raw Hex: {raw_data.hex()}")
                # 发布到 ROS 话题
                # pub.publish(line)

if __name__ == '__main__':
    try:
        uwb_publisher()
    except rospy.ROSInterruptException:
        pass
