import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")
    # 数据记录


    # 将数据输出到可视文件中
    output_file = open("Calculated_Data.txt", mode='w+')
    temp = sys.stdout
    sys.stdout = output_file
    # 程序运行

    # 返回输出状态
    sys.stdout = temp
    output_file.close()