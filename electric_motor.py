import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

P_work = 0.0
P_output = 0.0
n_work = 0.0
i_total = 0.0
i_belt = 0.0
i_gear = 0.0

n_machine = [0.0 for i in range(4)]  # 最后的全过程转速, 依次为电机、高速轴、低速轴、滚筒，下面也一样
T_machine = [0.0 for i in range(4)]  # 全过程转矩
P_machine = [0.0 for i in range(4)]  # 全过程输入功率


def motor_use(motor_final, i_final):  # 测算实际选用电动机后机构的传动比及相关参数

    global n_machine
    global T_machine
    global P_machine
    global i_total
    global i_belt
    global i_gear
    global P_output

    # 确定电机及其物理学参数
    print("  最终选用电机为" + motor_final[0])
    n_machine[0] = motor_final[2]
    T_machine[0] = motor_final[3]
    P_machine[0] = P_output
    print("·电机相关详情请翻阅《机械设计课程设计》（北京大学出版社）168页")

    # 确定传动比
    i_total = i_final
    i_gear = np.sqrt(i_total * 1.4)
    i_belt = i_total / i_gear
    print("·计算各级传动比:")
    print("  总传动比为: %.2f" % i_total)
    print("  V带传动比为: %.2f" % i_belt)
    print("  齿轮传动比为: %.2f" % i_gear)

    # 各级转速
    n_machine[1] = n_machine[0] / i_belt
    n_machine[3] = n_machine[2] = n_machine[1] / i_gear
    print("·计算各级转速:")
    print("  电机轴转速为: %.2f" % n_machine[0])
    print("  减速器高速轴转速为: %.2f" % n_machine[1])
    print("  减速器低速轴转速为: %.2f" % n_machine[2])
    print("  滚筒转速为: %.2f" % n_machine[3])

    # 各级输入功率
    P_machine[1] = P_machine[0] * efficiency_belt
    P_machine[2] = P_machine[1] * efficiency_gear * efficiency_bearing
    P_machine[3] = P_machine[2] * efficiency_coupling * efficiency_bearing
    print("·计算各级输入功率:")
    print("  电机轴输入功率为: %.2f" % P_machine[0])
    print("  减速器高速轴输入功率为: %.2f" % P_machine[1])
    print("  减速器低速轴输入功率为: %.2f" % P_machine[2])
    print("  滚筒输入功率为: %.2f" % P_machine[3])

    # 各级转矩
    for i in range(4):
        T_machine[i] = 9550 * P_machine[i] / n_machine[i]
    print("·计算各级转矩:")
    print("  电机轴转矩为: %.2f" % T_machine[0])
    print("  减速器高速轴转矩为: %.2f" % T_machine[1])
    print("  减速器低速轴转矩为: %.2f" % T_machine[2])
    print("  滚筒输入转矩为: %.2f" % T_machine[3])
    print("------------------电动机运算已结束--------------------")


def motor_scan():  # 选择你的电动机

    global P_work
    global P_output

    # 所有电机数据导入
    all_list_1000r = pd.read_excel('./all_sheets/all_motors.xls', sheet_name="Sheet1")  # 导入千转电机数据
    train_data = np.array(all_list_1000r)
    all_list_1000r = train_data.tolist()
    all_list_1500r = pd.read_excel('./all_sheets/all_motors.xls', sheet_name="Sheet2")  # 导入1.5k电机数据
    train_data = np.array(all_list_1500r)
    all_list_1500r = train_data.tolist()

    # 根据功率挑选合适电机
    list_tag = 1
    motor_1000r = all_list_1000r[list_tag]
    while motor_1000r[1] < P_output:
        list_tag += 1
        motor_1000r = all_list_1000r[list_tag]
    list_tag = 1
    motor_1500r = all_list_1500r[list_tag]
    while motor_1500r[1] < P_output:
        list_tag += 1
        motor_1500r = all_list_1500r[list_tag]

    # 输出电机参数
    print("·电机方案如下:")
    print("  方案1(千转): " + motor_1000r[0] + ",", "额定功率" + str(motor_1000r[1]) + "kW,",
          "满载转速" + str(motor_1000r[2]) + "r/min")
    print("  方案2(1500转): " + motor_1500r[0] + ",", "额定功率" + str(motor_1500r[1]) + "kW,",
          "满载转速" + str(motor_1500r[2]) + "r/min")
    # 这里的参数可修改，如果高转速优先就用1500r，如果经济优先就用1000r

    # high_motorspeed_tag = 1  # 测试用
    if high_motorspeed_tag == 1 and n_work * 24 > 1500:
        motor_use(motor_1500r, motor_1500r[2]/n_work)
    else:
        motor_use(motor_1000r, motor_1000r[2]/n_work)


