from PyQt4.QtCore import QThread, SIGNAL
from build_pointcloud import *

class buildPointcloudThread(QThread):
    def __init__(self,lidar_dir, poses_file_dir, extrinsics_dir, start_time, end_time, origin_time=-1):
        QThread.__init__(self)
        self.lidar_dir = lidar_dir
        self.poses_file_dir = poses_file_dir
        self.extrinsics_dir = extrinsics_dir
        self.start_time = start_time
        self.end_time = end_time
        self.origin_time = origin_time
    def __del__(self):
        self.wait()

    def run(self):
        pointcloud, reflectance = build_pointcloud(self.lidar_dir, self.poses_file_dir, self.extrinsics_dir, self.start_time, self.end_time,self.origin_time)
        self.emit(SIGNAL('drawPointcloud(PyQt_PyObject)'), pointcloud)