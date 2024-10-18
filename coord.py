import numpy as np
import ctypes, ctypes.util
import threading
from ctypes import *
import time
from enum import Enum
import sys
import pandas as pd
import atexit

class AGC_MODE_TYPE(ctypes.c_int):
    TRANSMITTER_AND_SENSOR_AGC = 0  # 对应 C++ 中的 TRANSMITTER_AND_SENSOR_AGC
    SENSOR_AGC_ONLY = 0             # 对应 C++ 中的 SENSOR_AGC_ONLY


class DEVICE_TYPES(ctypes.c_int):
    STANDARD_SENSOR = 0
    TYPE_800_SENSOR = 0
    STANDARD_TRANSMITTER = 0
    MINIBIRD_TRANSMITTER = 0
    SMALL_TRANSMITTER = 0
    TYPE_500_SENSOR = 0
    TYPE_180_SENSOR = 0
    TYPE_130_SENSOR = 0
    TYPE_TEM_SENSOR = 0
    UNKNOWN_SENSOR = 0
    UNKNOWN_TRANSMITTER = 0
    TYPE_800_BB_SENSOR = 0
    TYPE_800_BB_STD_TRANSMITTER = 0
    TYPE_800_BB_SMALL_TRANSMITTER = 0
    TYPE_090_BB_SENSOR = 0


class SYSTEM_PARAMETER_TYPE(Enum):
    SELECT_TRANSMITTER = 0
    POWER_LINE_FREQUENCY = 0
    AGC_MODE = 0
    MEASUREMENT_RATE = 0
    MAXIMUM_RANGE = 0
    METRIC = 0
    VITAL_PRODUCT_DATA = 0
    POST_ERROR = 0
    DIAGNOSTIC_TEST = 0
    REPORT_RATE = 0
    COMMUNICATIONS_MEDIA = 0
    LOGGING = 0
    RESET = 0
    AUTOCONFIG = 0
    AUXILIARY_PORT = 0
    COMMUTATION_MODE = 0
    END_OF_LIST = 0



class SENSOR_CONFIGURATION(ctypes.Structure):
    _fields_ = [
        ("serialNumber", c_ulong),
        ("boardNumber", c_ushort),
        ("channelNumber", c_ushort),
        ("type", DEVICE_TYPES),
        ("attached", c_bool),
    ]

class TRANSMITTER_CONFIGURATION(ctypes.Structure):
    _fields_ = [
        ("serialNumber", c_ulong),
        ("boardNumber", c_ushort),
        ("channelNumber", c_ushort),
        ("type", DEVICE_TYPES),
        ("attached", c_bool),
    ]

class SYSTEM_CONFIGURATION(ctypes.Structure):
    _fields_ = [
        ("measurementRate", c_double),
        ("powerLineFrequency", c_double),
        ("maximumRange", c_double),
        ("agcMode", AGC_MODE_TYPE),
        ("numberBoards", c_int),
        ("numberSensors", c_int),
        ("numberTransmitters", c_int),
        ("transmitterIDRunning", c_int),
        ("metric", c_bool)
    ]


class DOUBLE_POSITION_ANGLES_RECORD(ctypes.Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("z", c_double),
        ("a", c_double),
        ("e", c_double),
        ("r", c_double),
    ]