def output_MotorAbout():  # 输出相关参数并存储到config中，等待二次计算

    config["EM"]["P_work"] = str(P_work)
    config["EM"]["P_output"] = str(P_output)
    config["EM"]["n_d"] = str(1500) if high_motorspeed_tag == 1 else str(1000)
    config["EM"]["n_work"] = str(n_machine[0])  # 这里的电机工作效率以电机满载转速为准
    config["EM"]["P_scheduled"] = str(P_machine[0])
    config["Machine"]["i_total"] = str(i_total)
    config["Machine"]["i_belt"] = str(i_belt)
    config["Machine"]["i_gear"] = str(i_gear)
    config["Machine"]["n_motor"] = str(n_machine[0])
    config["Machine"]["n_highspeed"] = str(n_machine[1])
    config["Machine"]["n_lowspeed"] = str(n_machine[2])
    config["Machine"]["n_output"] = str(n_machine[3])
    config["Machine"]["P_motor"] = str(P_machine[0])
    config["Machine"]["P_highspeed"] = str(P_machine[1])
    config["Machine"]["P_lowspeed"] = str(P_machine[2])
    config["Machine"]["P_output"] = str(P_machine[3])
    config["Machine"]["T_motor"] = str(T_machine[0])
    config["Machine"]["T_highspeed"] = str(T_machine[1])
    config["Machine"]["T_lowspeed"] = str(T_machine[2])
    config["Machine"]["T_output"] = str(T_machine[3])

    with open("./config.ini", "w") as configfile:
        config.write(configfile)


def cal_motor():

    global P_work
    global P_output
    global n_work

    # 计算电机理论功率及转速
    P_work = F_belt * V_belt / 1000
    P_output = P_work / efficiency_total
    n_work = (60000 * V_belt) / (pi * D_roller)
    print("以下是电动机部分")
    print("----------------------------------------------------")
    print("·初步计算得电机理论参数:")
    print("  工作机所需功率P_w = %.2f" % P_work, "kW")
    print("  电机输出功率P_d = %.2f" % P_output, "kW")
    print("  根据《机械设计课程设计》得理论传动比范围荐用范围为 0 ~ 24")
    print("  电机理论所需转速范围为0 ~ %.2f" % (n_work * 24), "r/min")


if __name__ == "__main__":

    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")

    # 数据记录
    efficiency_belt = float(config["General"]["efficiency_belt"])  # V带传输效率
    efficiency_bearing = float(config["General"]["efficiency_bearing"])  # 轴承传输效率
    efficiency_gear = float(config["General"]["efficiency_gear"])  # 齿轮传输效率
    efficiency_coupling = float(config["General"]["efficiency_coupling"])  # 联轴器传输效率
    efficiency_roller = float(config["General"]["efficiency_roller"])  # 滚筒传输效率
    efficiency_total = float(config["General"]["efficiency_total"])  # 总传输效率
    F_belt = float(config["General"]["F_belt"])  # 运输带工作拉力
    V_belt = float(config["General"]["V_belt"])  # 运输带工作速度
    D_roller = float(config["General"]["D_roller"])  # 滚筒直径
    high_motorspeed_tag = int(config["General"]["high_motorspeed_tag"])  # 是否选择高速优先

    # 将数据输出到可视文件中
    output_file = open("Calculated_Data_Electric_Motor.txt", mode='w+')
    temp = sys.stdout
    sys.stdout = output_file
    # 程序运行
    cal_motor()
    motor_scan()
    output_MotorAbout()
    # 返回输出状态
    sys.stdout = temp
    output_file.close()
