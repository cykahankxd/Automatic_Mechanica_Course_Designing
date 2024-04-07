import configparser as cp
import pandas as pd
import numpy as np
import sys


class shaft_compress:

    def __init__(self):
        # 导入config
        self.config = cp.ConfigParser()
        self.config.read("./config.ini")

        # 数据记录
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
        self.length_2 = float(self.config["Machine"]["length_2"])
        self.bearing_cover_bolt_d = float(self.config["Machine"]["bearing_cover_bolt_d"])  # 轴承盖直径
        self.base_rib_thickness = float(self.config["Machine"]["base_rib_thickness"])  # 机座壁厚
        self.delta_2 = float(self.config["Machine"]["delta_2"])
        self.d_gear_highspeed = float(self.config["Gear"]["d_highspeed"])
        self.d_gear_lowspeed = float(self.config["Gear"]["d_lowspeed"])
        self.d_gear_shaft_low = float(self.config["Gear"]["d_gear_shaft_low"])
        self.d_gear_shaft_high = float(self.config["Gear"]["d_gear_shaft_high"])
        self.b_gear_highspeed = float(self.config["Gear"]["b_highspeed"])
        self.b_gear_lowspeed = float(self.config["Gear"]["b_lowspeed"])
        self.l_large_wheel = float(self.config["Belt"]["l_large_wheel"])
        self.high_shaft_cal_d = 0.0  # 高速轴计算直径
        self.low_shaft_cal_d = 0.0  # 低速轴计算直径
        self.high_shaft_design_d = 0.0  # 高速轴设计直径
        self.low_shaft_design_d = 0.0  # 低速轴设计直径
        self.high_shaft_standard_d = 0.0  # 高速轴标准直径
        self.low_shaft_standard_d = 0.0  # 低速轴标准直径
        self.alpha = 20
        self.d_high_1 = 0.0  # 高速轴各段直径
        self.d_high_2 = 0.0
        self.d_high_3 = 0.0
        self.d_high_4 = 0.0
        self.d_high_5 = 0.0
        self.d_high_6 = 0.0
        self.len_high_1 = 0.0  # 高速轴各段长度
        self.len_high_2 = 0.0
        self.len_high_3 = 0.0
        self.len_high_4 = 0.0
        self.len_high_5 = 0.0
        self.len_high_6 = 0.0
        self.d_low_1 = 0.0  # 低速轴各段直径
        self.d_low_2 = 0.0
        self.d_low_3 = 0.0
        self.d_low_4 = 0.0
        self.d_low_5 = 0.0
        self.d_low_6 = 0.0
        self.len_low_1 = 0.0  # 低速轴各段长度
        self.len_low_2 = 0.0
        self.len_low_3 = 0.0
        self.len_low_4 = 0.0
        self.len_low_5 = 0.0
        self.len_low_6 = 0.0
        self.bearing_ID_high = ""
        self.bearing_ID_low = ""
        self.coupling_type_low = ""  # 联轴器数据
        self.coupling_L_low = 0
        self.coupling_L1_low = 0
        self.bearing_high_D = 0.0  # 轴承外径
        self.bearing_low_D = 0.0
        self.bearing_high_T = 0.0  # 轴承厚度
        self.bearing_low_T = 0.0
        self.bearing_cover_high_D = 0.0  # 轴承端盖外径
        self.bearing_cover_low_D = 0.0

        # 导入标准六角头螺栓长度数据
        standard_bolt = pd.read_excel('./all_sheets/standard_bolt.xls', sheet_name="Sheet1")
        train_data = np.array(standard_bolt)
        self.standard_bolt = train_data.tolist()
        # 导入标准零尺寸系列深沟球轴承尺寸数据
        bearing_0_size_series = pd.read_excel('./all_sheets/bearing_0_size_series.xls', sheet_name="Sheet1")
        train_data = np.array(bearing_0_size_series)
        self.bearing_0_size_series = train_data.tolist()
        # 导入LX型弹性柱销联轴器尺寸数据
        coupling_standard = pd.read_excel('./all_sheets/coupling_standard.xls', sheet_name="Sheet1")
        train_data = np.array(coupling_standard)
        self.coupling_standard = train_data.tolist()

        # 将数据输出到可视文件中
        output_file = open("./outputs/Calculated_Data_Shaft.txt", mode='w+')
        self.output_tmp = sys.stdout
        sys.stdout = output_file

    def first_design(self):
        # 计入键槽影响，计算轴的计算直径
        self.high_shaft_cal_d = 110 * np.cbrt(self.P_highspeed / self.n_highspeed) * 1.03
        self.low_shaft_cal_d = 110 * np.cbrt(self.P_lowspeed / self.n_lowspeed) * 1.03

        # 以标准值确定轴的最小直径
        tag1 = tag2 = 0
        for i in range(10, 26):
            if i > self.high_shaft_cal_d and tag1 == 0:
                self.high_shaft_standard_d = i
                tag1 = 1
            if i > self.low_shaft_cal_d and tag2 == 0:
                self.low_shaft_standard_d = i
                tag2 = 1
        for i in range(26, 41, 2):
            if i > self.high_shaft_cal_d and tag1 == 0:
                self.high_shaft_standard_d = i
                tag1 = 1
            if i > self.low_shaft_cal_d and tag2 == 0:
                self.low_shaft_standard_d = i
                tag2 = 1

        print("以下是轴的实际大小计算部分")
        print("·预选轴用直径")
        print("  高速轴计入单键槽误差后计算最小直径为: %.2f" % self.high_shaft_cal_d)
        print("  取标准值为: %.1f" % self.high_shaft_standard_d)
        print("  低速轴计入单键槽误差后计算最小直径为: %.2f" % self.low_shaft_cal_d)
        print("  取标准值为: %.1f" % self.low_shaft_standard_d)

    def shaft_length_design(self):
        # 计算螺钉长度
        nail_len = 0.0
        for i in range(len(self.standard_bolt[0])):
            if self.bearing_cover_bolt_d == self.standard_bolt[0][i]:
                nail_len = self.standard_bolt[1][i] + self.standard_bolt[2][i]

        # 计算高速轴
        # 第一段
        self.len_high_1 = self.l_large_wheel - 2
        self.d_high_1 = self.high_shaft_standard_d
        # 第二段
        self.d_high_2 = self.d_high_1 + 4
        e = np.ceil(1.2 * self.bearing_cover_bolt_d)
        e = e if 5 <= e <= 8 else 8 if e > 8 else 5
        self.len_high_2 = self.base_rib_thickness + e + 2 + nail_len  # +2是预留调整垫片的空间

        # 高速轴轴承选用，顺带解决第三段和第六段直径问题
        self.d_high_3 = self.d_high_2
        for i in range(len(self.bearing_0_size_series)):
            if self.bearing_0_size_series[i][1] > self.d_high_3:
                self.d_high_3 = self.bearing_0_size_series[i][1]
                self.bearing_high_T = self.bearing_0_size_series[i][3]
                self.bearing_high_D = self.bearing_0_size_series[i][2]
                self.bearing_ID_high += str(self.bearing_0_size_series[i][0])
                break
        if self.bearing_ID_high == "":
            lastone = len(self.bearing_0_size_series) - 1
            self.d_high_3 = self.bearing_0_size_series[lastone][1]
            self.bearing_high_T = self.bearing_0_size_series[lastone][3]
            self.bearing_high_D = self.bearing_0_size_series[lastone][2]
            self.bearing_ID_high += str(self.bearing_0_size_series[lastone][0])
        self.d_high_6 = self.d_high_3
        # 顺带把轴承盖外径给解决了
        self.bearing_cover_high_D = self.bearing_high_D + 5 * self.bearing_cover_bolt_d

        # 第三段长度
        delta_3 = 10
        self.len_high_3 = self.delta_2 + delta_3 + self.bearing_high_T + 2
        # 第四段
        self.d_high_4 = self.d_high_3 + 4
        L_gear_high = self.b_gear_highspeed if self.d_high_4 <= self.b_gear_highspeed <= self.d_high_4 * 1.5 else \
            np.ceil(self.d_high_4 * 1.25)
        self.len_high_4 = L_gear_high - 2
        # 第五段
        a = np.ceil(0.075 * self.d_high_4 + 1)  # 轴环处轴肩大小
        self.d_high_5 = self.d_high_4 + 2 * a
        self.len_high_5 = np.ceil(a * 1.4)

        print("·高速轴计算")
        print("  根据标准GB/T 276-1994，经计算确定使用深沟球轴承编号为:", self.bearing_ID_high)
        print("    其内径为: %.2f" % self.d_high_3)
        print("    外径为: %.2f" % self.bearing_high_D)
        print("    厚度为: %.2f" % self.bearing_high_T)
        print("  根据轴承外径得高速轴轴承盖外径为: %.2f" % self.bearing_cover_high_D)
        print("  根据齿轮计算结果，得腹板式齿轮的轴实际参数:")
        print("    其轴/孔径理论值为: %.2f" % self.d_high_4)
        print("    孔长度为: %.2f , 根据《机械设计课程设计》, 轴长向内收缩2~3mm" % L_gear_high)
        print("  故得出高速轴各段数据如下:")
        print("  第一节直径: %.2f" % self.d_high_1)
        print("       长度: %.2f" % self.len_high_1)
        print("  第二节直径: %.2f" % self.d_high_2)
        print("       长度: %.2f" % self.len_high_2)
        print("  第三节直径: %.2f" % self.d_high_3)
        print("       长度: %.2f" % self.len_high_3)
        print("  第四节直径: %.2f" % self.d_high_4)
        print("       长度: %.2f" % self.len_high_4)
        print("  第五节(轴环)直径: %.2f" % self.d_high_5)
        print("       长度: %.2f" % self.len_high_5)
        print("  第六节直径: %.2f" % self.d_high_6)
        print("  (因第六节长度可直接作图得到，故省略)")

        # 低速轴同理

        # 计算所用联轴器
        for i in range(len(self.coupling_standard)):
            if self.coupling_standard[i][1] <= self.low_shaft_standard_d:
                self.coupling_type_low = self.coupling_standard[i][0]
                self.coupling_L_low = self.coupling_standard[i][2]
                self.coupling_L1_low = self.coupling_standard[i][3]
                break
        if self.coupling_type_low == "":
            lastone = len(self.coupling_standard[0]) - 1
            self.coupling_type_low = self.coupling_standard[lastone][0]
            self.coupling_L_low = self.coupling_standard[lastone][2]
            self.coupling_L1_low = self.coupling_standard[lastone][3]

        # 第一段
        self.len_low_1 = self.coupling_L1_low - 2
        self.d_low_1 = self.low_shaft_standard_d
        # 第二段
        self.d_low_2 = self.d_low_1 + 4
        e = np.ceil(1.2 * self.bearing_cover_bolt_d)
        e = e if 5 <= e <= 8 else 8 if e > 8 else 5
        self.len_low_2 = self.base_rib_thickness + e + 2 + nail_len

        # 低速轴轴承选用
        self.d_low_3 = self.d_low_2
        for i in range(len(self.bearing_0_size_series)):
            if self.bearing_0_size_series[i][1] > self.d_low_3:
                self.d_low_3 = self.bearing_0_size_series[i][1]
                self.bearing_low_T = self.bearing_0_size_series[i][3]
                self.bearing_low_D = self.bearing_0_size_series[i][2]
                self.bearing_ID_low += str(self.bearing_0_size_series[i][0])
                break
        if self.bearing_ID_low == "":
            lastone = len(self.bearing_0_size_series) - 1
            self.d_low_3 = self.bearing_0_size_series[lastone][1]
            self.bearing_low_T = self.bearing_0_size_series[lastone][3]
            self.bearing_low_D = self.bearing_0_size_series[lastone][2]
            self.bearing_ID_low += str(self.bearing_0_size_series[lastone][0])
        self.d_low_6 = self.d_low_3
        self.bearing_cover_low_D = self.bearing_low_D + 5 * self.bearing_cover_bolt_d

        # 第三段长度
        delta_3 = 10
        self.len_low_3 = self.delta_2 + delta_3 + self.bearing_low_T + 2
        # 第四段
        self.d_low_4 = self.d_low_3 + 4
        L_gear_low = self.b_gear_lowspeed if self.d_low_4 <= self.b_gear_lowspeed <= self.d_low_4 * 1.5 \
            else np.ceil(self.d_low_4 * 1.25)
        self.len_low_4 = L_gear_low - 2
        # 第五段
        a = np.ceil(0.075 * self.d_low_4 + 1)  # 轴环处轴肩大小
        self.d_low_5 = self.d_low_4 + 2 * a
        self.len_low_5 = np.ceil(a * 1.4)

        print("·低速轴计算")
        print("  根据标准GB/T 5014-2003，经计算确定使用LX型弹性柱销联轴器编号为:", self.coupling_type_low)
        print("    其内径为: %.2f" % self.d_low_1)
        print("    其轴孔长度/轴孔小径长度为: %.2f, %.2f" % (self.coupling_L_low, self.coupling_L1_low))
        print("    详细参数详见《机械设计课程设计》")
        print("  根据标准GB/T 276-1994，经计算确定使用深沟球轴承编号为:", self.bearing_ID_low)
        print("    其内径为: %.2f" % self.d_low_3)
        print("    外径为: %.2f" % self.bearing_low_D)
        print("    厚度为: %.2f" % self.bearing_low_T)
        print("  根据轴承外径得高速轴轴承盖外径为: %.2f" % self.bearing_cover_low_D)
        print("  根据齿轮计算结果，得腹板式齿轮的轴实际参数:")
        print("    其轴/孔径理论值为: %.2f" % self.d_low_4)
        print("    孔长度为: %.2f , 根据《机械设计课程设计》, 轴长向内收缩2~3mm" % L_gear_low)
        print("  故得出低速轴各段数据如下:")
        print("  第一节直径: %.2f" % self.d_low_1)
        print("       长度: %.2f" % self.len_low_1)
        print("  第二节直径: %.2f" % self.d_low_2)
        print("       长度: %.2f" % self.len_low_2)
        print("  第三节直径: %.2f" % self.d_low_3)
        print("       长度: %.2f" % self.len_low_3)
        print("  第四节直径: %.2f" % self.d_low_4)
        print("       长度: %.2f" % self.len_low_4)
        print("  第五节(轴环)直径: %.2f" % self.d_low_5)
        print("       长度: %.2f" % self.len_low_5)
        print("  第六节直径: %.2f" % self.d_low_6)
        print("  (因第六节长度可直接作图得到，故省略)")

    def shaft_about_output(self):
        self.config["Shaft"]["high_shaft_cal_d"] = str(self.high_shaft_cal_d)  # 高速轴计算直径
        self.config["Shaft"]["low_shaft_cal_d"] = str(self.low_shaft_cal_d)  # 低速轴计算直径
        self.config["Shaft"]["high_shaft_design_d"] = str(self.high_shaft_design_d)  # 高速轴设计直径
        self.config["Shaft"]["low_shaft_design_d"] = str(self.low_shaft_design_d)  # 低速轴设计直径
        self.config["Shaft"]["high_shaft_standard_d"] = str(self.high_shaft_standard_d)  # 高速轴标准直径
        self.config["Shaft"]["low_shaft_standard_d"] = str(self.low_shaft_standard_d)  # 低速轴标准直径
        self.config["Shaft"]["d_high_1"] = str(self.d_high_1)  # 高速轴各段直径
        self.config["Shaft"]["d_high_2"] = str(self.d_high_2)
        self.config["Shaft"]["d_high_3"] = str(self.d_high_3)
        self.config["Shaft"]["d_high_4"] = str(self.d_high_4)
        self.config["Shaft"]["d_high_5"] = str(self.d_high_5)
        self.config["Shaft"]["d_high_6"] = str(self.d_high_6)
        self.config["Shaft"]["len_high_1"] = str(self.len_high_1)  # 高速轴各段长度
        self.config["Shaft"]["len_high_2"] = str(self.len_high_2)
        self.config["Shaft"]["len_high_3"] = str(self.len_high_3)
        self.config["Shaft"]["len_high_4"] = str(self.len_high_4)
        self.config["Shaft"]["len_high_5"] = str(self.len_high_5)
        self.config["Shaft"]["len_high_6"] = str(self.len_high_6)
        self.config["Shaft"]["d_low_1"] = str(self.d_low_1)  # 低速轴各段直径
        self.config["Shaft"]["d_low_2"] = str(self.d_low_2)
        self.config["Shaft"]["d_low_3"] = str(self.d_low_3)
        self.config["Shaft"]["d_low_4"] = str(self.d_low_4)
        self.config["Shaft"]["d_low_5"] = str(self.d_low_5)
        self.config["Shaft"]["d_low_6"] = str(self.d_low_6)
        self.config["Shaft"]["len_low_1"] = str(self.len_low_1)  # 低速轴各段长度
        self.config["Shaft"]["len_low_2"] = str(self.len_low_2)
        self.config["Shaft"]["len_low_3"] = str(self.len_low_3)
        self.config["Shaft"]["len_low_4"] = str(self.len_low_4)
        self.config["Shaft"]["len_low_5"] = str(self.len_low_5)
        self.config["Shaft"]["len_low_6"] = str(self.len_low_6)
        self.config["Shaft"]["bearing_ID_high"] = str(self.bearing_ID_high)
        self.config["Shaft"]["bearing_ID_low"] = str(self.bearing_ID_low)
        self.config["Shaft"]["coupling_type_low"] = str(self.coupling_type_low)
        self.config["Shaft"]["coupling_L_low"] = str(self.coupling_L_low)
        self.config["Shaft"]["coupling_L1_low"] = str(self.coupling_L1_low)
        self.config["Shaft"]["bearing_high_D"] = str(self.bearing_high_D)  # 轴承外径
        self.config["Shaft"]["bearing_low_D"] = str(self.bearing_low_D)
        self.config["Shaft"]["bearing_high_T"] = str(self.bearing_high_T)  # 轴承厚度
        self.config["Shaft"]["bearing_low_T"] = str(self.bearing_low_T)
        self.config["Shaft"]["bearing_cover_high_D"] = str(self.bearing_cover_high_D)  # 轴承端盖外径
        self.config["Shaft"]["bearing_cover_low_D"] = str(self.bearing_cover_low_D)
        print(self.coupling_type_low, self.coupling_L_low, self.coupling_L1_low)

        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)


def shaft_start():
    local_class = shaft_compress()
    # 程序运行
    local_class.first_design()
    local_class.shaft_length_design()
    local_class.shaft_about_output()
    print("因轴套类零件力学计算关键数据缺失，故暂不更新，待专业人士补充")
    print("-------------------轴结构运算已结束-------------------")
    # 返回输出状态
    sys.stdout = local_class.output_tmp
    local_class.output_tmp.close()


if __name__ == "__main__":
    shaft_start()