#声明结构体
p_main_B = []
p_B = []
p_sub_B = []
m_config = SYSTEM_CONFIGURATION()
m_config2 = SENSOR_CONFIGURATION()
m_config3 = TRANSMITTER_CONFIGURATION()
VALID_STATUS = 0x00000000
GLOBAL_ERROR = 0x00000001
errorCode = ctypes.c_int()
i = ctypes.c_int()
sensorID = ctypes.c_int()
id = ctypes.c_short()
records = ctypes.c_int(100)
output = []
METRIC = 5
metricOption = True  # 或者 False，根据需要设置
pMetricOption = pointer(c_bool(metricOption))
numberBytes = ctypes.c_int()
goal = ctypes.c_double()
wait = float(10)  # 按照 ctypes 的要求将整数转换为浮点数
current_time = time.time()
global data
data = [
    [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]


# 错误反馈函数
def errorHandler(error):
    buffer = ctypes.create_string_buffer(1024)  # 创建一个 1024 字节大小的字符数组作为缓冲区
    pBuffer = ctypes.byref(buffer)  # 获取缓冲区的指针
    numberBytes = 0

    while error != 0:
        vc_dll = ctypes.CDLL(dll_path)
        error = vc_dll.GetErrorText(error, pBuffer, ctypes.sizeof(buffer),0)
        numberBytes = len(buffer.value)
        # buffer.raw[numberBytes] = '\n'  # 在缓冲区末尾添加换行符
        sys.stdout.write(buffer.value.decode())  # 将缓冲区的内容打印到标准输出
    sys.exit(0)



def load_dll():
    global dll_path
    dll_path = './parameter/ATC3DG64.dll'
    try:
        vc_dll = ctypes.CDLL(dll_path)   #加载动态库
        print("成功加载动态库")

        # 初始化系统
        errorCode = vc_dll.InitializeBIRDSystem()
        if (errorCode != 0):errorHandler(errorCode)

        # 设置系统参数：metric为true，使输出为mm
        errorCode = vc_dll.SetSystemParameter(METRIC, pMetricOption, ctypes.sizeof(ctypes.c_int32))
        if (errorCode != 0):errorHandler(errorCode)

        # 获取系统参数
        errorCode = vc_dll.GetBIRDSystemConfiguration(ctypes.byref(m_config))
        if (errorCode != 0):errorHandler(errorCode)

        # 获取传感器配置参数
        numberSensors = m_config.numberSensors
        for i in range(numberSensors):
            errorCode = vc_dll.GetSensorConfiguration(i, ctypes.byref(m_config2))
            if (errorCode != 0):errorHandler(errorCode)

        # 获取发射机配置参数
        numberTransmitters = m_config.numberTransmitters
        for i in range(numberTransmitters):
            errorCode = vc_dll.GetTransmitterConfiguration(0, ctypes.byref(m_config3))
            if (errorCode != 0):errorHandler(errorCode)


        for id in range(numberTransmitters):
            if m_config3.attached:
                errorCode = vc_dll.SetSystemParameter(SYSTEM_PARAMETER_TYPE.SELECT_TRANSMITTER.value,
                                                      ctypes.byref(ctypes.c_int(id)), ctypes.sizeof(ctypes.c_int16))
                if (errorCode != 0):errorHandler(errorCode)
                break

        record = DOUBLE_POSITION_ANGLES_RECORD()
        pRecord = ctypes.pointer(record)

        goal = wait + time.process_time()
        global data
        # for i in range(100):
        global data_history
        # 创建一个空的DataFrame
        df = pd.DataFrame(columns=['ID', 'X', 'Y', 'Z', 'A', 'E', 'R'])
        data_history = []

        while True:
            while goal < time.process_time():
                pass
            goal = wait + time.process_time()

            for sensorID in range(m_config.numberSensors):
                errorCode = vc_dll.GetAsynchronousRecord(sensorID, pRecord, ctypes.sizeof(record))
                if (errorCode != 0): errorHandler(errorCode)

                status = vc_dll.GetSensorStatus(sensorID)
                if (status == 0):
                    output = "%d %8.3f %8.3f %8.3f %8.2f %8.2f %8.2f\n" % (
                        sensorID,
                        record.x,
                        record.y,
                        record.z,
                        record.a,
                        record.e,
                        record.r
                    )
                    row_index = int(output.split()[0])  # 获取输出中的行索引
                    # 将输出转换为浮点数列表
                    values = [float(x) for x in output.split()[1:]]
                    # 更新 data 列表中的对应行
                    data[row_index] = [row_index] + values
                    # 将 data 列表添加到历史记录中
                    data_history.append(data.copy())


    except OSError as e:
        print(e, "加载动态库失败")












#求解坐标系A到坐标系B的变换矩阵：
def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]  # total points
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # centre the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    H = np.matmul(np.transpose(AA),BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.matmul(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = np.matmul(Vt.T,U.T)

    t = -np.matmul(R, centroid_A) + centroid_B
    return R, t


