#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from nlink_parser.msg import LinktrackNodeframe2
from geometry_msgs.msg import PoseStamped

class UwbCamFusion:
    def __init__(self):
        rospy.init_node('ekf_fusion_node')

        # 状态向量: [x, y, z, vx, vy, vz]
        self.X = np.array([0.5, 0.6, 0.0, 0.0, 0.0, 0.0])
        self.P = np.eye(6) * 1.0
        self.Q = np.diag([1e-4, 1e-4, 1e-4, 1e-3, 1e-3, 1e-3]) # 过程噪声
        
        # 观测噪声
        self.R_uwb = 0.05**2  # UWB 测距标准差约 5cm
        self.R_cam = np.diag([0.02**2, 0.01**2, 0.01**2]) # 距离, 方位角, 俯仰角

        self.last_time = rospy.Time.now()

        self.pub_pose = rospy.Publisher('/fusion/pose', PoseStamped, queue_size=10)
        
        rospy.Subscriber('/nlink_linktrack_nodeframe2', LinktrackNodeframe2, self.uwb_callback)
        
        # 订阅相机数据 
        # rospy.Subscriber('/camera/target_pose', PoseStamped, self.cam_callback)

        rospy.loginfo("EKF Fusion Node Initialized")

    def predict(self):
        current_time = rospy.Time.now()
        dt = (current_time - self.last_time).to_sec()
        if dt <= 0: dt = 0.02
        
        # 状态转移矩阵 F
        F = np.eye(6)
        F[0, 3], F[1, 4], F[2, 5] = dt, dt, dt
        
        self.X = np.dot(F, self.X)
        self.P = np.dot(np.dot(F, self.P), F.T) + self.Q
        self.last_time = current_time

    def uwb_callback(self, msg):
        if not msg.nodes: return
        
        self.predict()

        z_dist = msg.nodes[0].dis 
        
        x, y, z = float(self.X[0]), float(self.X[1]), float(self.X[2])
        d_est = np.sqrt(x**2 + y**2 + z**2) + 1e-6
        res = z_dist - d_est
        
        if abs(float(res)) < 1.0: # 剔除大于 1m 的跳变噪声
            # Jacobian H = [dx/d, dy/d, dz/d, 0, 0, 0]
            H = np.array([[x/d_est, y/d_est, z/d_est, 0, 0, 0]])
            
            S = np.dot(np.dot(H, self.P), H.T) + self.R_uwb
            K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
            
            update_val = np.dot(K,res).flatten()
            self.X = self.X + update_val
            self.P = np.dot((np.eye(6) - np.dot(K, H)), self.P)

        self.publish_pose()

    def cam_callback(self, msg):
        self.predict()
        
        # 假设相机给出的观测是：距离, 水平角, 垂直角
        # z_cam = np.array([msg.range, msg.azimuth, msg.elevation]) 
        pass 

    def publish_pose(self):
        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = "world"
        pose.pose.position.x = self.X[0]
        pose.pose.position.y = self.X[1]
        pose.pose.position.z = self.X[2]
        self.pub_pose.publish(pose)

if __name__ == '__main__':
    try:
        fusion_node = UwbCamFusion()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
