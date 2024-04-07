import configparser as cp

import pandas as pd
import numpy as np
import sys
from numpy import pi


class electric_motor_compress:

    def __init__(self):
        # 导入config
        self.config = cp.ConfigParser()
        self.config.read("./config.ini")
        # 数据记录
        self.efficiency_belt = float(self.config["General"]["efficiency_belt"])  # V带传输效率
        self.efficiency_bearing = float(self.config["General"]["efficiency_bearing"])  # 轴承传输效率
        self.efficiency_gear = float(self.config["General"]["efficiency_gear"])  # 齿轮传输效率
        self.efficiency_coupling = float(self.config["General"]["efficiency_coupling"])  # 联轴器传输效率
        self.efficiency_roller = float(self.config["General"]["efficiency_roller"])  # 滚筒传输效率
        self.efficiency_total = float(self.config["General"]["efficiency_total"])  # 总传输效率
        self.F_belt = float(self.config["General"]["F_belt"])  # 运输带工作拉力
        self.V_belt = float(self.config["General"]["V_belt"])  # 运输带工作速度
        self.D_roller = float(self.config["General"]["D_roller"])  # 滚筒直径
        self.high_motorspeed_tag = int(self.config["General"]["high_motorspeed_tag"])  # 是否选择高速优先
        self.P_work = 0.0
        self.P_output = 0.0
        self.n_work = 0.0
        self.i_total = 0.0
        self.i_belt = 0.0
        self.i_gear = 0.0
        self.n_machine = [0.0 for i in range(4)]  # 最后的全过程转速, 依次为电机、高速轴、低速轴、滚筒，下面也一样
        self.T_machine = [0.0 for i in range(4)]  # 全过程转矩
        self.P_machine = [0.0 for i in range(4)]  # 全过程输入功率
        # 将数据输出到可视文件中
        output_file = open("./outputs/Calculated_Data_Electric_Motor.txt", mode='w+')
        self.output_tmp = sys.stdout
        sys.stdout = output_file

    def motor_use(self, motor_final, i_final):  # 测算实际选用电动机后机构的传动比及相关参数
        # 确定电机及其物理学参数
        print("  最终选用电机为" + motor_final[0])
        self.n_machine[0] = motor_final[2]
        self.T_machine[0] = motor_final[3]
        self.P_machine[0] = self.P_output
        print("·电机相关详情请翻阅《机械设计课程设计》（北京大学出版社）168页")

        # 确定传动比
        self.i_total = i_final
        self.i_gear = np.sqrt(self.i_total * 1.4)
        self.i_belt = self.i_total / self.i_gear
        print("·计算各级传动比:")
        print("  总传动比为: %.2f" % self.i_total)
        print("  V带传动比为: %.2f" % self.i_belt)
        print("  齿轮传动比为: %.2f" % self.i_gear)

        # 各级转速
        self.n_machine[1] = self.n_machine[0] / self.i_belt
        self.n_machine[3] = self.n_machine[2] = self.n_machine[1] / self.i_gear
        print("·计算各级转速:")
        print("  电机轴转速为: %.2f" % self.n_machine[0])
        print("  减速器高速轴转速为: %.2f" % self.n_machine[1])
        print("  减速器低速轴转速为: %.2f" % self.n_machine[2])
        print("  滚筒转速为: %.2f" % self.n_machine[3])

        # 各级输入功率
        self.P_machine[1] = self.P_machine[0] * self.efficiency_belt
        self.P_machine[2] = self.P_machine[1] * self.efficiency_gear * self.efficiency_bearing
        self.P_machine[3] = self.P_machine[2] * self.efficiency_coupling * self.efficiency_bearing
        print("·计算各级输入功率:")
        print("  电机轴输入功率为: %.2f" % self.P_machine[0])
        print("  减速器高速轴输入功率为: %.2f" % self.P_machine[1])
        print("  减速器低速轴输入功率为: %.2f" % self.P_machine[2])
        print("  滚筒输入功率为: %.2f" % self.P_machine[3])

        # 各级转矩
        for i in range(4):
            self.T_machine[i] = 9550 * self.P_machine[i] / self.n_machine[i]
        print("·计算各级转矩:")
        print("  电机轴转矩为: %.2f" % self.T_machine[0])
        print("  减速器高速轴转矩为: %.2f" % self.T_machine[1])
        print("  减速器低速轴转矩为: %.2f" % self.T_machine[2])
        print("  滚筒输入转矩为: %.2f" % self.T_machine[3])
        print("------------------电动机运算已结束--------------------")

    def motor_scan(self):  # 选择你的电动机
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
        while motor_1000r[1] < self.P_output:
            list_tag += 1
            motor_1000r = all_list_1000r[list_tag]
        list_tag = 1
        motor_1500r = all_list_1500r[list_tag]
        while motor_1500r[1] < self.P_output:
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
        if self.high_motorspeed_tag == 1 and self.n_work * 24 > 1500:
            self.motor_use(motor_1500r, motor_1500r[2] / self.n_work)
        else:
            self.motor_use(motor_1000r, motor_1000r[2] / self.n_work)

    def output_MotorAbout(self):  # 输出相关参数并存储到config中，等待二次计算
        self.config["EM"]["P_work"] = str(self.P_work)
        self.config["EM"]["P_output"] = str(self.P_output)
        self.config["EM"]["n_d"] = str(1500) if self.high_motorspeed_tag == 1 else str(1000)
        self.config["EM"]["n_work"] = str(self.n_machine[0])  # 这里的电机工作效率以电机满载转速为准
        self.config["EM"]["P_scheduled"] = str(self.P_machine[0])
        self.config["Machine"]["i_total"] = str(self.i_total)
        self.config["Machine"]["i_belt"] = str(self.i_belt)
        self.config["Machine"]["i_gear"] = str(self.i_gear)
        self.config["Machine"]["n_motor"] = str(self.n_machine[0])
        self.config["Machine"]["n_highspeed"] = str(self.n_machine[1])
        self.config["Machine"]["n_lowspeed"] = str(self.n_machine[2])
        self.config["Machine"]["n_output"] = str(self.n_machine[3])
        self.config["Machine"]["P_motor"] = str(self.P_machine[0])
        self.config["Machine"]["P_highspeed"] = str(self.P_machine[1])
        self.config["Machine"]["P_lowspeed"] = str(self.P_machine[2])
        self.config["Machine"]["P_output"] = str(self.P_machine[3])
        self.config["Machine"]["T_motor"] = str(self.T_machine[0])
        self.config["Machine"]["T_highspeed"] = str(self.T_machine[1])
        self.config["Machine"]["T_lowspeed"] = str(self.T_machine[2])
        self.config["Machine"]["T_output"] = str(self.T_machine[3])

        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)

    def cal_motor(self):
        # 计算电机理论功率及转速
        self.P_work = self.F_belt * self.V_belt / 1000
        self.P_output = self.P_work / self.efficiency_total
        self.n_work = (60000 * self.V_belt) / (pi * self.D_roller)
        print("以下是电动机部分")
        print("----------------------------------------------------")
        print("·初步计算得电机理论参数:")
        print("  工作机所需功率P_w = %.2f" % self.P_work, "kW")
        print("  电机输出功率P_d = %.2f" % self.P_output, "kW")
        print("  根据《机械设计课程设计》得理论传动比范围荐用范围为 0 ~ 24")
        print("  电机理论所需转速范围为0 ~ %.2f" % (self.n_work * 24), "r/min")


def electric_motor_start():
    local_class = electric_motor_compress()
    # 程序运行
    local_class.cal_motor()
    local_class.motor_scan()
    local_class.output_MotorAbout()
    # 返回输出状态
    sys.stdout = local_class.output_tmp
    local_class.output_tmp.close()


if __name__ == "__main__":
    electric_motor_start()
