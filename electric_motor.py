import configparser as cp
import pandas as pd
import numpy as np
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
    # 确定电机及其物理学参数
    print("最终选用电机为" + motor_final[0])
    n_machine[0] = motor_final[2]
    T_machine[0] = motor_final[3]
    P_machine[0] = motor_final[1]
    # 确定传动比
    i_total = i_final
    i_belt = np.sqrt(i_total * 1.4)
    i_gear = i_total / i_belt
    # 各级转速
    n_machine[1] = n_machine[0] / i_belt
    n_machine[3] = n_machine[2] = n_machine[1] / i_gear
    # 各级输入功率
    P_machine[1] = P_machine[0] * efficiency_belt
    P_machine[2] = P_machine[1] * efficiency_gear * efficiency_bearing
    P_machine[3] = P_machine[2] * efficiency_coupling * efficiency_roller
    # 各级转矩
    for i in range(4):
        T_machine[i] = 9550 * P_machine[i] / n_machine[i]


def motor_scan():  # 选择你的电动机
    global P_work
    global P_output
    # 所有电机数据导入
    all_list_1000r = pd.read_excel('all_motors.xls', sheet_name="Sheet1")  # 导入千转电机数据
    train_data = np.array(all_list_1000r)
    all_list_1000r = train_data.tolist()
    all_list_1500r = pd.read_excel('all_motors.xls', sheet_name="Sheet2")  # 导入1.5k电机数据
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
    print("电机方案如下:")
    print("方案1(千转): " + motor_1000r[0] + ",", "额定功率" + str(motor_1000r[1]) + "kW,",
          "满载转速" + str(motor_1000r[2]) + "r/min")
    print("方案2(1500转): " + motor_1500r[0] + ",", "额定功率" + str(motor_1500r[1]) + "kW,",
          "满载转速" + str(motor_1500r[2]) + "r/min")
    # 这里的参数可修改，如果高转速优先就用1500r，如果经济优先就用1000r
    high_motorspeed_tag = 1  # 测试用
    if high_motorspeed_tag == 1:
        motor_use(motor_1500r, motor_1500r[2]/n_work)
    else:
        motor_use(motor_1000r, motor_1000r[2]/n_work)


def output_motorabout():  # 输出相关参数并存储到config中，等待二次计算

    config["EM"]["P_work"] = str(P_work)
    config["EM"]["P_output"] = str(P_output)
    config["EM"]["n_d"] = str(1500) if high_motorspeed_tag == 1 else str(1000)
    config["EM"]["n_work"] = str(n_machine[0])
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

    print("电机相关详情请翻阅《机械设计课程设计》（北京大学出版社）168页")


def cal_motor():
    global P_work
    global P_output
    global n_work
    # 计算电机理论功率及转速
    P_work = F_belt * V_belt / 1000
    P_output = P_work / efficiency_total
    n_work = (60000 * V_belt) / (pi * D_roller)


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
    # 如下为测试代码
    cal_motor()
    motor_scan()
    output_motorabout()
