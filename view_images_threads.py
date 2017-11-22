from PyQt4.QtCore import QThread, SIGNAL
import os
from image import*
import numpy as np
from transform import*
from interpolate_poses import*
import pydevd
import colorsys

class ViewImagesThread(QThread):
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