from PyQt4.QtCore import QThread, SIGNAL
from build_pointcloud import *
#import pydevd


class BuildPointcloudThread(QThread):
    def __init__(self,lidar_dir, poses_file_dir, extrinsics_dir, start_time, end_time, origin_time=-1, extr_pose=0, pose_kind=2):
        QThread.__init__(self)
        self.lidar_dir = lidar_dir
        self.poses_file_dir = poses_file_dir
        self.extrinsics_dir = extrinsics_dir
        self.start_time = start_time
        self.end_time = end_time
        self.origin_time = origin_time
        self.extr_pose = extr_pose
        self.pose_kind = pose_kind
    def __del__(self):
        self.wait()

    def run(self):

        if self.pose_kind == 2:
            pointcloud, reflectance = build_pointcloud(self.lidar_dir, self.poses_file_dir, self.extrinsics_dir, self.start_time, self.end_time,self.origin_time)
        else:
            pointcloud, reflectance = build_pointcloud_nasze(self.lidar_dir, self.poses_file_dir, self.extrinsics_dir,
                                                       self.start_time, self.end_time, self.origin_time, self.extr_pose,
                                                       self.pose_kind)
        self.emit(SIGNAL('drawPointcloud(PyQt_PyObject)'), pointcloud)


