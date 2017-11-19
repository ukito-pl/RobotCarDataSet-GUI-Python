# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 University of Oxford
# Authors:
#  Geoff Pascoe (gmp@robots.ox.ac.uk)
#
# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
################################################################################

import os
import re
import numpy as np
import csv
from transform import *

from interpolate_poses import interpolate_vo_poses, interpolate_ins_poses
import pydevd


def build_pointcloud(lidar_dir, poses_file, extrinsics_dir, start_time, end_time, origin_time=-1):
    """Builds a pointcloud by combining multiple LIDAR scans with odometry information.

    Args:
        lidar_dir (str): Directory containing LIDAR scans.
        poses_file (str): Path to a file containing pose information. Can be VO or INS data.
        extrinsics_dir (str): Directory containing extrinsic calibrations.
        start_time (int): UNIX timestamp of the start of the window over which to build the pointcloud.
        end_time (int): UNIX timestamp of the end of the window over which to build the pointcloud.
        origin_time (int): UNIX timestamp of origin frame. Pointcloud coordinates are relative to this frame.

    Returns:
        numpy.ndarray: 3xn array of (x, y, z) coordinates of pointcloud
        numpy.array: array of n reflectance values or None if no reflectance values are recorded (LDMRS)

    Raises:
        ValueError: if specified window doesn't contain any laser scans.
        IOError: if scan files are not found.

    """

    if origin_time < 0:
        origin_time = start_time


    try:
        lidar = re.search('(lms_front|lms_rear|ldmrs)', lidar_dir).group(0)
        timestamps_path = os.path.join(lidar_dir, os.pardir, lidar + '.timestamps')
    except:
        timestamps_path = os.path.split(lidar_dir)[0] + '/plik.timestamps'
        lidar = 'lms_front'


    timestamps = []
    with open(timestamps_path) as timestamps_file:
        for line in timestamps_file:
            try:
                timestamp = int(line.split('\n\r')[0])
            except:
                timestamp = int(line.split(' ')[0])
            if start_time <= timestamp <= end_time:
                timestamps.append(timestamp)

    if len(timestamps) == 0:
        raise ValueError("No LIDAR data in the given time bracket.")
    print len(timestamps)

    with open(os.path.join(extrinsics_dir, lidar + '.txt')) as extrinsics_file:
        extrinsics = next(extrinsics_file)
    G_posesource_laser = build_se3_transform([float(x) for x in extrinsics.split(' ')])

    try:
        poses_type = re.search('(vo|ins)\.csv', poses_file).group(1)
    except:
        pass

    if poses_type == 'ins':
        with open(os.path.join(extrinsics_dir, 'ins.txt')) as extrinsics_file:
            extrinsics = next(extrinsics_file)
            G_posesource_laser = np.linalg.solve(build_se3_transform([float(x) for x in extrinsics.split(' ')]),
                                                     G_posesource_laser)

        poses = interpolate_ins_poses(poses_file, timestamps, origin_time,2)   #jeśli pose_kind == 2 to z projektu RCDS
    else:
        # sensor is VO, which is located at the main vehicle frame
        poses = interpolate_vo_poses(poses_file, timestamps, origin_time)

    pointcloud = np.array([[0], [0], [0], [0]])
    if lidar == 'ldmrs':
        reflectance = None
    else:
        reflectance = np.empty((0))

        ####
    for i in range(0, len(poses)):
        scan_path = os.path.join(lidar_dir, str(timestamps[i]) + '.bin')
        if not os.path.isfile(scan_path):
            continue

        scan_file = open(scan_path)
        scan = np.fromfile(scan_file, np.double)
        scan_file.close()

        scan = scan.reshape((len(scan) // 3, 3)).transpose()

        if lidar != 'ldmrs':
            # LMS scans are tuples of (x, y, reflectance)
            reflectance = np.concatenate((reflectance, np.ravel(scan[2, :])))
            scan[2, :] = np.zeros((1, scan.shape[1]))

        scan = np.dot(np.dot(poses[i], G_posesource_laser), np.vstack([scan, np.ones((1, scan.shape[1]))]))
        pointcloud = np.hstack([pointcloud, scan])

    pointcloud = pointcloud[:, 1:]
    if pointcloud.shape[1] == 0:
        raise IOError("Could not find scan files for given time range in directory " + lidar_dir)



    return pointcloud, reflectance

def build_pointcloud_nasze(lidar_dir, poses_file, extrinsics_dir, start_time, end_time, origin_time=-1, extr_pose=0, pose_kind=3):
    if origin_time < 0:
        origin_time = start_time

    with open(os.path.join(extrinsics_dir)) as lidar_extr_file:
        lidar_extrinsics = next(lidar_extr_file)
        G_posesource_laser = build_se3_transform([float(x) for x in lidar_extrinsics.split(' ')])

    with open(os.path.join(extr_pose)) as pose_extr_file:
        pose_extrinsics = next(pose_extr_file)
        G_posesource_laser = np.linalg.solve(build_se3_transform([float(x) for x in pose_extrinsics.split(' ')]),
                                             G_posesource_laser)

    timestamps = []
    with open('lidar.timestamps') as timestamps_file:
        for line in timestamps_file:
            try:
                timestamp = int(line.split('\n\r')[0])
            except:
                timestamp = int(line.split(' ')[0])
            if start_time <= timestamp <= end_time:
                timestamps.append(timestamp)

    poses = interpolate_ins_poses('poses.csv', timestamps, origin_time, pose_kind)

    pointcloud = np.array([[0], [0], [0]])
    reflectance = np.empty((0))
    i = 0
    lidar_data_file = open('dane_odleglosci_lidar.csv', 'r')
    for line in lidar_data_file:
        if i < poses.__len__():
            dane_pointcloud = []
            j = -45
            for x in line.split(','):
                s = np.pi / 180 * j
                a = float(x) * np.cos(s)
                b = float(x) * np.sin(s)
                j = j + 1
                one_point = [a] + [-b] + [0]
                dane_pointcloud.append(one_point)
            dane_pointcloud = np.array(dane_pointcloud)
            scan = dane_pointcloud.transpose()

            reflectance = np.concatenate((reflectance, np.ravel(scan[2, :])))
            scan[2, :] = np.zeros((1, scan.shape[1]))

            # teoretycznie przy dobrych extrinsicsach ta linijka powinna załatwić całą zabawę z układami współrzędnych, ale ...
            scan = np.dot(np.dot(poses[i], G_posesource_laser), np.vstack([scan, np.ones((1, scan.shape[1]))]))

            pointcloud = np.hstack([pointcloud, scan[0:3]])

            i = i + 1
    # ...przy pozycjach z vo trzeba jeszcze obrócić(nie wiem dlaczego):
    if pose_kind == 1:
        pointcloud = np.dot(pointcloud.transpose(), euler_to_so3([1.57, 0, 0]))
        pointcloud = pointcloud.transpose()
    # w ogóle końcowy układ współrzędnych nie jest taki jaki powinien być ale już walić to, tak jak jest przynajmniej wyświetla dobrze
    print len(poses)
    pointcloud = pointcloud[:, 1:]
    if pointcloud.shape[1] == 0:
        raise IOError("Could not find scan files for given time range in directory " + lidar_dir)

    lidar_data_file.close()

    return pointcloud, reflectance

if __name__ == "__main__":
    from pyqtgraph.Qt import QtCore, QtGui
    import pyqtgraph.opengl as gl
    import pyqtgraph as pg
    import argparse
    import sys
    

    parser = argparse.ArgumentParser(description='Build and display a pointcloud')
    parser.add_argument('--poses_file', type=str, default=None, help='File containing relative or absolute poses')
    parser.add_argument('--extrinsics_dir', type=str, default=None,
                        help='Directory containing extrinsic calibrations')
    parser.add_argument('--laser_dir', type=str, default=None, help='Directory containing LIDAR data')

    args = parser.parse_args()

    lidar = re.search('(lms_front|lms_rear|ldmrs)', args.laser_dir).group(0)
    timestamps_path = os.path.join(args.laser_dir, os.pardir, lidar + '.timestamps')
    with open(timestamps_path) as timestamps_file:
        start_time = int(next(timestamps_file).split(' ')[0])

    end_time = start_time + 0.5e7

    print 'Building PointCloud...'
    pointcloud, reflectance = build_pointcloud(args.laser_dir, args.poses_file,
                                               args.extrinsics_dir, start_time, end_time)
    print 'PointCloud built'

    if reflectance is not None:
        colours = (reflectance - reflectance.min()) / (reflectance.max() - reflectance.min())
        colours = 1 / (1 + np.exp(-10 * (colours - colours.mean())))
    else:
        colours = 'gray'

   
    
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.opts['distance'] = 40
    #w.setBackgroundColor(200,200,200)
    w.show()
    w.setWindowTitle('Built Pointcloud')

    
    pointcloud = pointcloud[0:3, : ].transpose()
    print pointcloud
    pointcloud = np.array(-pointcloud)
    sp1 = gl.GLScatterPlotItem(pos=pointcloud, size=1, color=[0.7,0.7,0.7,1], pxMode=True)
    sp1.translate(5,5,0)
    w.addItem(sp1)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
    
