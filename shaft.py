import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

high_shaft_cal_d = 0.0  # 高速轴计算直径
low_shaft_cal_d = 0.0  # 低速轴计算直径
high_shaft_design_d = 0.0  # 高速轴设计直径
low_shaft_design_d = 0.0  # 低速轴设计直径
high_shaft_standard_d = 0.0  # 高速轴标准直径
low_shaft_standard_d = 0.0  # 低速轴标准直径
alpha = 20
d_high_1 = 0.0  # 高速轴各段直径
d_high_2 = 0.0
d_high_3 = 0.0
d_high_4 = 0.0
d_high_5 = 0.0
d_high_6 = 0.0
len_high_1 = 0.0  # 高速轴各段长度
len_high_2 = 0.0
len_high_3 = 0.0
len_high_4 = 0.0
len_high_5 = 0.0
len_high_6 = 0.0
d_low_1 = 0.0  # 低速轴各段直径
d_low_2 = 0.0
d_low_3 = 0.0
d_low_4 = 0.0
d_low_5 = 0.0
d_low_6 = 0.0
len_low_1 = 0.0  # 低速轴各段长度
len_low_2 = 0.0
len_low_3 = 0.0
len_low_4 = 0.0
len_low_5 = 0.0
len_low_6 = 0.0
bearing_cover_high_D = 0.0  # 轴承端盖外径
bearing_cover_low_D = 0.0


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


