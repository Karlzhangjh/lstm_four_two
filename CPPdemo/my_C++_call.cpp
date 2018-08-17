#include <fstream>
#include <utility>
#include <iostream>

#include <Eigen/Core>
#include <Eigen/Dense>

#include "tensorflow/cc/ops/const_op.h"
#include "tensorflow/cc/ops/image_ops.h"
#include "tensorflow/cc/ops/standard_ops.h"

#include "tensorflow/core/framework/graph.pb.h"
#include "tensorflow/core/framework/tensor.h"

#include "tensorflow/core/graph/default_device.h"
#include "tensorflow/core/graph/graph_def_builder.h"

#include "tensorflow/core/lib/core/errors.h"
#include "tensorflow/core/lib/core/stringpiece.h"
#include "tensorflow/core/lib/core/threadpool.h"
#include "tensorflow/core/lib/io/path.h"
#include "tensorflow/core/lib/strings/stringprintf.h"

#include "tensorflow/core/public/session.h"
#include "tensorflow/core/util/command_line_flags.h"

#include "tensorflow/core/platform/env.h"
#include "tensorflow/core/platform/init_main.h"
#include "tensorflow/core/platform/logging.h"
#include "tensorflow/core/platform/types.h"

#define min 0
#define max 1

using namespace tensorflow::ops;
using namespace tensorflow;
using namespace std;
using tensorflow::Flag;
using tensorflow::Tensor;
using tensorflow::Status;
using tensorflow::string;
using tensorflow::int32 ;

int main(int argc, char** argv )
{
    /*--------------------------------配置关键信息------------------------------*/
    string model_path = "../my_model_1s.pb";

    string input_tensor_name = "lstm_5_input";
    string output_tensor_name = "activation_3/Identity";

    /*--------------------------------创建session------------------------------*/
    Session* session;
    Status status = NewSession(SessionOptions(), &session);//创建新会话Session

    /*--------------------------------从pb文件中读取模型--------------------------------*/
    GraphDef graphdef; //Graph Definition for current model

    Status status_load = ReadBinaryProto(Env::Default(), model_path, &graphdef); //从pb文件中读取图模型;
    if (!status_load.ok()) {
        cout << "ERROR: Loading model failed..." << model_path << std::endl;
        cout << status_load.ToString() << "\n";
        return -1;
    }
    Status status_create = session->Create(graphdef); //将模型导入会话Session中;
    if (!status_create.ok()) {
        cout << "ERROR: Creating graph in session failed..." << status_create.ToString() << std::endl;
        return -1;
    }
    cout << "<----Successfully created session and load graph.------->"<< endl;


    /*--------------------------------数据准备--------------------------------*/
    Eigen::MatrixXf input_mat(20,4);
    input_mat<<14.900936126708984,-0.3072899580001831,-0.45719367265701294,-0.00018134104902856052,14.880328178405762,-0.2817583382129669,-0.44569748640060425,-0.0002478625101502985,
            14.847033500671387,-0.2702173590660095,-0.42701104283332825,-0.0011573004303500056,14.800742149353027,-0.24197040498256683,-0.4136403799057007,-0.0034908712841570377,
            14.747754096984863,-0.20110110938549042,-0.39106282591819763,-0.004100644960999489,14.69748306274414,-0.17054730653762817,-0.3680441975593567,-0.004257105756551027,
            14.649885177612305,-0.1547924429178238,-0.3449624478816986,-0.0047998917289078236, 14.612407684326172,-0.14370453357696533,-0.3267240822315216,-0.005080684553831816,
            14.565342903137207,-0.12986838817596436,-0.3069870173931122,-0.0044813151471316814,14.53187084197998,-0.13159972429275513,-0.272495836019516,-0.0033145283814519644,
            14.518220901489258,-0.13640078902244568,-0.23333893716335297,-0.0014161539729684591,14.498723030090332,-0.13275398313999176,-0.20562049746513367,-0.000669070752337575,
            14.475351333618164,-0.13127531111240387,-0.1807514727115631,-0.0006104772910475731,14.469170570373535,-0.13765588402748108,-0.14550051093101501,0.0005646329373121262,
            14.471479415893555,-0.1438756287097931,-0.08951394259929657,0.0035874301102012396, 14.47757339477539,-0.1468716710805893,-0.03633914142847061,0.005523295607417822,
            14.487256050109863,-0.146312415599823,0.02003718912601471,0.007119690999388695,    14.49159049987793,-0.14584726095199585,0.08539550006389618,0.008989161811769009,
            14.49010181427002,-0.14196546375751495,0.14023378491401672,0.009904530830681324,   14.515379905700684,-0.14664381742477417,0.2138351947069168,0.012141942977905273;
    cout << input_mat.rows()<<input_mat.cols()<<input_mat<<endl;

    //scaler
    vector<vector<float>> scaler(2,vector<float>(input_mat.cols())); //min and max
    //cout << "scaler:" << endl;
    //cout << "min:" << input_mat.colwise().minCoeff() << "max:" << input_mat.colwise().maxCoeff() << endl;

    //scaler min  & max
    for (int i=0; i < input_mat.cols(); ++i) {
        scaler[min][i] = input_mat.colwise().minCoeff()[i];
        scaler[max][i] = input_mat.colwise().maxCoeff()[i];
    }
    //scale input_mat
    for (int feature = 0; feature < 4; ++feature) {
        for (int time_step = 0; time_step < 20; ++time_step)
            input_mat(time_step,feature) = (input_mat(time_step,feature)-scaler[min][feature]) / (scaler[max][feature]-scaler[min][feature]);
    }
    //cout << input_mat.rows()<<input_mat.cols()<<input_mat<<endl;

    //创建一个tensor作为输入网络的接口  对tensor进行赋值
    Tensor my_input_tensor(DT_FLOAT, TensorShape({1,20,4}));
    auto input = my_input_tensor.tensor<float,3>(); //3 dimensions
    for (int time_step = 0; time_step < 20; ++time_step)    {
        for (int feature = 0; feature < 4; ++feature)
            input(0,time_step,feature) = input_mat(time_step,feature);
    }
    cout << my_input_tensor.DebugString()<<endl;


    /*-----------------------------------用网络进行测试-----------------------------------------*/
    cout<<endl<<"<-------------Running the model with test_sequence--------------->"<<endl;
    //前向运行，输出结果一定是一个tensor的vector
    vector<tensorflow::Tensor> outputs;
    string output_node = output_tensor_name;
    Status status_run = session->Run({{input_tensor_name, my_input_tensor}}, {output_node}, {}, &outputs);

    if (!status_run.ok()) {
        cout << "ERROR: RUN failed..."  << std::endl;
        cout << status_run.ToString() << "\n";
        return -1;
    }

    //read tensor
    auto output = outputs[0].tensor<float,2>();//2D
    float predict_x = output(0)*(scaler[max][0]-scaler[min][0]) + scaler[min][0];
    float predict_y = output(1)*(scaler[max][1]-scaler[min][1]) + scaler[min][1];
    
    //把输出值提取出来
    cout << outputs[0].DebugString() << endl;  //outputs.size() == 1
    cout << "output tensor:   " << predict_x << " " << predict_y<< endl;
    
    return 0;
}


