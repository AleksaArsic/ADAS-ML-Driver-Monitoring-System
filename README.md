# DriverMonitoringSystem
 Driver monitoring system

**Start date:** 27.3.2020.

## ImageCapture
**Functionality:** Capture pictures from one of three possible video sources:
  - Internal camera
  - External camera
  - Video 
  
Picture capturing starts when trackbar **Capture (STOP/START)** is at position **1**.
Sliding **Capture FPS** trackbar will increase/decrease number of frames per second that are captured in output directory.
  
**Usage**:
ImageCapture.py -v <--vsource> [-h]

**Arguments:**  
-v <--vsource>  
 - 0 - internal camera
 - 1 - external camera
 - < path > \ *.mp4 - video 
