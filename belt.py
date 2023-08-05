import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

belt_type = 'A'
P_design = 0.0
d_small = 0.0
d_large = 0.0
center_distance = 0.0
belt_base_len = 0.0


def belt_type_choose():  # 选择V带型号

    global belt_type
    global P_design
    # 取V带类型
    P_design = P_motor * K_A
    select_parameters = 506.7 * (P_design - 0.8) + 357.5
    # 因没有现成的运算函数，遂使用近似函数区分A带区与Z带区，但无法判定除此之外的其它带型
    if select_parameters > n_motor:
        belt_type = 'A'
    else:
        belt_type = 'Z'


def belt_wheel_choose():
    global d_small
    global d_large
    global i_belt
    # 取小带轮直径，参考标准系列，不同于课本，直接使用额定功率表各带型的界定范围参考，毕竟没函数
    for i in range(len(belt_P_scheduled)):
        if belt_P_scheduled[i][0] != belt_type:
            continue
        for stp in range(5):
            if belt_P_scheduled[i + stp][1] * pi * n_motor / 60000.0 < 5:
                continue
            if belt_P_scheduled[i + stp][1] * pi * n_motor / 60000.0 > 20:
                break
            d_small = belt_P_scheduled[i + stp][1]
        break
    # 取大带轮直径，参考标准系列
    last = 0.0
    targeting = 0.0
    d_large = d_small * i_belt
    for i in belt_wheel_designed:
        for j in i:
            last = targeting
            targeting = j
            # 保证带轮传动比不大于齿轮组的同时寻找合适尺寸
            if targeting >= d_large or ((targeting / d_small) > i_total / (targeting / d_small)):
                break
        if targeting >= d_large:
            break
    # 取更接近的值用作带轮
    mid = (last + targeting) / 2
    if d_large >= mid:
        d_large = targeting
    else:
        d_large = last
    # 更新带传动比
    i_belt = d_large / d_small
    print("初定带型号为: %s%.0f" % (belt_type, d_small))
    print("对应小/大带轮直径为: %.0f / %.0f" % (d_small, d_large))
    print("带轮传动比修正为:", i_belt)


def base_length_design():
    global d_small
    global d_large
    global center_distance
    global belt_base_len
    center_distance = ((1.2 * (d_small + d_large)) // 100 + 1) * 100
    belt_base_len = 2 * center_distance + pi * (d_small + d_large) / 2 + ((d_large - d_small) ** 2) / (4 * center_distance)
    print(center_distance, belt_base_len)


if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")
    # 数据记录
    K_A = float(config["Belt"]["K_A"])
    P_motor = float(config["Machine"]["P_motor"])
    n_motor = float(config["Machine"]["n_motor"])
    i_total = float(config["Machine"]["i_total"])
    i_belt = float(config["Machine"]["i_belt"])
    # 导入额定功率数据
    belt_P_scheduled = pd.read_excel('./all_sheets/belt_P_scheduled.xls', sheet_name="Sheet1")
    train_data = np.array(belt_P_scheduled)
    belt_P_scheduled = train_data.tolist()
    # 导入带轮标准系列数据
    belt_wheel_designed = pd.read_excel('./all_sheets/belt_wheel_designed.xls', sheet_name="Sheet1")
    train_data = np.array(belt_wheel_designed)
    belt_wheel_designed = train_data.tolist()
    # # 将数据输出到可视文件中
    # output_file = open("Calculated_Data.txt", mode='w+')
    # temp = sys.stdout
    # sys.stdout = output_file
    # 程序运行
    belt_type_choose()
    belt_wheel_choose()
    base_length_design()
    # # 返回输出状态
    # sys.stdout = temp
    # output_file.close()
