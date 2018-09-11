# -*- coding: utf-8 -*-
 
from __future__ import print_function
    
import time
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import random
from math import sqrt
from numpy import concatenate
from pandas import DataFrame
from pandas import concat


# load data
def load_data(filename):
	#load_data
	raw_data = pd.read_csv(filename)
	raw_data = raw_data.iloc[:,[0,1]]#[4,3,5,6]
	#print(raw_data)

	values = np.array(raw_data).astype(float)

 	real = np.zeros((43,2))
 	lstm_1 = np.zeros((43,2))
 	lstm_3 = np.zeros((43,2))
 	lstm_5 = np.zeros((43,2))
 	lstm_6 = np.zeros((43,2))
 	lstm_7 = np.zeros((43,2))
 	lstm_8 = np.zeros((43,2))
 	lstm_9 = np.zeros((43,2))
	for i in range(values.shape[0]):
		num = i/9
		if i%9 == 0:
			real[num,:] = values[i,:]
		elif i%9 == 2:
			lstm_1[num,:] = values[i,:]
		elif i%9 == 3:
			lstm_3[num,:] = values[i,:]
		elif i%9 == 4:
			lstm_5[num,:] = values[i,:]
		elif i%9 == 5:
			lstm_6[num,:] = values[i,:]
		elif i%9 == 6:
			lstm_7[num,:] = values[i,:]
		elif i%9 == 7:
			lstm_8[num,:] = values[i,:]
		elif i%9 == 8:
			lstm_9[num,:] = values[i,:]

	'''
	raw_data = raw_data.iloc[:,[4,3]]#[4,3,5,6]
	print('the shape of raw_data: ',raw_data.shape)#(500,8)
	print(raw_data.head(12))

	values = np.array(raw_data).astype(float)

	#frame as supervised learning
	reframed_data = series_to_supervised(raw_data,1,time_range)#from 10 to predict next 1 
	#print(reframed_data)

	#drop columns we don't want to predict
	reframed_data = reframed_data.iloc[:,[0,1,2,3,time_range*features,time_range*features+1]]  
	'''
	
	plt.title('from 20s to predict 0.1 0.3 0.5 0.6 0.7 0.8 0.9s by lstm')

	plt.axhline(0)
	plt.axhline(-2.5)
	plt.axhline(real[-1,1])

	plt.axvline(17.96)
	plt.axvline(35.6)

	plt.plot(real[:,1],'k--',label='real')
	plt.plot(lstm_1[:,1],label='lstm_1')
	plt.plot(lstm_3[:,1],label='lstm_3')
	plt.plot(lstm_5[:,1],label='lstm_4')
	plt.plot(lstm_6[:,1],label='lstm_6')
	plt.plot(lstm_7[:,1],label='lstm_7')
	plt.plot(lstm_8[:,1],label='lstm_8')
	plt.plot(lstm_9[:,1],label='lstm_9')
	plt.legend(loc="upper left")
	
if __name__ == '__main__':
	

	fig = plt.figure(0)

	load_data('20_1_3_5_6_7_8_9.csv')

	plt.show()

	