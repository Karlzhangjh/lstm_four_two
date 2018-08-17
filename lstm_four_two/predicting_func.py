# -*- coding: utf-8 -*-
from __future__ import print_function
    
import tensorflow as tf 
import sys
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
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers.core import Dense,Activation,Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential,load_model

#data processing
def data_process(input_frame):
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = scaler.fit_transform(input_frame)
	scaled_data = np.array(scaled_data)

	input_frame_3D = scaled_data.reshape(1,scaled_data.shape[0],scaled_data.shape[1])

	return input_frame_3D,scaler

#prediction
def pos_predict(my_model,scaler,input_frame_3D):
	print(my_model)
	print(input_frame_3D.shape)
	Y_hat = my_model.predict(input_frame_3D)
	
	input_frame = input_frame_3D.reshape(input_frame_3D.shape[1],input_frame_3D.shape[2])
	
	input_frame[-1,:2] = Y_hat # using the scaled data to inverse
	inv_Y_hat = scaler.inverse_transform(input_frame)
	
	predict_pos = inv_Y_hat[-1,:2]

	return predict_pos

def predicting(input_frame):	
	print('>>>>> Loading data...')
	# 20 frames for test, 2s
	#input_frame = np.array(input_frame)

	# 10 frames for prediction, 1s
	fore_step = 10
	true_pos = [15.266347885131836,-0.17504578828811646]
	true_pos = np.array(true_pos)
	print('>>>>> Data Loaded. Compiling...')

	input_frame_3D,scaler = data_process(input_frame)

	#model saved as HDF5 file    model.save('my_model.h5')
	if fore_step == 1:
		my_model = load_model('my_model_0.1s.h5') 
	elif fore_step == 5:
		my_model = load_model('my_model_0.5s.h5') 
	elif fore_step == 10:
		my_model = load_model('my_model_1s.h5') # 1 step:my_model_0.1s.h5 ; 5 step:my_model_0.5s.h5 ; 10 step:my_model_1s.h5 ; 

	#predict next position 
	predict_pos = pos_predict(my_model,scaler,input_frame_3D)
	print('True pos: ',true_pos,'  Predict pos: ',predict_pos)

	return predict_pos
		

if __name__ == '__main__':
	sys.exit()