def shaft_length_design():

    global high_shaft_standard_d, len_high_1, len_high_2, len_high_3, len_high_4, len_high_5, len_high_6, \
        d_high_1, d_high_2, d_high_3, d_high_4, d_high_5, d_high_6, len_low_1, len_low_2, len_low_3, \
        len_low_4, len_low_5, len_low_6, d_low_1, d_low_2, d_low_3, d_low_4, d_low_5, d_low_6, \
        bearing_cover_high_D, bearing_cover_low_D

    # 计算螺钉长度
    nail_len = 0.0
    bearing_cover_bolt_d = float(config["Machine"]["bearing_cover_bolt_d"])  # 这里是轴承盖直径
    for i in range(len(standard_bolt[0])):
        if bearing_cover_bolt_d == standard_bolt[0][i]:
            nail_len = standard_bolt[1][i] + standard_bolt[2][i]

    # 计算高速轴
    # 第一段
    len_high_1 = float(config["Belt"]["L_large_wheel"]) + nail_len
    d_high_1 = high_shaft_standard_d
    # 第二段
    d_high_2 = d_high_1 + 4
    base_rib_thickness = float(config["Machine"]["base_rib_thickness"])  # 调用一下机壳数据，这里是机座壁厚
    e = np.ceil(1.2 * bearing_cover_bolt_d)
    e = e if 5 <= e <= 8 else 8 if e > 8 else 5
    len_high_2 = base_rib_thickness + e + nail_len

    # 高速轴轴承选用，顺带解决第三段和第六段直径问题
    bearing_high_T = 0
    bearing_high_D = 0
    bearing_ID_high = ""

    d_high_3 = d_high_2
    for i in range(len(bearing_0_size_series)):
        if bearing_0_size_series[i][1] > d_high_3:
            d_high_3 = bearing_0_size_series[i][1]
            bearing_high_T = bearing_0_size_series[i][3]
            bearing_high_D = bearing_0_size_series[i][2]
            bearing_ID_high += str(bearing_0_size_series[i][0])
            break
    if bearing_ID_high == "":
        lastone = len(bearing_0_size_series) - 1
        d_high_3 = bearing_0_size_series[lastone][1]
        bearing_high_T = bearing_0_size_series[lastone][3]
        bearing_high_D = bearing_0_size_series[lastone][2]
        bearing_ID_high += str(bearing_0_size_series[lastone][0])
    d_high_6 = d_high_3
    # 顺带把轴承盖外径给解决了
    bearing_cover_high_D = bearing_high_D + 5 * bearing_cover_bolt_d

    # 第三段长度
    delta_3 = 10
    delta_2 = float(config["Machine"]["delta_2"])
    len_high_3 = delta_2 + delta_3 + bearing_high_T + 2
    # 第四段
    d_high_4 = d_high_3 + 4
    L_gear_high = b_gear_highspeed if d_high_4 <= b_gear_highspeed <= d_high_4 * 1.5 else np.ceil(d_high_4 * 1.25)
    len_high_4 = L_gear_high - 2
    # 第五段
    a = np.ceil(0.075 * d_high_4 + 1)  # 轴环处轴肩大小
    d_high_5 = d_high_4 + 2 * a
    len_high_5 = np.ceil(a * 1.4)

    print("·高速轴计算")
    print("  根据标准GB/T 276-1994，经计算确定使用深沟球轴承编号为:", bearing_ID_high)
    print("    其内径为: %.2f" % d_high_3)
    print("    外径为: %.2f" % bearing_high_D)
    print("    厚度为: %.2f" % bearing_high_T)
    print("  根据轴承外径得高速轴轴承盖外径为: %.2f" % bearing_cover_high_D)
    print("  根据齿轮计算结果，得腹板式齿轮的轴实际参数:")
    print("    其轴/孔径理论值为: %.2f" % d_high_4)
    print("    孔长度为: %.2f , 根据《机械设计课程设计》, 轴长向内收缩2~3mm" % L_gear_high)
    print("  故得出高速轴各段数据如下:")
    print("  第一节直径: %.2f" % d_high_1)
    print("       长度: %.2f" % len_high_1)
    print("  第二节直径: %.2f" % d_high_2)
    print("       长度: %.2f" % len_high_2)
    print("  第三节直径: %.2f" % d_high_3)
    print("       长度: %.2f" % len_high_3)
    print("  第四节直径: %.2f" % d_high_4)
    print("       长度: %.2f" % len_high_4)
    print("  第五节(轴环)直径: %.2f" % d_high_5)
    print("       长度: %.2f" % len_high_5)
    print("  第六节直径: %.2f" % d_high_6)
    print("  (因第六节长度可直接作图得到，故省略)")

    # 低速轴同理

    # 计算所用联轴器
    coupling_type_low = ""
    coupling_L_low = 0
    coupling_L1_low = 0
    for i in range(len(coupling_standard)):
        if coupling_standard[i][1] <= low_shaft_standard_d:
            coupling_type_low = coupling_standard[i][0]
            coupling_L_low = coupling_standard[i][2]
            coupling_L1_low = coupling_standard[i][3]
            break
    if coupling_type_low == "":
        lastone = len(coupling_standard[0]) - 1
        coupling_type_low = coupling_standard[lastone][0]
        coupling_L_low = coupling_standard[lastone][2]
        coupling_L1_low = coupling_standard[lastone][3]

    # 第一段
    len_low_1 = coupling_L1_low
    d_low_1 = low_shaft_standard_d
    # 第二段
    d_low_2 = d_low_1 + 4
    e = np.ceil(1.2 * bearing_cover_bolt_d)
    e = e if 5 <= e <= 8 else 8 if e > 8 else 5
    len_low_2 = base_rib_thickness + e + nail_len

    # 低速轴轴承选用
    bearing_low_T = 0
    bearing_low_D = 0
    bearing_ID_low = ""

    d_low_3 = d_low_2
    for i in range(len(bearing_0_size_series)):
        if bearing_0_size_series[i][1] > d_low_3:
            d_low_3 = bearing_0_size_series[i][1]
            bearing_low_T = bearing_0_size_series[i][3]
            bearing_low_D = bearing_0_size_series[i][2]
            bearing_ID_low += str(bearing_0_size_series[i][0])
            break
    if bearing_ID_low == "":
        lastone = len(bearing_0_size_series) - 1
        d_low_3 = bearing_0_size_series[lastone][1]
        bearing_low_T = bearing_0_size_series[lastone][3]
        bearing_low_D = bearing_0_size_series[lastone][2]
        bearing_ID_low += str(bearing_0_size_series[lastone][0])
    d_low_6 = d_low_3
    bearing_cover_low_D = bearing_low_D + 5 * bearing_cover_bolt_d

    # 第三段长度
    delta_3 = 10
    delta_2 = float(config["Machine"]["delta_2"])
    len_low_3 = delta_2 + delta_3 + bearing_low_T + 2
    # 第四段
    d_low_4 = d_low_3 + 4
    L_gear_low = b_gear_lowspeed if d_low_4 <= b_gear_lowspeed <= d_low_4 * 1.5 else np.ceil(d_low_4 * 1.25)
    len_low_4 = L_gear_low - 2
    # 第五段
    a = np.ceil(0.075 * d_low_4 + 1)  # 轴环处轴肩大小
    d_low_5 = d_low_4 + 2 * a
    len_low_5 = np.ceil(a * 1.4)

    print("·低速轴计算")
    print("  根据标准GB/T 5014-2003，经计算确定使用LX型弹性柱销联轴器编号为:", coupling_type_low)
    print("    其内径为: %.2f" % d_low_1)
    print("    其轴孔长度/轴孔小径长度为: %.2f, %.2f" % (coupling_L_low, coupling_L1_low))
    print("    详细参数详见《机械设计课程设计》")
    print("  根据标准GB/T 276-1994，经计算确定使用深沟球轴承编号为:", bearing_ID_low)
    print("    其内径为: %.2f" % d_low_3)
    print("    外径为: %.2f" % bearing_low_D)
    print("    厚度为: %.2f" % bearing_low_T)
    print("  根据轴承外径得高速轴轴承盖外径为: %.2f" % bearing_cover_low_D)
    print("  根据齿轮计算结果，得腹板式齿轮的轴实际参数:")
    print("    其轴/孔径理论值为: %.2f" % d_low_4)
    print("    孔长度为: %.2f , 根据《机械设计课程设计》, 轴长向内收缩2~3mm" % L_gear_low)
    print("  故得出低速轴各段数据如下:")
    print("  第一节直径: %.2f" % d_low_1)
    print("       长度: %.2f" % len_low_1)
    print("  第二节直径: %.2f" % d_low_2)
    print("       长度: %.2f" % len_low_2)
    print("  第三节直径: %.2f" % d_low_3)
    print("       长度: %.2f" % len_low_3)
    print("  第四节直径: %.2f" % d_low_4)
    print("       长度: %.2f" % len_low_4)
    print("  第五节(轴环)直径: %.2f" % d_low_5)
    print("       长度: %.2f" % len_low_5)
    print("  第六节直径: %.2f" % d_low_6)
    print("  (因第六节长度可直接作图得到，故省略)")


