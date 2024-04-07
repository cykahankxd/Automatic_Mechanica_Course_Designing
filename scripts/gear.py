import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi


class gear_compress:
    def __init__(self):
        # 导入config
        self.config = cp.ConfigParser()
        self.config.read("./config.ini")
        # 数据记录
        self.highspeed_gear_material = self.config["Gear"]["highspeed_gear_material"]
        self.lowspeed_gear_material = self.config["Gear"]["lowspeed_gear_material"]
        self.d_gear_shaft_high = float(self.config["Belt"]["d_large_wheel_shaft"])  # 高速轴直径
        self.n_highspeed = float(self.config["Machine"]["n_highspeed"])
        self.p_highspeed = float(self.config["Machine"]["p_highspeed"])
        self.t_highspeed = float(self.config["Machine"]["t_highspeed"]) * 10000
        self.i_gear = float(self.config["Machine"]["i_gear"])
        self.p_lowspeed = float(self.config["Machine"]["p_lowspeed"])
        self.n_lowspeed = float(self.config["Machine"]["n_lowspeed"])
        self.t_lowspeed = float(self.config["Machine"]["t_lowspeed"])
        self.p_output = float(self.config["Machine"]["p_output"])
        self.n_output = float(self.config["Machine"]["n_output"])
        self.t_output = float(self.config["Machine"]["t_output"])
        self.efficiency_bearing = float(self.config["General"]["efficiency_bearing"])
        self.efficiency_gear = float(self.config["General"]["efficiency_gear"])
        self.efficiency_coupling = float(self.config["General"]["efficiency_coupling"])
        self.efficiency_roller = float(self.config["General"]["efficiency_roller"])
        self.stress_limit_high = 0.0  # 小齿轮极限接触应力
        self.stress_limit_low = 0.0  # 大齿轮极限接触应力
        self.stress_allowable_high = 0.0  # 小齿轮许用接触应力
        self.stress_allowable_low = 0.0  # 大齿轮许用接触应力
        self.stress_limit_high_flim = 0.0  # 小齿轮极限弯曲应力
        self.stress_limit_low_flim = 0.0  # 小齿轮极限弯曲应力
        self.stress_allowable_high_flim = 0.0  # 小齿轮许用弯曲应力
        self.stress_allowable_low_flim = 0.0  # 大齿轮许用弯曲应力
        self.hardness_high = 0.0  # 小齿轮平均硬度
        self.hardness_low = 0.0  # 大齿轮平均硬度
        self.d_highspeed = 0.0  # 小齿轮分度圆直径
        self.d_lowspeed = 0.0  # 大齿轮分度圆直径
        self.z_highspeed = 0.0  # 小齿轮齿数
        self.z_lowspeed = 0.0  # 大齿轮齿数
        self.m = 0.0  # 模数
        self.center_distance = 0.0  # 中心距
        self.b_highspeed = 0.0  # 小齿轮齿宽
        self.b_lowspeed = 0.0  # 小齿轮齿宽
        self.addendum_h_factor = 1  # 齿顶高系数
        self.bottom_c_factor = 0.25  # 顶隙系数
        self.alpha = 20  # 齿形角
        self.addendum_height = 0.0  # 齿顶高
        self.bottom_clearance = 0.0  # 顶隙
        self.height = 0.0  # 齿高
        self.base_circle_d_high = 0.0  # 小齿轮齿根圆直径
        self.base_circle_d_low = 0.0  # 大齿轮齿根圆直径
        self.addendum_circle_d_high = 0.0  # 小齿轮齿顶圆直径
        self.addendum_circle_d_low = 0.0  # 大齿轮齿顶圆直径
        self.root_d_high = 0.0  # 小齿轮齿根圆直径
        self.root_d_low = 0.0  # 大齿轮齿根圆直径
        self.pitch = 0.0  # 锥距
        self.tooth_thickness = 0.0  # 齿宽
        self.spacewidth = 0.0
        self.d_gear_shaft_low = 0.0  # 低速轴直径

        # 导入标准模数
        gear_standard_modulus = pd.read_excel('./all_sheets/gear_standard_modulus.xls', sheet_name="Sheet1")
        train_data = np.array(gear_standard_modulus)
        self.gear_standard_modulus = train_data.tolist()
        # 导入标准模数
        compound_form_factor = pd.read_excel('./all_sheets/compound_form_factor.xls', sheet_name="Sheet1")
        train_data = np.array(compound_form_factor)
        self.compound_form_factor = train_data.tolist()

        # 将数据输出到可视文件中
        output_file = open("./outputs/Calculated_Data_Gear.txt", mode='w+')
        self.output_tmp = sys.stdout
        sys.stdout = output_file

    def stress_cal(self):  # 许用接触应力的计算

        # 先取各齿轮材料平均硬度，一般比较不容易出错的是45号钢的各种形态
        if self.highspeed_gear_material == "45 quenched and tempered":  # 高速轮（小齿轮，硬度要求偏高）
            self.hardness_high = 240
        elif self.highspeed_gear_material == "45 normalizing":
            self.hardness_high = 200
        if self.lowspeed_gear_material == "45 quenched and tempered":  # 低速轮（大齿轮，硬度要求偏低）
            self.hardness_low = 240
        elif self.lowspeed_gear_material == "45 normalizing":
            self.hardness_low = 200

        # 再计算极限接触应力
        if self.highspeed_gear_material.find("45") != -1:
            self.stress_limit_high = np.ceil(self.hardness_high * 0.87 + 380)
        if self.lowspeed_gear_material.find("45") != -1:
            self.stress_limit_low = np.ceil(self.hardness_low * 0.87 + 380)

        # 计算许用接触应力
        safety_factor = 1  # 取理想值
        self.stress_allowable_low = self.stress_limit_low / safety_factor
        self.stress_allowable_high = self.stress_limit_high / safety_factor

        print("以下是减速齿轮组部分")
        print("----------------------------------------------------")
        print("·按齿面解除疲劳强度设计")
        print("·计算接触应力")
        print("  计算极限应力得小齿轮极限应力: %d" % self.stress_limit_low, "MPa")
        print("  大齿轮极限应力: %d" % self.stress_limit_high, "MPa")
        print("  依工作情况取安全系数S_H = %d" % safety_factor)
        print("  计算许用接触应力得小齿轮许用接触应力: %d" % self.stress_allowable_low, "MPa")
        print("  大齿轮许用接触应力: %d" % self.stress_allowable_high, "MPa")

    def size_deisgn(self):  # 确定几何尺寸

        thickness_factor = 1  # 齿宽系数
        load_factor = 1.4  # 载荷系数
        Z_H = 2.5  # 节点区域系数
        Z_E = 189.8  # 弹性系数

        # 齿轮计算直径
        self.d_highspeed = np.cbrt(
            pow((Z_E * Z_H / self.stress_allowable_high), 2) * 2 * load_factor * self.t_highspeed / thickness_factor
            * (self.i_gear + 1) / self.i_gear)

        print("·计算并设计齿轮的几何尺寸")
        print("  单级减速器中齿轮相对轴承对称布置，由《机械设计基础》P117 表7-7取齿宽系数: %d" % thickness_factor)
        print("  工作平稳，软齿面齿轮，取载荷系数: %.2f" % load_factor)
        print("  标准直齿圆柱传动，取节点区域系数: %.2f" % Z_H)
        print("  钢制齿轮，取弹性系数: %.2f" % Z_E)
        print("  由是，得小齿轮计算直径为: %.2f" % self.d_highspeed)

        # 确定几何尺寸
        # 取齿数
        self.z_highspeed = 25
        self.z_lowspeed = np.ceil(self.i_gear * self.z_highspeed)
        self.m = self.d_highspeed / self.z_highspeed
        # 传动比修正
        self.i_gear = self.z_lowspeed / self.z_highspeed

        # 取标准模数
        target1_m = self.gear_standard_modulus[0][0]
        target2_m = self.gear_standard_modulus[1][0]
        # 为了保险同取两个标准序列
        for series in self.gear_standard_modulus[0]:
            target1_m = series
            if series > self.m:
                break
        for series in self.gear_standard_modulus[1]:
            target2_m = series
            if series > self.m:
                break
        self.m = target1_m if abs(target1_m - self.m) < abs(target2_m - self.m) else target2_m

        # 第二次修正
        self.d_highspeed = self.m * self.z_highspeed
        self.d_lowspeed = self.m * self.z_lowspeed
        self.center_distance = (self.d_lowspeed + self.d_highspeed) / 2

        # 齿宽
        self.b_lowspeed = np.ceil(thickness_factor * self.d_highspeed)
        self.b_highspeed = np.ceil(self.b_lowspeed / 10) * 10 if np.ceil(self.b_lowspeed / 10) * 10 - self.b_lowspeed >= 5 <= 10 else (
            np.ceil(self.b_lowspeed / 5 + 1) * 5 if np.ceil(self.b_lowspeed / 5 + 1) * 5 - self.b_lowspeed >= 5 <= 10
            else np.ceil(self.b_lowspeed / 5) * 5)

        print("  取大/小齿轮齿数分别为: %d / %d" % (self.z_lowspeed, self.z_highspeed))
        print("  修正传动比值为: %.2f" % self.i_gear)
        print("  取模数标准值为: %.3f" % self.m)
        print("  修正分度圆直径得大/小齿轮分度圆直径分别为: %.3f / %.3f" % (self.d_lowspeed, self.d_highspeed), "mm")
        print("  中心距为: %.3f" % self.center_distance)
        print("  大/小齿轮齿宽分别为: %d / %d" % (self.b_lowspeed, self.b_highspeed))

    def Strength_Check(self):

        load_factor = 1.4  # 载荷系数
        safety_factor = 1.4  # 安全系数

        # 计算极限弯曲应力
        if self.highspeed_gear_material.find("45") != -1:
            self.stress_limit_high_flim = 0.7 * self.hardness_high + 275
        if self.lowspeed_gear_material.find("45") != -1:
            self.stress_limit_low_flim = 0.7 * self.hardness_low + 275

        # 计算许用齿根应力
        self.stress_allowable_high_flim = self.stress_limit_high_flim / safety_factor
        self.stress_allowable_low_flim = self.stress_limit_low_flim / safety_factor

        # 验算齿根应力
        form_factor_highspeed = self.compound_form_factor[1][0]  # 小齿轮复合齿形系数
        form_factor_lowspeed = self.compound_form_factor[1][0]  # 小齿轮复合齿形系数

        # 线性插值（你最好是）求复合齿形系数
        for i in range(1, len(self.compound_form_factor[0]) - 1):
            form_factor_highspeed = self.compound_form_factor[1][i]
            if self.compound_form_factor[0][i] > self.z_highspeed:
                form_factor_highspeed = self.compound_form_factor[1][i] if abs(
                    self.z_highspeed - self.compound_form_factor[0][i]) < abs(
                    self.z_highspeed - self.compound_form_factor[0][i - 1]) else self.compound_form_factor[1][i - 1]
                break
        if self.z_highspeed > 250:  # inf修正
            form_factor_highspeed = self.compound_form_factor[1][len(self.compound_form_factor[0] - 1)]

        for i in range(1, len(self.compound_form_factor[0]) - 1):
            form_factor_lowspeed = self.compound_form_factor[1][i]
            if self.compound_form_factor[0][i] > self.z_lowspeed:
                form_factor_lowspeed = self.compound_form_factor[1][i] if abs(self.z_lowspeed - self.compound_form_factor[0][i]) < abs(
                    self.z_lowspeed - self.compound_form_factor[0][i - 1]) else self.compound_form_factor[1][i - 1]
                break
        if self.z_lowspeed > 250:  # inf修正
            form_factor_lowspeed = self.compound_form_factor[1][len(self.compound_form_factor[0] - 1)]

        # 齿根应力
        stress_high_flim = 2 * load_factor * self.t_highspeed * form_factor_highspeed / (
                    self.b_lowspeed * self.d_highspeed * self.m)
        stress_low_flim = stress_high_flim * form_factor_lowspeed / form_factor_highspeed

        print("·校核齿根弯曲疲劳强度")
        print("  计算大/小齿轮齿根极限应力为: %.2f / %.2f" % (self.stress_limit_low_flim, self.stress_limit_high_flim), "MPa")
        print("  取安全系数为: %.1f" % safety_factor)
        print("  计算大/小齿轮许用齿根应力为: %.2f / %.2f" % (self.stress_allowable_low_flim, self.stress_allowable_high_flim), "MPa")
        print("  大/小齿轮复合齿形系数由教材P116 表7-6得为: %.2f / %.2f" % (form_factor_lowspeed, form_factor_highspeed))
        print("  大齿轮齿根应力计算为: %.2f" % stress_low_flim,
              "MPa, " + ("符合标准" if stress_low_flim < self.stress_allowable_low_flim
                         else "不符合标准"))
        print("  小齿轮齿根应力计算为: %.2f" % stress_high_flim,
              "MPa, " + ("符合标准" if stress_high_flim < self.stress_allowable_high_flim
                         else "不符合标准"))

    def gear_design(self):
        self.addendum_height = self.addendum_h_factor * self.m  # 齿顶高
        self.bottom_clearance = self.bottom_c_factor * self.m  # 顶隙
        dedendum = self.bottom_clearance + self.addendum_height  # 齿根高
        self.height = self.addendum_height + dedendum  # 齿高

        self.base_circle_d_high = self.d_highspeed * np.cos(np.radians(self.alpha))  # 小齿轮基圆直径
        self.base_circle_d_low = self.d_lowspeed * np.cos(np.radians(self.alpha))  # 大齿轮基圆直径
        self.addendum_circle_d_high = self.d_highspeed + 2 * self.addendum_height  # 小齿轮齿顶圆直径
        self.addendum_circle_d_low = self.d_lowspeed + 2 * self.addendum_height  # 大齿轮齿顶圆直径
        self.root_d_high = self.d_highspeed - 2 * dedendum  # 小齿轮齿根圆直径
        self.root_d_low = self.d_lowspeed - 2 * dedendum  # 大齿轮齿根圆直径
        self.pitch = pi * self.m  # 齿距
        self.tooth_thickness = self.spacewidth = self.pitch / 2  # 标准齿厚/齿槽宽

        # 三次修正传动数据
        self.t_highspeed /= 10000
        self.n_lowspeed = self.n_output = self.n_highspeed / self.i_gear
        self.t_lowspeed = 9550 * self.p_lowspeed / self.n_lowspeed
        self.t_output = 9550 * self.p_output / self.n_output

        # 轴设计
        self.d_gear_shaft_high += 12
        tag2 = 0
        self.d_gear_shaft_low = 110 * np.cbrt(self.p_lowspeed / self.n_lowspeed) * 1.03
        for i in range(10, 26):
            if i > self.d_gear_shaft_low and tag2 == 0:
                self.d_gear_shaft_low = i
                tag2 = 1
        for i in range(26, 41, 2):
            if i > self.d_gear_shaft_low and tag2 == 0:
                self.d_gear_shaft_low = i
                tag2 = 1
        self.d_gear_shaft_low += 12

        print("·齿轮整体结构设计")
        print("  综上，得齿轮整体结构如下:")
        print("  齿顶高为: %.2f" % self.addendum_height)
        print("  顶隙: %.2f" % self.bottom_clearance)
        print("  齿根高为: %.2f" % dedendum)
        print("  齿高为: %.2f" % self.height)
        print("  大/小齿轮分度圆直径分别为: %.2f / %.2f" % (self.d_lowspeed, self.d_highspeed))
        print("  大/小齿轮基圆直径分别为: %.2f / %.2f" % (self.base_circle_d_low, self.base_circle_d_high))
        print("  大/小齿轮齿宽为: %.2f / %.2f" % (self.b_lowspeed, self.b_highspeed))
        print("  大/小齿轮齿顶圆直径为: %.2f / %.2f" % (self.addendum_circle_d_low, self.addendum_circle_d_high))
        print("  大/小齿轮齿根圆直径为: %.2f / %.2f" % (self.root_d_low, self.root_d_high))
        print("  大/小齿轮初定轴孔径为: %.2f / %.2f" % (self.d_gear_shaft_low, self.d_gear_shaft_high))
        print("------------------减速齿轮运算已结束-------------------")

    def output_GearAbout(self):
        self.config["Gear"]["d_highspeed"] = str(self.d_highspeed)
        self.config["Gear"]["d_lowspeed"] = str(self.d_lowspeed)
        self.config["Gear"]["b_highspeed"] = str(self.b_highspeed)
        self.config["Gear"]["b_lowspeed"] = str(self.b_lowspeed)
        self.config["Gear"]["z_highspeed"] = str(self.z_highspeed)
        self.config["Gear"]["z_lowspeed"] = str(self.z_lowspeed)
        self.config["Gear"]["m"] = str(self.m)
        self.config["Gear"]["center_distance"] = str(self.center_distance)
        self.config["Gear"]["addendum_height"] = str(self.addendum_height)
        self.config["Gear"]["bottom_clearance"] = str(self.bottom_clearance)
        self.config["Gear"]["height"] = str(self.height)
        self.config["Gear"]["base_circle_d_high"] = str(self.base_circle_d_high)
        self.config["Gear"]["base_circle_d_low"] = str(self.base_circle_d_low)
        self.config["Gear"]["addendum_circle_d_high"] = str(self.addendum_circle_d_high)
        self.config["Gear"]["addendum_circle_d_low"] = str(self.addendum_circle_d_low)
        self.config["Gear"]["root_d_high"] = str(self.root_d_high)
        self.config["Gear"]["root_d_low"] = str(self.root_d_low)
        self.config["Gear"]["pitch"] = str(self.pitch)
        self.config["Gear"]["tooth_thickness"] = str(self.tooth_thickness)
        self.config["Gear"]["spacewidth"] = str(self.spacewidth)
        self.config["Gear"]["d_gear_shaft_low"] = str(self.d_gear_shaft_low)
        self.config["Gear"]["d_gear_shaft_high"] = str(self.d_gear_shaft_high)

        self.config["Machine"]["t_output"] = str(self.t_output)
        self.config["Machine"]["t_lowspeed"] = str(self.t_lowspeed)
        self.config["Machine"]["n_lowspeed"] = str(self.n_lowspeed)
        self.config["Machine"]["n_output"] = str(self.n_output)

        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)


def gear_start():
    local_class = gear_compress()
    # 程序运行
    local_class.stress_cal()
    local_class.size_deisgn()
    local_class.Strength_Check()
    local_class.gear_design()
    local_class.output_GearAbout()
    # 返回输出状态
    sys.stdout = local_class.output_tmp
    local_class.output_tmp.close()


if __name__ == "__main__":
    gear_start()
