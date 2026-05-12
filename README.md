<h1 align="center">🚗 Unmanned System Target Following: UWB & Vision Fusion Localization</h1>

<p align="center">
  <img src="https://img.shields.io/badge/ROS-Noetic-22314E?style=flat-square&logo=ros&logoColor=white" alt="ROS" />
  <img src="https://img.shields.io/badge/Algorithm-Extended%20Kalman%20Filter-blue?style=flat-square" alt="EKF" />
  <img src="https://img.shields.io/badge/Hardware-UWB%20LinkTrack-brightgreen?style=flat-square" alt="UWB" />
  <img src="https://img.shields.io/badge/Status-Deployed%20on%20Robot-orange?style=flat-square" alt="Status" />
</p>

## Project Description

This repository contains the software stack for the relative localization and target tracking of a mobile robot. The system is designed to fuse **Ultra-Wideband (UWB)** ranging data with **Depth Camera** measurements to ensure robust tracking in complex environments.

## Core Algorithm: EKF Fusion

The system utilizes an **Extended Kalman Filter (EKF)** to fuse asynchronous multi-sensor data. Key capabilities include:
- **Asynchronous Processing**: Handles different sampling rates (e.g., UWB at 50Hz, Camera at 30Hz) seamlessly.
- **Noise Suppression**: Incorporates an innovation threshold (Gating) to automatically reject outlier jumps and UWB high-frequency noise.
- **Trajectory Compensation**: Uses a Constant Velocity (CV) kinematic model to provide continuous state estimation even during temporary sensor occlusion.

---

## Installation & Build

The system runs on **Ubuntu 20.04** with **ROS Noetic**. 

## Future Work
- Complete the data pipeline integration between the physical depth camera and the EKF node.
- Dynamically fine-tune the noise covariance matrices (Q & R) based on real-world statistical analysis.
- Upgrade the kinematic model by incorporating angular velocity states.
