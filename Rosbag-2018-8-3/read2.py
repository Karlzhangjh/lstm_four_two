#-*- coding:utf-8 -*-
import sys
paths = ['/usr/lib/python3.5/site-packages', '/opt/ros/kinetic/lib/python2.7/dist-packages']
sys.path.extend(paths)
import os
import re
import rosbag
import time
import pandas as pd 
'''

	read bagdata and write bagdata to csv

'''
__all__ = ['ReadBag']

class readBag(object):
	def __init__(self, name):
		self.name = name
	def ReadFile(self, folder_path):
		for root, dirs, files in os.walk(folder_path):
			return root, files
	def ReadBag(self, folder_path, topics, attrs, matchdate=None):
		folder, bags = self.ReadFile(folder_path)
		bags.sort()
		print(bags)
		bagdata = dict()
		bagdata['timestamp'] = list()
		bagdata['t'] = list()
		bagdata['obstacle_pos_x'] = list()
		bagdata['obstacle_pos_y'] = list()
		bagdata['obstacle_rel_vel_x'] = list()
		bagdata['obstacle_rel_vel_y'] = list()
		'''for attr in attrs:
			bagdata[attr] = list()'''
		self.bagdata = bagdata
		for bagfile in bags:
			if matchdate:
				if re.search(matchdate, bagfile):
					bag = rosbag.Bag(folder+bagfile)
					print("%s file!" % matchdate)
					self.ReadBagData(bag=bag, topics=topics, attrs=attrs)	
			else:
				bag = rosbag.Bag(folder+bagfile)
				self.ReadBagData(bag=bag, topics=topics, attrs=attrs)
	def ReadBagData(self, bag, topics, attrs):
		#secs_temp = 0
		count = 0
		count_2 = 0

		for topic, msg, t in bag.read_messages(topics=topics):
			count_2 += 1
			#print('---------------------------------------',t)
			if msg.tracks != [] :

				for i in range(len(msg.tracks)):
					if msg.tracks[i].obstacle_id == 19 :

						strt = str(msg.tracks[i].header.stamp.secs) + str(msg.tracks[i].header.stamp.nsecs)
						self.bagdata['t'].append(time.strftime('%Y-%m-%d %H:%M:%S' , time.localtime(float(strt[:10]))))
						self.bagdata['timestamp'].append(strt)
						
						self.bagdata['obstacle_pos_x'].append(msg.tracks[i].obstacle_pos_x)
						self.bagdata['obstacle_pos_y'].append(msg.tracks[i].obstacle_pos_y)
						self.bagdata['obstacle_rel_vel_x'].append(msg.tracks[i].obstacle_rel_vel_x)
						self.bagdata['obstacle_rel_vel_y'].append(msg.tracks[i].obstacle_rel_vel_y)

						count += 1
						print(count_2,'   ',count)							
							
			# tracks has data and the id is 22
			
			'''
			if msg.tracks != [] and msg.tracks[0].obstacle_id == 55:
				#if header.seq
				strt = str(msg.header.stamp.secs) + str(msg.header.stamp.nsecs)
				self.bagdata['t'].append(time.strftime('%Y-%m-%d %H:%M:%S' , time.localtime(float(strt[:10]))))
				self.bagdata['timestamp'].append(strt)
				#if topic == topics[0]:
				for attr in attrs:
					self.bagdata[attr].append(eval('msg.'+attr))
			'''

			'''
			#orientation 50hz  1/5  secs_flags
			if secs_temp == msg.header.stamp.secs :  #equal
				secs_flag += 1
			else :  #not equal
				secs_flag = 0 
				secs_temp = msg.header.stamp.secs

			if secs_flag%5 == 0 :
				#print(msg.header.stamp.secs)			
				strt = str(msg.header.stamp.secs) + str(msg.header.stamp.nsecs)
				self.bagdata['t'].append(time.strftime('%Y-%m-%d %H:%M:%S' , time.localtime(float(strt[:10]))))
				self.bagdata['timestamp'].append(strt)
				#if topic == topics[0]:
				for attr in attrs:
					self.bagdata[attr].append(eval('msg.'+attr))
				secs_temp = msg.header.stamp.secs
			'''						

	def ToCsv(self, file):
		pd_data = pd.DataFrame(self.bagdata, columns=self.bagdata.keys())
		pd_data.to_csv(file)

def ReadBag(folder_path, topics, matchdate, attrs, to_file):
	rb = readBag('read with one topic!')
	''''
	
	attrs = ['obstacle_in_path.obstacle_pos_x', 'curr_twist.linear.x']
	
	to_file = ''
	'''
	'''folder_path = '../nullmaxdata/rawbag20180703/rosbag/bag0703/'
	matchdate = '19-45'
	topics = '/mobileye/parsed_tx/obstacle_data'
	'''
	rb.ReadBag(folder_path=folder_path, topics=topics, attrs=attrs, matchdate=matchdate)
	rb.ToCsv(to_file)
if __name__ == "__main__":
	sys.exit(readBag20180704())

