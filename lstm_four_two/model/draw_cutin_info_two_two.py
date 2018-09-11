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
 	lstm_5 = np.zeros((43,2))
 	lstm_10 = np.zeros((43,2))
 	lstm_15 = np.zeros((43,2))
 	lstm_20 = np.zeros((43,2))
 	lstm_25 = np.zeros((43,2))
 	lstm_30 = np.zeros((43,2))
	for i in range(values.shape[0]):
		num = i/9
		if i%9 == 0:
			real[num,:] = values[i,:]
		elif i%9 == 2:
			lstm_1[num,:] = values[i,:]
		elif i%9 == 3:
			lstm_5[num,:] = values[i,:]
		elif i%9 == 4:
			lstm_10[num,:] = values[i,:]
		elif i%9 == 5:
			lstm_15[num,:] = values[i,:]
		elif i%9 == 6:
			lstm_20[num,:] = values[i,:]
		elif i%9 == 7:
			lstm_25[num,:] = values[i,:]
		elif i%9 == 8:
			lstm_30[num,:] = values[i,:]

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
	
	plt.title('from 20s to predict 0.1 0.5 1 1.5 2 2.5 3 by lstm')

	plt.axhline(0)
	plt.axhline(-2.5)
	plt.axhline(real[-1,1])

	plt.axvline(15.12)
	plt.axvline(33.9)

	plt.plot(real[:,1],'k--',label='real')
	plt.plot(lstm_1[:,1],label='lstm_1')
	plt.plot(lstm_5[:,1],label='lstm_5')
	plt.plot(lstm_10[:,1],label='lstm_10')
	plt.plot(lstm_15[:,1],label='lstm_15')
	plt.plot(lstm_20[:,1],label='lstm_20')
	plt.plot(lstm_25[:,1],label='lstm_25')
	plt.plot(lstm_30[:,1],label='lstm_30')
	plt.legend(loc="upper left")
	
if __name__ == '__main__':
	

	fig = plt.figure(0)

	load_data('two_two_20_1_5_10_15_20_25_30.csv')

	plt.show()

	