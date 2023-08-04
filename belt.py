import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

belt_type = 'A'
P_design = 0.0
d_small = 0.0
d_large = 0.0


def belt_type_choose():  # 选择V带型号

    global belt_type
    global P_design
    global d_small
    # 取V带类型
    P_design = P_motor * K_A
    select_parameters = 506.7 * (P_design - 0.8) + 357.5
    # 因没有现成的运算函数，遂使用近似函数区分A带区与Z带区，但无法判定除此之外的其它带型
    if select_parameters > n_motor:
        belt_type = 'A'
    else:
        belt_type = 'Z'
    # 取小带轮直径，参考标准系列，不同于课本，直接使用额定功率表各带型的界定范围参考，毕竟没函数
    for i in range(len(belt_P_scheduled)):
        if belt_P_scheduled[i][0] != belt_type:
            continue
        for stp in range(5):
            if belt_P_scheduled[i+stp][1] * pi * n_motor / 60000.0 < 5:
                continue
            if belt_P_scheduled[i+stp][1] * pi * n_motor / 60000.0 > 25:
                break
            d_small = belt_P_scheduled[i+stp][1]
        break
    print(belt_type + str(d_small))


if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")
    # 数据记录
    K_A = float(config["Belt"]["K_A"])
    P_motor = float(config["Machine"]["P_motor"])
    n_motor = float(config["Machine"]["n_motor"])
    # 导入额定功率数据
    belt_P_scheduled = pd.read_excel('./all_sheets/belt_P_scheduled.xls', sheet_name="Sheet1")
    train_data = np.array(belt_P_scheduled)
    belt_P_scheduled = train_data.tolist()
    # # 将数据输出到可视文件中
    # output_file = open("Calculated_Data.txt", mode='w+')
    # temp = sys.stdout
    # sys.stdout = output_file
    # 程序运行
    belt_type_choose()
    # # 返回输出状态
    # sys.stdout = temp
    # output_file.close()