def strength_check():

    global alpha

    # 高速轴危险截面距离轴承压力中心距离
    # len_gear_2_bearing =

    # 小齿轮处理论所受力
    peripheral_force_high = 2 * T_highspeed / d_gear_highspeed  # 圆周力
    radial_force_high = peripheral_force_high * np.tan(np.radians(alpha))  # 根据齿形角计算径向力

    print("·轴的强度计算")
    print("  对于直齿圆柱齿轮，理想状况下，减速器轴无轴向力，且轴上载荷方向与大小不变，故此处减速器轴向不传递弯矩")
    print("  对于6000系列深沟球轴承，轴承内壁完全接触轴踢，故压力中心视为轴承中线")
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
    length_2 = float(config["Machine"]["length_2"])
    d_gear_highspeed = float(config["Gear"]["d_highspeed"])
    d_gear_lowspeed = float(config["Gear"]["d_lowspeed"])
    d_gear_shaft_low = float(config["Gear"]["d_gear_shaft_low"])
    d_gear_shaft_high = float(config["Gear"]["d_gear_shaft_high"])
    b_gear_highspeed = float(config["Gear"]["b_highspeed"])
    b_gear_lowspeed = float(config["Gear"]["b_lowspeed"])

    # 导入标准六角头螺栓长度数据
    standard_bolt = pd.read_excel('./all_sheets/standard_bolt.xls', sheet_name="Sheet1")
    train_data = np.array(standard_bolt)
    standard_bolt = train_data.tolist()
    # 导入标准零尺寸系列深沟球轴承尺寸数据
    bearing_0_size_series = pd.read_excel('./all_sheets/bearing_0_size_series.xls', sheet_name="Sheet1")
    train_data = np.array(bearing_0_size_series)
    bearing_0_size_series = train_data.tolist()
    # 导入LX型弹性柱销联轴器尺寸数据
    coupling_standard = pd.read_excel('./all_sheets/coupling_standard.xls', sheet_name="Sheet1")
    train_data = np.array(coupling_standard)
    coupling_standard = train_data.tolist()

    # 将数据输出到可视文件中
    output_file = open("Calculated_Data.txt", mode='w+')
    temp = sys.stdout
    sys.stdout = output_file
    # 程序运行
    first_design()
    shaft_length_design()
    strength_check()
    # 返回输出状态
    sys.stdout = temp
    output_file.close()
