# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, SIGNAL
import os
from image import*
import numpy as np
from transform import*
from interpolate_poses import*
import pydevd
import colorsys

class ViewImagesThreadSDK(QThread):
    def __init__(self,timestamps_path, start_timestamp, end_timestamp, camera_model, dir_camera, dir_poses, dir_extrinsic,project,pointcloud = -1):
        QThread.__init__(self)
        self.timestamps_path = timestamps_path
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.camera_model = camera_model
        self.dir_camera = dir_camera
        self.dir_poses = dir_poses
        self.dir_extr = dir_extrinsic
        self.project = project
        self.pointcloud = pointcloud

    def __del__(self):
        self.wait()

    def run(self):
        images = []
        self.emit(SIGNAL('update_progressbar(PyQt_PyObject)'), [2, 0])

        timestamps = []
        with open(self.timestamps_path) as timestamps_file:
            for line in timestamps_file:
                try:
                    timestamp = int(line.split('\n\r')[0])
                except:
                    timestamp = int(line.split(' ')[0])
                if self.start_timestamp <= timestamp <= self.end_timestamp:
                    timestamps.append(timestamp)

        if self.camera_model and self.project:
            extrinsics_path = os.path.join(self.dir_extr, self.camera_model.camera + '.txt')
            with open(extrinsics_path) as extrinsics_file:
                extrinsics = [float(x) for x in next(extrinsics_file).split(' ')]
            G_camera_vehicle = build_se3_transform(extrinsics)

            poses_type = re.search('(vo|ins)\.csv', self.dir_poses).group(1)
            if poses_type == 'ins':
                with open(os.path.join(self.dir_extr, 'ins.txt')) as extrinsics_file:
                    extrinsics = next(extrinsics_file)
                    G_camera_posesource = G_camera_vehicle * build_se3_transform([float(x) for x in extrinsics.split(' ')])
                poses = interpolate_ins_poses(self.dir_poses, timestamps, timestamps[0], 2)
            else:
                # VO frame and vehicle frame are the same
                G_camera_posesource = G_camera_vehicle
                poses = interpolate_vo_poses(self.dir_poses, timestamps, timestamps[0])

            for i in range(0,timestamps.__len__()):
                timestamp = timestamps[i]
                if (timestamp >= self.start_timestamp) and (timestamp <= self.end_timestamp):
                    if i == 0:
                        G_camera_posesource_good = G_camera_posesource
                    else:
                        G_camera_posesource_good = np.dot(G_camera_posesource, np.linalg.inv(poses[i - 1]))

                    pointcloud = np.dot(G_camera_posesource_good, self.pointcloud)
                    image_path = os.path.join(self.dir_camera, str(timestamp) + '.png')

                    image = load_image(image_path, self.camera_model)
                    imgv = np.array(image)
                    uv, depth = self.camera_model.project(pointcloud, image.shape)
                    try:
                        dmax = max(depth)
                    except:
                        pass

                    for j in range(0, uv.shape[1]):
                        d = depth[j] / dmax * 0.66
                        rgb = np.array(colorsys.hsv_to_rgb(0.66 - d, 1.0, 1.0))
                        u = int(uv[0, j])
                        v = int(uv[1, j])
                        imgv[v, u, :] = rgb * 255
                    images.append(imgv)

                    percent = float(i+1)/len(timestamps)*100
                    self.emit(SIGNAL('update_progressbar(PyQt_PyObject)'), [2,percent])
        else:
            for i in range(0, timestamps.__len__()):
                timestamp = timestamps[i]

                image_path = os.path.join(self.dir_camera, str(timestamp) + '.png')
                image = load_image(image_path,self.camera_model)
                imgv = np.array(image)
                images.append(imgv)
                percent = float(i + 1) / len(timestamps) * 100
                self.emit(SIGNAL('update_progressbar(PyQt_PyObject)'), [2, percent])


        imagesnp = np.array(images)
        self.emit(SIGNAL('draw_images(PyQt_PyObject)'), imagesnp)

