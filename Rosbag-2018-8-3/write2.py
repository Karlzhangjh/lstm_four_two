#-*- coding:utf-8 -*-
import sys
paths = ['/usr/lib/python3.5/site-packages', '/opt/ros/kinetic/lib/python2.7/dist-packages']
sys.path.extend(paths)
import os
import re
import rosbag
from read2 import *


def main():
	folder_path = '/home/xiang/Documents/Rosbag-2018-8-3/'
	topics = ['/fusion/obstacle_list']
	#topics = ['/odom/current_pose']
	attrs = []#'tracks[0].obstacle_pos_x', 'tracks[0].obstacle_pos_y',
			#'tracks[0].obstacle_rel_vel_x','tracks[0].obstacle_rel_vel_y']#,
	#		 'pose.orientation.x','pose.orientation.y','pose.orientation.z','pose.orientation.w']
	#attrs = ['pose.orientation.x','pose.orientation.y','pose.orientation.z','pose.orientation.w']
	to_file = '/home/xiang/Documents/Rosbag-2018-8-3/X_Y_dX_dY_11_27.csv'
	matchdate = 'px2_zhang_2018-08-03-11-27'
	ReadBag(folder_path, topics, matchdate, attrs, to_file)
		

if __name__ == "__main__":
	sys.exit(main())
	