import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi


class belt_compress:

    def __init__(self):
        # 导入config
        self.config = cp.ConfigParser()
        self.config.read("./config.ini")

        # 数据记录
        self.K_A = float(self.config["Belt"]["K_A"])
        self.efficiency_belt = float(self.config["General"]["efficiency_belt"])
        self.efficiency_bearing = float(self.config["General"]["efficiency_bearing"])
        self.efficiency_gear = float(self.config["General"]["efficiency_gear"])
        self.efficiency_coupling = float(self.config["General"]["efficiency_coupling"])
        self.efficiency_roller = float(self.config["General"]["efficiency_roller"])
        self.n_motor = float(self.config["Machine"]["n_motor"])
        self.n_highspeed = float(self.config["Machine"]["n_highspeed"])
        self.n_lowspeed = float(self.config["Machine"]["n_lowspeed"])
        self.n_output = float(self.config["Machine"]["n_output"])
        self.P_motor = float(self.config["Machine"]["P_motor"])
        self.P_highspeed = float(self.config["Machine"]["P_highspeed"])
        self.P_lowspeed = float(self.config["Machine"]["P_lowspeed"])
        self.P_output = float(self.config["Machine"]["P_output"])
        self.T_motor = float(self.config["Machine"]["T_motor"])
        self.T_highspeed = float(self.config["Machine"]["T_highspeed"])
        self.T_lowspeed = float(self.config["Machine"]["T_lowspeed"])
        self.T_output = float(self.config["Machine"]["T_output"])
        self.i_total = float(self.config["Machine"]["i_total"])
        self.i_belt = float(self.config["Machine"]["i_belt"])
        self.i_gear = float(self.config["Machine"]["i_gear"])
        self.belt_type = 'A'  # 带型
        self.P_design = 0.0  # 设计功率
        self.P_single_belt = 0.0  # 单个带额定传输功率
        self.delta_P = 0.0  # 额定功率增量
        self.K_len = 0.0  # 长度修正系数
        self.K_alpha = 0.0  # 包角修正系数
        self.d_small = 0.0  # 小带轮直径
        self.d_large = 0.0  # 大带轮直径
        self.alpha_small = 0.0  # 小带轮包角
        self.alpha_large = 0.0  # 大带轮包角
        self.center_distance = 0.0  # 带轮中心距
        self.belt_base_len = 0.0  # 带轮基准长度
        self.belt_sum = 0.0  # 带数
        self.mass_per_unit = 0.0  # 带单位长度质量
        self.belt_speed = 0.0  # 带速
        self.F_pull_0 = 0.0  # 每根带初拉力
        self.F_Q = 0.0  # 轴上载荷
        self.d_small_wheel_shaft = 0.0  # 小带轮设计轴孔径
        self.d_large_wheel_shaft = 0.0  # 大带轮设计轴孔径
        self.L_small_wheel = 0.0  # 小带轮设计轮毂宽
        self.L_large_wheel = 0.0  # 大带轮设计轴孔宽

        # 导入额定功率数据
        belt_P_scheduled = pd.read_excel('./all_sheets/belt_P_scheduled.xls', sheet_name="Sheet1")
        train_data = np.array(belt_P_scheduled)
        self.belt_P_scheduled = train_data.tolist()
        # 导入额定功率增量数据
        belt_deltaP_scheduled = pd.read_excel('./all_sheets/belt_deltaP_scheduled.xls', sheet_name="Sheet1")
        train_data = np.array(belt_deltaP_scheduled)
        self.belt_deltaP_scheduled = train_data.tolist()
        # 导入包角修正系数数据
        Wrap_Angle_Correction = pd.read_excel('./all_sheets/Wrap_Angle_Correction.xls', sheet_name="Sheet1")
        train_data = np.array(Wrap_Angle_Correction)
        self.Wrap_Angle_Correction = train_data.tolist()
        # 导入带轮标准系列数据
        belt_wheel_designed = pd.read_excel('./all_sheets/belt_wheel_designed.xls', sheet_name="Sheet1")
        train_data = np.array(belt_wheel_designed)
        self.belt_wheel_designed = train_data.tolist()
        # 导入V带基准长度标准系列数据
        belt_length_list = pd.read_excel('./all_sheets/belt_length_list.xls', sheet_name="Sheet1")
        train_data = np.array(belt_length_list)
        self.belt_length_list = train_data.tolist()

        # 将数据输出到可视文件中
        output_file = open("./outputs/Calculated_Data_Belt.txt", mode='w+')
        self.output_tmp = sys.stdout
        sys.stdout = output_file

    def belt_type_choose(self):  # 选择V带型号
        # 取V带类型
        self.P_design = self.P_motor * self.K_A
        select_parameters = 506.7 * (self.P_design - 0.8) + 357.5
        # 因没有现成的运算函数，遂使用近似函数区分A带区与Z带区，但无法判定除此之外的其它带型
        if select_parameters > self.n_motor:
            self.belt_type = 'A'
        else:
            self.belt_type = 'Z'
        print("以下是V带传动部分")
        print("----------------------------------------------------")

    def data_update(self):  # 更新相关参数

        # 更新传动比
        self.i_belt = self.d_large / self.d_small
        self.i_gear = self.i_total / self.i_belt

        # 更新转速
        self.n_highspeed = self.n_motor / self.i_belt
        self.n_lowspeed = self.n_output = self.n_highspeed / self.i_gear

        # 更新转矩
        self.T_highspeed = 9550 * self.P_highspeed / self.n_highspeed
        self.T_lowspeed = 9550 * self.P_lowspeed / self.n_lowspeed
        self.T_output = 9550 * self.P_output / self.n_output

    def belt_wheel_choose(self):  # 选择带轮直径
        # 取小带轮直径，参考标准系列，不同于课本，直接使用额定功率表各带型的界定范围参考，毕竟没函数
        for i in range(len(self.belt_P_scheduled)):

            if self.belt_P_scheduled[i][0] != self.belt_type:
                continue
            record = 0
            for stp in range(5):
                if self.belt_P_scheduled[i + stp][1] * pi * self.n_motor / 60000.0 < 5:
                    continue
                if self.belt_P_scheduled[i + stp][1] * pi * self.n_motor / 60000.0 > 20:
                    break
                self.d_small = self.belt_P_scheduled[i + stp][1]
                record = stp
            # 顺便取一下单根V带额定功率
            delta = self.n_motor
            last = delta
            for j in range(2, len(self.belt_P_scheduled[0])):
                delta = abs(self.n_motor - self.belt_P_scheduled[0][j])
                if delta > last:
                    break
                self.P_single_belt = self.belt_P_scheduled[i + record][j]
                last = delta
            break

        # 取大带轮直径，参考标准系列
        last = 0.0
        targeting = 0.0
        self.d_large = self.d_small * self.i_belt
        for i in self.belt_wheel_designed:
            for j in i:
                last = targeting
                targeting = j
                # 保证带轮传动比不大于齿轮组的同时寻找合适尺寸
                if targeting >= self.d_large or (
                        (targeting / self.d_small) > self.i_total / (targeting / self.d_small)):
                    break
            if targeting >= self.d_large:
                break

        # 取更接近的值用作带轮
        mid = (last + targeting) / 2
        if self.d_large >= mid:
            self.d_large = targeting
        else:
            self.d_large = last

        # 第一轮更新数据
        self.data_update()

        print("·确定V带带轮直径")
        print("  初定带型号为: %s型" % self.belt_type)
        print("  对应小/大带轮直径为: %.0f / %.0f" % (self.d_small, self.d_large))
        print("  带轮传动比修正为: %.2f" % self.i_belt)
        print("  相关其它数据已完成修正")

    def base_length_design(self):  # 选择V带基准长度
        # 初定中心距及带基准长度
        center_distance_0 = 1.3 * (self.d_small + self.d_large)
        belt_base_len_0 = 2 * self.center_distance + pi * (self.d_small + self.d_large) / 2 + (
                    (self.d_large - self.d_small) ** 2) / (
                                  4 * center_distance_0)

        # 由表取标准值进行更正
        row = 4 if self.belt_type == 'A' else 2
        delta = belt_base_len_0
        for i in range(1, len(self.belt_length_list[row])):
            if abs(self.belt_length_list[row][i] - self.belt_base_len) < delta:
                delta = belt_base_len_0 - self.belt_base_len
                self.belt_base_len = self.belt_length_list[row][i]
                self.K_len = self.belt_length_list[row + 1][i]
            else:
                break

        # 确定中心距及小带轮包角
        self.center_distance = center_distance_0 + (self.belt_base_len - belt_base_len_0) / 2
        self.alpha_small = 180 - 57.3 * (self.d_large - self.d_small) / self.center_distance

        print("·确定中心距及V带基准长度")
        print("  根据0.7(d_d1 + d_d2) <= a_0 <= 2(d_d1 + d_d2), 初定中心距为: %.2f" % center_distance_0)
        print("  初定V带基准长度: %.2f" % belt_base_len_0)
        print("  由标准值确定V带基准长度为: %.2f" % self.belt_base_len)
        print("  再确定中心距为: %.2f" % self.center_distance)
        print("  小带轮包角计算为: %.2f°" % self.alpha_small)

    def belt_count(self):  # 计算带数
        # 选用额定功率增量
        for i in range(1, len(self.belt_deltaP_scheduled)):
            if self.belt_deltaP_scheduled[i][0] == self.belt_type:
                # 按传动比算范围
                target_i = 0
                for j in range(0, 3):
                    if self.i_belt >= self.belt_deltaP_scheduled[i + j][1]:
                        target_i = j
                # 按转速选列
                target_n = 2
                delta = self.n_motor
                last = delta
                for j in range(2, len(self.belt_deltaP_scheduled[0])):
                    delta = abs(self.n_motor - self.belt_deltaP_scheduled[0][j])
                    if delta > last: break
                    last = delta
                    target_n = j
                self.delta_P = self.belt_deltaP_scheduled[i + target_i][target_n]
                break

        # 取包角修正系数
        delta = self.alpha_small
        last = delta
        self.K_alpha = self.Wrap_Angle_Correction[1][0]
        for i in range(19):
            delta = abs(self.alpha_small - self.Wrap_Angle_Correction[0][i])
            if delta > last: break
            last = delta
            self.K_alpha = self.Wrap_Angle_Correction[1][i]

        # 计算V带总数
        self.belt_sum = np.ceil(self.P_design / ((self.P_single_belt + self.delta_P) * self.K_alpha * self.K_len))

        print("·确定V带根数")
        print("  由先前运算结果取得单根V带额定功率为: %.2f kW" % self.P_single_belt)
        print("  取得额定功率增量为: %.2f kW" % self.delta_P)
        print("  取得包角修正系数为: %.2f" % self.K_alpha)
        print("  取得带长修正系数为: %.2f" % self.K_len)
        print("  计算得V带根数为: %d" % self.belt_sum)

    def aft_design(self):  # 计算其它部件参数
        # 单位长度质量
        if self.belt_type == 'A': self.mass_per_unit = 0.10
        if self.belt_type == 'Z': self.mass_per_unit = 0.06

        # 带速及轴上载荷
        self.belt_speed = pi * self.d_small * self.n_motor / 60000
        self.F_pull_0 = 500 * self.P_design / (self.belt_sum * self.belt_speed) * (
                    2.5 / self.K_alpha - 1) + self.mass_per_unit * (self.belt_speed ** 2)
        self.F_Q = 2 * self.F_pull_0 * self.belt_sum * np.sin(np.radians(self.alpha_small) / 2)

        # 初定轴孔径及轮毂宽度
        self.d_small_wheel_shaft = 110 * np.cbrt(self.P_motor / self.n_motor) * 1.03
        self.d_large_wheel_shaft = 110 * np.cbrt(self.P_highspeed / self.n_highspeed) * 1.03

        print("·结构设计计算")
        print("  V带单位长度质量查表得为: %.2f" % self.mass_per_unit)
        print("  单根带所受初拉力为: %.2f N" % self.F_pull_0)
        print("  轴上载荷为: %.2f N" % self.F_Q)
        print("  以45钢为轴用材料，开单键槽")
        print("  根据圆截面轴的扭转强度条件，初定小带轮轴的计算直径为: %.2f" % self.d_small_wheel_shaft)
        print("  大带轮轴的计算直径为: %.2f" % self.d_large_wheel_shaft)

        # 根据标准尺寸系列选直径，常用的40以内有规律可循
        tag1 = tag2 = 0
        for i in range(10, 26):
            if i > self.d_small_wheel_shaft and tag1 == 0:
                self.d_small_wheel_shaft = i
                tag1 = 1
            if i > self.d_large_wheel_shaft and tag2 == 0:
                self.d_large_wheel_shaft = i
                tag2 = 1
        for i in range(26, 41, 2):
            if i > self.d_small_wheel_shaft and tag1 == 0:
                self.d_small_wheel_shaft = i
                tag1 = 1
            if i > self.d_large_wheel_shaft and tag2 == 0:
                self.d_large_wheel_shaft = i
                tag2 = 1
        self.L_small_wheel = np.ceil(1.7 * self.d_small_wheel_shaft)
        self.L_large_wheel = np.ceil(1.7 * self.d_large_wheel_shaft)

        print("  根据圆截面轴的标准尺寸，暂定小带轮轴的直径为: %.2f" % self.d_small_wheel_shaft)
        print("  大带轮轴的直径为: %.2f" % self.d_large_wheel_shaft)
        print("  故根据《机械设计课程设计》，轮毂宽度荐用值取1.5~2倍轴孔宽度，则:")
        print("  小带轮轮毂的宽度为: %.2f" % self.L_small_wheel)
        print("  大带轮轮毂的宽度为: %.2f" % self.L_large_wheel)
        print("-------------------带轮运算已结束--------------------")

    def output_BeltAbout(self):
        self.config["Belt"]["belt_type"] = self.belt_type
        self.config["Belt"]["P_design"] = str(self.P_design)
        self.config["Belt"]["P_single_belt"] = str(self.P_single_belt)
        self.config["Belt"]["delta_P"] = str(self.delta_P)
        self.config["Belt"]["K_len"] = str(self.K_len)
        self.config["Belt"]["K_alpha"] = str(self.K_alpha)
        self.config["Belt"]["d_small"] = str(self.d_small)
        self.config["Belt"]["d_large"] = str(self.d_large)
        self.config["Belt"]["alpha_small"] = str(self.alpha_small)
        self.config["Belt"]["alpha_large"] = str(self.alpha_large)
        self.config["Belt"]["center_distance"] = str(self.center_distance)
        self.config["Belt"]["belt_base_len"] = str(self.belt_base_len)
        self.config["Belt"]["belt_sum"] = str(self.belt_sum)
        self.config["Belt"]["mass_per_unit"] = str(self.mass_per_unit)
        self.config["Belt"]["belt_speed"] = str(self.belt_speed)
        self.config["Belt"]["F_pull_0"] = str(self.F_pull_0)
        self.config["Belt"]["F_Q"] = str(self.F_Q)
        self.config["Belt"]["d_small_wheel_shaft"] = str(self.d_small_wheel_shaft)
        self.config["Belt"]["d_large_wheel_shaft"] = str(self.d_large_wheel_shaft)
        self.config["Belt"]["L_small_wheel"] = str(self.L_small_wheel)
        self.config["Belt"]["L_large_wheel"] = str(self.L_large_wheel)

        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)


def belt_start():
    local_class = belt_compress()
    # 程序运行
    local_class.belt_type_choose()
    local_class.belt_wheel_choose()
    local_class.base_length_design()
    local_class.belt_count()
    local_class.aft_design()
    local_class.output_BeltAbout()
    # 返回输出状态
    sys.stdout = local_class.output_tmp
    local_class.output_tmp.close()


if __name__ == "__main__":
    belt_start()
