#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from nlink_parser.msg import LinktrackNodeframe2
from geometry_msgs.msg import PoseStamped

class UwbCamFusion:
    def __init__(self):
        rospy.init_node('ekf_fusion_node')

        # --- 1. EKF 初始状态 ---
        # 状态向量: [x, y, z, vx, vy, vz]
        self.X = np.array([0.5, 0.6, 0.0, 0.0, 0.0, 0.0])
        self.P = np.eye(6) * 1.0
        self.Q = np.diag([1e-4, 1e-4, 1e-4, 1e-3, 1e-3, 1e-3]) # 过程噪声
        
        # 观测噪声
        self.R_uwb = 0.05**2  # UWB 测距标准差约 5cm
        self.R_cam = np.diag([0.02**2, 0.01**2, 0.01**2]) # 距离, 方位角, 俯仰角

        self.last_time = rospy.Time.now()

        # --- 2. ROS 接口 ---
        self.pub_pose = rospy.Publisher('/fusion/pose', PoseStamped, queue_size=10)
        
        # 订阅 UWB 数据 (nlink_parser 输出)
        rospy.Subscriber('/nlink_linktrack_nodeframe2', LinktrackNodeframe2, self.uwb_callback)
        
        # 订阅相机数据 (假设你的相机节点发布这个话题，格式可自定义)
        # rospy.Subscriber('/camera/target_pose', PoseStamped, self.cam_callback)

        rospy.loginfo("EKF Fusion Node Initialized")

    def predict(self):
        """ 预测步：匀速运动模型 """
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
        """ UWB 更新步 (50Hz) """
        if not msg.nodes: return
        
        # 1. 预测
        self.predict()

        # 2. 获取观测值 (取 ID 为 0 的节点距离作为例子)
        z_dist = msg.nodes[0].dis 
        
        # 3. 容错处理 (同 Matlab 中的残差检查)
        x, y, z = float(self.X[0]), float(self.X[1]), float(self.X[2])
        d_est = np.sqrt(x**2 + y**2 + z**2) + 1e-6
        res = z_dist - d_est
        
        if abs(float(res)) < 1.0: # 剔除大于 1m 的跳变噪声
            # Jacobian H = [dx/d, dy/d, dz/d, 0, 0, 0]
            H = np.array([[x/d_est, y/d_est, z/d_est, 0, 0, 0]])
            
            # 卡尔曼增益
            S = np.dot(np.dot(H, self.P), H.T) + self.R_uwb
            K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
            
            # 更新状态
            update_val = np.dot(K,res).flatten()
            self.X = self.X + update_val
            self.P = np.dot((np.eye(6) - np.dot(K, H)), self.P)

        self.publish_pose()

    def cam_callback(self, msg):
        """ 相机更新步 (30Hz) - 处理距离+双角度 """
        self.predict()
        
        # 假设相机给出的观测是：距离, 水平角, 垂直角
        # 这里需要根据你实际相机算法的输出来填入 z_cam
        # z_cam = np.array([msg.range, msg.azimuth, msg.elevation]) 
        pass 
        # (具体 H 矩阵计算参考上一条回复的推导)

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