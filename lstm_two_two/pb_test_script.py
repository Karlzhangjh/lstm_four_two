# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
#import cv2
from sklearn.preprocessing import MinMaxScaler

#data processing
def data_process(input_frame):
	scaler = MinMaxScaler(feature_range=(0,1))
	scaled_data = scaler.fit_transform(input_frame)
	scaled_data = np.array(scaled_data)

	input_frame_3D = scaled_data.reshape(1,scaled_data.shape[0],scaled_data.shape[1])

	return input_frame_3D,scaler

#inverse prediction
def inverse_predict(predict_result,input_frame_3D,scaler):
	input_frame = input_frame_3D.reshape(input_frame_3D.shape[1],input_frame_3D.shape[2])
	
	input_frame[-1,:2] = predict_result # using the scaled data to inverse
	inv_Y_hat = scaler.inverse_transform(input_frame)
	
	predict_pos = inv_Y_hat[-1,:2]

	return predict_pos


"""-----------------------------------------------定义识别函数-----------------------------------------"""
def recognize(input_frame, pb_file_path):
    with tf.Graph().as_default():
    	input_frame_3D,scaler = data_process(input_frame)

        output_graph_def = tf.GraphDef()

        # 打开.pb模型
        with open(pb_file_path, "rb") as f:
            output_graph_def.ParseFromString(f.read())
            tensors = tf.import_graph_def(output_graph_def, name="")
            print("tensors:",tensors)

        # 在一个session中去run一个前向
        with tf.Session() as sess:
            init = tf.global_variables_initializer()
            sess.run(init)

            op = sess.graph.get_operations()

            # 打印图中有的操作
            for i,m in enumerate(op):
                print('op{}:'.format(i),m.values())

            input_x = sess.graph.get_tensor_by_name("lstm_5_input:0")  # 具体名称看上一段代码的input.name
            print("input_X:",input_x)

            out_softmax = sess.graph.get_tensor_by_name("activation_3/Identity:0")  # 具体名称看上一段代码的output.name
            print("Output:",out_softmax)


            predict_result = sess.run(out_softmax,feed_dict={input_x: input_frame_3D})

            predict_pos = inverse_predict(predict_result,input_frame_3D,scaler)
            print("predict_pos:", predict_pos)


pb_path = './my_model_1s.pb'
#img = 'Pictures/6.png'
input_frame = [[14.900936126708984,-0.3072899580001831,-0.45719367265701294,-0.00018134104902856052],[14.880328178405762,-0.2817583382129669,-0.44569748640060425,-0.0002478625101502985],
				[14.847033500671387,-0.2702173590660095,-0.42701104283332825,-0.0011573004303500056],[14.800742149353027,-0.24197040498256683,-0.4136403799057007,-0.0034908712841570377],
				[14.747754096984863,-0.20110110938549042,-0.39106282591819763,-0.004100644960999489],[14.69748306274414,-0.17054730653762817,-0.3680441975593567,-0.004257105756551027],
				[14.649885177612305,-0.1547924429178238,-0.3449624478816986,-0.0047998917289078236], [14.612407684326172,-0.14370453357696533,-0.3267240822315216,-0.005080684553831816],
				[14.565342903137207,-0.12986838817596436,-0.3069870173931122,-0.0044813151471316814],[14.53187084197998,-0.13159972429275513,-0.272495836019516,-0.0033145283814519644],
				[14.518220901489258,-0.13640078902244568,-0.23333893716335297,-0.0014161539729684591],[14.498723030090332,-0.13275398313999176,-0.20562049746513367,-0.000669070752337575],
				[14.475351333618164,-0.13127531111240387,-0.1807514727115631,-0.0006104772910475731],[14.469170570373535,-0.13765588402748108,-0.14550051093101501,0.0005646329373121262],
				[14.471479415893555,-0.1438756287097931,-0.08951394259929657,0.0035874301102012396], [14.47757339477539,-0.1468716710805893,-0.03633914142847061,0.005523295607417822],
				[14.487256050109863,-0.146312415599823,0.02003718912601471,0.007119690999388695],    [14.49159049987793,-0.14584726095199585,0.08539550006389618,0.008989161811769009],
				[14.49010181427002,-0.14196546375751495,0.14023378491401672,0.009904530830681324],   [14.515379905700684,-0.14664381742477417,0.2138351947069168,0.012141942977905273]]
input = np.array(input_frame)

recognize(input, pb_path)