# 从位姿信息到单个传感器的位姿变换矩阵
def getT_fromPose(x, y, z, α, β, γ):
    # 计算旋转矩阵
    Rx = np.array([[1, 0, 0], [0, np.cos(α), -np.sin(α)], [0, np.sin(α), np.cos(α)]])
    Ry = np.array([[np.cos(β), 0, np.sin(β)], [0, 1, 0], [-np.sin(β), 0, np.cos(β)]])
    Rz = np.array([[np.cos(γ), -np.sin(γ), 0], [np.sin(γ), np.cos(γ), 0], [0, 0, 1]])
    # print('RX,RY,RZ: ', Rx, Ry, Rz)
    # 计算旋转矩阵的乘积
    R = Rz @ Ry @ Rx

    # 构造变换矩阵
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [x, y, z]
    return T

# 从变换矩阵到位姿信息的函数
def getPose_fromT(M):
    # 从旋转矩阵中提取欧拉角，采用zyx（yaw-pitch-roll）方式
    R = M[0:3, 0:3]
    t = M[0:3, 3]
    rx = np.arctan2(R[2, 1], R[2, 2])
    ry = np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
    rz = np.arctan2(R[1, 0], R[0, 0])
    return np.array([t[0], t[1], t[2], rx, ry, rz])



def process_output():
    global p_main_B,p_sub_B
    while True:
        time.sleep(50/500)
        global data
        a = np.array([[data[0][1], data[0][2], data[0][3]],
                      [data[1][1], data[1][2], data[1][3]],
                      [data[2][1], data[2][2], data[2][3]],
                      [data[3][1], data[3][2], data[3][3]],
                      [data[4][1], data[4][2], data[4][3]],
                      [data[5][1], data[5][2], data[5][3]]
                      ])



        # 计算每列的平均值
        column_means = a.mean(axis=0)

        # 去中心化
        b = a - column_means




        r, t = rigid_transform_3D(a, b)

        #矩阵A到矩阵B的变换矩阵（后期放到子程序内）
        T_AB = np.eye(4)
        T_AB[:3, :3] = r
        T_AB[:3, 3] = t





        #得到传感器位姿信息在磁场坐标系下的位姿变换矩阵
        x_A, y_A, z_A, α_A, β_A, γ_A = np.array([data[6][1], data[6][2], data[6][3], np.deg2rad(data[6][6]), np.deg2rad(data[6][5]), np.deg2rad(data[6][4])])
        # print('A坐标系下的位姿信息：', x_A, y_A, z_A, α_A, β_A, γ_A)
        T_A = getT_fromPose(x_A, y_A, z_A, α_A, β_A, γ_A)
        # print('T_A: ', T_A)
        #得到传感器在B坐标系下的位姿变换矩阵
        T_B = T_AB.dot(T_A)
        # print('T_B: ', T_B)
        #得到传感器在B坐标系下的位姿信息
        p_B = getPose_fromT(T_B)
        # print('B坐标系下的位姿信息：', p_B)


        p_main_B = p_B[:3]
        # print(p_main_B)



        # 已知在传感器子坐标系下的针尖坐标值
        p_sub = np.array([-5.8, 159,  7.1])
        # 转换到磁场坐标系
        p_sub_homo = np.hstack([p_sub, 1])       # 转换为齐次坐标
        p_sub_homo = np.dot(T_A, p_sub_homo)    #得到磁场坐标值

        # 得到B坐标系下的坐标值
        p_sub_B = T_AB @ p_sub_homo


        # print('针尖在B坐标系下的值：', p_sub_B[:3])


        # print("针尖的磁场坐标：", p_sub_homo)






def save_data_history():
    global data_history
    # 将历史记录转换为 DataFrame
    print("调用程序")
    history_df = pd.DataFrame(data_history, columns=['ID', 'X', 'Y', 'Z', 'A', 'E', 'R'])
    # 将 DataFrame 保存为 Excel 文件
    history_df.to_excel('医学影像变换.xlsx', index=False)
    print('保存数据成功')








if __name__=='__main__':

    added_thred = threading.Thread(target=load_dll)
    added_thred.start()
    added_thread2 = threading.Thread(target=process_output)
    added_thread2.start()

    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     print(1)
    #     # 保存一次数据
    #     save_data_history()
    #     # 等待线程结束
    #     added_thred.join()
    #     added_thread2.join()