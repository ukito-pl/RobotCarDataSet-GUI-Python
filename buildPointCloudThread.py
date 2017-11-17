from PyQt4.QtCore import QThread, SIGNAL
from build_pointcloud import *
import csv
#import pydevd

class BuildPointcloudThread(QThread):
    def __init__(self,lidar_dir, poses_file_dir, extrinsics_dir, start_time, end_time, origin_time=-1, extr_pose=0, pose_kind=3):
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
        pointcloud, reflectance = build_pointcloud(self.lidar_dir, self.poses_file_dir, self.extrinsics_dir, self.start_time, self.end_time,self.origin_time,self.extr_pose, self.pose_kind)
        self.emit(SIGNAL('drawPointcloud(PyQt_PyObject)'), pointcloud)


class BuildPointcloudThreadLive(QThread):
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
        #Nie dziala
        if self.origin_time < 0:
            self.origin_time = self.start_time

        lidar = re.search('(lms_front|lms_rear|ldmrs)', self.lidar_dir).group(0)
        timestamps_path = os.path.join(self.lidar_dir, os.pardir, lidar + '.timestamps')

        timestamps = []
        with open(timestamps_path) as timestamps_file:
            for line in timestamps_file:
                timestamp = int(line.split(' ')[0])
                if self.start_time <= timestamp <= self.end_time:
                    timestamps.append(timestamp)

        if len(timestamps) == 0:
            raise ValueError("No LIDAR data in the given time bracket.")



        poses_type = re.search('(vo|ins)\.csv', self.poses_file_dir).group(1)

        if poses_type == 'ins':

            with open(self.poses_file_dir) as ins_file:
                ins_reader = csv.reader(ins_file)
                headers = next(ins_file)
                pose_timestamps = [0]
                xyzrpy = [[0,0,0,0,0,0]]
                upper_timestamp = max(max(timestamps), self.origin_time)

                for row in ins_reader:
                    timestamp = int(row[0])
                    pose_timestamps.append(timestamp)

                    xyzrpy.append([float(v) for v in row[5:8]] + [float(v) for v in row[-3:]])

                    if timestamp >= upper_timestamp:
                        break

        else:
            # sensor is VO, which is located at the main vehicle frame
            with open(self.poses_file_dir) as vo_file:
                vo_reader = csv.reader(vo_file)
                headers = next(vo_file)

                pose_timestamps = [0]
                xyzrpy = [[0, 0, 0, 0, 0, 0]]

                lower_timestamp = min(min(timestamps), self.origin_time)
                upper_timestamp = max(max(timestamps), self.origin_time)

                for row in vo_reader:
                    timestamp = int(row[0])
                    if timestamp < lower_timestamp:
                        pose_timestamps[0] = timestamp
                        continue

                    pose_timestamps.append(timestamp)

                    pydevd.settrace(suspend=False, trace_only_current_thread=True)
                    xyzrpy.append([float(v) for v in row[2:8]])
                    print xyzrpy

                    if timestamp >= upper_timestamp:
                        break

        j = 0
        for i in range(0,pose_timestamps.__len__()):
            if pose_timestamps[i] <= timestamps[j] <= pose_timestamps[i+1]:
                requested_timestamp = timestamps[j]
                requested_xyzrpy = (xyzrpy[i+1]-xyzrpy[i])#/(pose_timestamps[i+1]-pose_timestamps[i])*requested_timestamp + (xyzrpy[i] - (xyzrpy[i+1]-xyzrpy[i])/(pose_timestamps[i+1]-pose_timestamps[i])*pose_timestamps[i])

        #self.emit(SIGNAL('drawPointcloud(PyQt_PyObject)'), pointcloud)