import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

high_shaft_cal_d = 0.0
low_shaft_cal_d = 0.0
high_shaft_design_d = 0.0
low_shaft_design_d = 0.0
high_shaft_standard_d = 0.0
low_shaft_standard_d = 0.0
alpha = 20


def first_design():
    global high_shaft_cal_d, high_shaft_standard_d, high_shaft_design_d, \
        low_shaft_cal_d, low_shaft_standard_d, low_shaft_design_d

    # 计入键槽影响，计算轴的计算直径
    high_shaft_cal_d = 110 * np.cbrt(P_highspeed / n_highspeed) * 1.03
    low_shaft_cal_d = 110 * np.cbrt(P_lowspeed / n_lowspeed) * 1.03

    # 以标准值确定轴的最小直径
    tag1 = tag2 = 0
    for i in range(10, 26):
        if i > high_shaft_cal_d and tag1 == 0:
            high_shaft_standard_d = i
            tag1 = 1
        if i > low_shaft_cal_d and tag2 == 0:
            low_shaft_standard_d = i
            tag2 = 1
    for i in range(26, 41, 2):
        if i > high_shaft_cal_d and tag1 == 0:
            high_shaft_standard_d = i
            tag1 = 1
        if i > low_shaft_cal_d and tag2 == 0:
            low_shaft_standard_d = i
            tag2 = 1

    print("以下是轴的实际大小计算部分")
    print("·预选轴用直径")
    print("  高速轴计入单键槽误差后计算最小直径为: %.2f" % high_shaft_cal_d)
    print("  取标准值为: %.1f" % high_shaft_standard_d)
    print("  低速轴计入单键槽误差后计算最小直径为: %.2f" % low_shaft_cal_d)
    print("  取标准值为: %.1f" % low_shaft_standard_d)


def strength_check():

    global alpha

    # 小齿轮处理论所受力
    peripheral_force_high = 2 * T_highspeed / d_gear_shaft_high  # 圆周力
    radial_force_high = peripheral_force_high * np.tan(np.radians(alpha))  # 根据齿形角计算径向力


    print("·轴的强度计算")
    print("  对于直齿圆柱齿轮，理想状况下，减速器轴无轴向力，且轴上载荷方向与大小不变，故此处减速器轴不传递弯矩")
    print("  如下，仅校核危险截面处，即旋转件元件连接处的轴强度")
    print("  1.高速轴部分")


if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")

    # 数据记录
    n_highspeed = float(config["Machine"]["n_highspeed"])
    n_lowspeed = float(config["Machine"]["n_lowspeed"])
    n_output = float(config["Machine"]["n_output"])
    P_motor = float(config["Machine"]["P_motor"])
    P_highspeed = float(config["Machine"]["P_highspeed"])
    P_lowspeed = float(config["Machine"]["P_lowspeed"])
    P_output = float(config["Machine"]["P_output"])
    T_motor = float(config["Machine"]["T_motor"])
    T_highspeed = float(config["Machine"]["T_highspeed"])
    T_lowspeed = float(config["Machine"]["T_lowspeed"])
    T_output = float(config["Machine"]["T_output"])
    d_gear_shaft_low = float(config["Gear"]["d_gear_shaft_low"])
    d_gear_shaft_high = float(config["Gear"]["d_gear_shaft_high"])

    # # 将数据输出到可视文件中
    # output_file = open("Calculated_Data.txt", mode='w+')
    # temp = sys.stdout
    # sys.stdout = output_file
    # 程序运行
    first_design()
    strength_check()
    # # 返回输出状态
    # sys.stdout = temp
    # output_file.close()