class ViewImagesThreadCustom(QThread):
    def __init__(self,images_path, delta_t, start_time, end_time,project, pointcloud = None, camera_model = None,
                 camera_extr_path = None, pose_path = None, pose_extr_path = None ):
        QThread.__init__(self)
        self.images_path = images_path
        self.delta_t = delta_t # różnica czasu pomiędzy dwoma klatkami, w ms
        self.start_time = start_time # czas startu względem pierwszej klatki, w ms
        self.end_time = end_time #czas zakończenia względem pierwszej klatki, w ms
        self.project = project
        self.pointcloud = pointcloud
        self.camera_model = camera_model
        self.camera_extr_path = camera_extr_path
        self.pose_path = pose_path
        self.pose_extr_path = pose_extr_path

    def __del__(self):
        self.wait()

    def run(self):
        images = []
        num_images = (self.end_time-self.start_time)/self.delta_t
        if not self.project:
            p = 0
            i = self.start_time/self.delta_t
            for t in range(self.start_time,self.end_time,self.delta_t):
                try:
                    plik = 'out%03d.png' % (i + 1)
                    img_path = os.path.join(self.images_path, plik)
                    img = Image.open(img_path)
                    imgv = np.array(img)
                    images.append(imgv)
                    i = i + 1
                    p = p + 1
                    percent = float(p)/num_images*100
                    self.emit(SIGNAL('update_progressbar(PyQt_PyObject)'), [2, percent])

                except:
                    pass
        else:
            with open(self.camera_extr_path) as extrinsics_file:
                extrinsics = [float(x) for x in next(extrinsics_file).split(' ')]
            camera_extrinsics = build_se3_transform(extrinsics)

            with open(self.pose_extr_path) as pose_extr_file:
                pose_extrinsics = [float(x) for x in next(pose_extr_file).split(' ')]
                pose_extr = build_se3_transform(pose_extrinsics)


            timestamps = []
            with open('lidar.timestamps') as timestamps_file:
                for line in timestamps_file:
                    try:
                        timestamp = int(line.split('\n\r')[0])
                    except:
                        timestamp = int(line.split(' ')[0])
                    if self.start_time*1000 <= timestamp <= self.end_time*1000:
                        timestamps.append(timestamp)

            timestamps = []
            i = 0
            for t in range(self.start_time, self.end_time, self.delta_t):
                timestamps.append(t*1000)
                i = i+ 1

            #pydevd.settrace()
            poses = interpolate_ins_poses('poses.csv', timestamps, timestamps[0], 1)

            pointcloud = np.dot(self.pointcloud.transpose(), camera_extrinsics)
            pointcloud = pointcloud.transpose()
            pointcloud_base = pointcloud
            i = int(self.start_time / self.delta_t)
            k = 0
            for t in range(self.start_time, self.end_time, self.delta_t):
                try:
                    plik = 'out%03d.png' % (i + 1)
                    img_path = os.path.join(self.images_path, plik)
                    image = Image.open(img_path)
                except:
                    pass

                if k > 0:
                    #pydevd.settrace()
                    trans = np.linalg.solve( pose_extr,camera_extrinsics)
                    poses[k-1] = np.linalg.inv(poses[k-1])
                    poses[k-1] = np.dot(poses[k-1],trans)
                    pointcloud = np.dot( poses[k-1],pointcloud_base)


                imgv = np.array(image)
                uv, depth = self.camera_model.project(pointcloud, imgv.shape)
                try:
                    dmax = max(depth)
                except:
                    print "Projection failed, no point in front of camera"
                    pass

                for j in range(0, uv.shape[1]):
                    d = depth[j] / dmax * 0.66
                    rgb = np.array(colorsys.hsv_to_rgb(0.66 - d, 1.0, 1.0))
                    u = int(uv[0, j])
                    v = int(uv[1, j])
                    imgv[v, u, :] = rgb * 255
                images.append(imgv)
                k = k + 1
                i = i + 1
                percent = float(k) / num_images * 100
                self.emit(SIGNAL('update_progressbar(PyQt_PyObject)'), [2, percent])


        imagesnp = np.array(images)
        self.emit(SIGNAL('draw_images(PyQt_PyObject)'), imagesnp)