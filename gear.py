import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

stress_limit_high = 0.0  # 小齿轮极限接触应力
stress_limit_low = 0.0  # 大齿轮极限接触应力
stress_allowable_high = 0.0  # 小齿轮许用接触应力
stress_allowable_low = 0.0  # 大齿轮许用接触应力
stress_limit_high_flim = 0.0  # 小齿轮极限弯曲应力
stress_limit_low_flim = 0.0  # 小齿轮极限弯曲应力
stress_allowable_high_flim = 0.0  # 小齿轮许用弯曲应力
stress_allowable_low_flim = 0.0  # 大齿轮许用弯曲应力
hardness_high = 0.0  # 小齿轮平均硬度
hardness_low = 0.0  # 大齿轮平均硬度
d_highspeed = 0.0  # 小齿轮分度圆直径
d_lowspeed = 0.0  # 大齿轮分度圆直径
z_highspeed = 0.0  # 小齿轮齿数
z_lowspeed = 0.0  # 大齿轮齿数
m = 0.0  # 模数
center_distance = 0.0  # 中心距
b_highspeed = 0.0  # 小齿轮齿宽
b_lowspeed = 0.0  # 小齿轮齿宽
addendum_h_factor = 1  # 齿顶高系数
bottom_c_factor = 0.25  # 顶隙系数
alpha = 20  # 齿形角
addendum_height = 0.0
bottom_clearance = 0.0
height = 0.0
base_circle_d_high = 0.0
base_circle_d_low = 0.0
addendum_circle_d_high = 0.0
addendum_circle_d_low = 0.0
root_d_high = 0.0
root_d_low = 0.0
pitch = 0.0
tooth_thickness = 0.0
spacewidth = 0.0
d_gear_shaft_low = 0.0  # 低速轴直径
d_gear_shaft_high = 0.0  # 高速轴直径


def stress_cal():  # 许用接触应力的计算

    global stress_limit_low
    global stress_limit_high
    global stress_allowable_low
    global stress_allowable_high
    global hardness_low
    global hardness_high

    # 先取各齿轮材料平均硬度，一般比较不容易出错的是45号钢的各种形态
    if highspeed_gear_material == "45 quenched and tempered":  # 高速轮（小齿轮，硬度要求偏高）
        hardness_high = 240
    elif highspeed_gear_material == "45 normalizing":
        hardness_high = 200
    if lowspeed_gear_material == "45 quenched and tempered":  # 低速轮（大齿轮，硬度要求偏低）
        hardness_low = 240
    elif lowspeed_gear_material == "45 normalizing":
        hardness_low = 200

    # 再计算极限接触应力
    if highspeed_gear_material.find("45") != -1:
        stress_limit_high = np.ceil(hardness_high * 0.87 + 380)
    if lowspeed_gear_material.find("45") != -1:
        stress_limit_low = np.ceil(hardness_low * 0.87 + 380)

    # 计算许用接触应力
    safety_factor = 1  # 取理想值
    stress_allowable_low = stress_limit_low / safety_factor
    stress_allowable_high = stress_limit_high / safety_factor

    print("以下是减速齿轮组部分")
    print("----------------------------------------------------")
    print("·按齿面解除疲劳强度设计")
    print("·计算接触应力")
    print("  计算极限应力得小齿轮极限应力: %d" % stress_limit_low, "MPa")
    print("  大齿轮极限应力: %d" % stress_limit_high, "MPa")
    print("  依工作情况取安全系数S_H = %d" % safety_factor)
    print("  计算许用接触应力得小齿轮许用接触应力: %d" % stress_allowable_low, "MPa")
    print("  大齿轮许用接触应力: %d" % stress_allowable_high, "MPa")


def size_deisgn():  # 确定几何尺寸

    global d_highspeed
    global d_lowspeed
    global z_highspeed
    global z_lowspeed
    global i_gear
    global stress_allowable_high
    global m
    global center_distance
    global b_lowspeed
    global b_highspeed

    thickness_factor = 1  # 齿宽系数
    load_factor = 1.4  # 载荷系数
    Z_H = 2.5  # 节点区域系数
    Z_E = 189.8  # 弹性系数

    # 齿轮计算直径
    d_highspeed = np.cbrt(pow((Z_E * Z_H / stress_allowable_high), 2) * 2 * load_factor * t_highspeed / thickness_factor
                          * (i_gear + 1) / i_gear)

    print("·计算并设计齿轮的几何尺寸")
    print("  单级减速器中齿轮相对轴承对称布置，由《机械设计基础》P117 表7-7取齿宽系数: %d" % thickness_factor)
    print("  工作平稳，软齿面齿轮，取载荷系数: %.2f" % load_factor)
    print("  标准直齿圆柱传动，取节点区域系数: %.2f" % Z_H)
    print("  钢制齿轮，取弹性系数: %.2f" % Z_E)
    print("  由是，得小齿轮计算直径为: %.2f" % d_highspeed)

    # 确定几何尺寸
    # 取齿数
    z_highspeed = 25
    z_lowspeed = np.ceil(i_gear * z_highspeed)
    m = d_highspeed / z_highspeed
    # 传动比修正
    i_gear = z_lowspeed / z_highspeed

    # 取标准模数
    target1_m = gear_standard_modulus[0][0]
    target2_m = gear_standard_modulus[1][0]
    # 为了保险同取两个标准序列
    for series in gear_standard_modulus[0]:
        target1_m = series
        if series > m:
            break
    for series in gear_standard_modulus[1]:
        target2_m = series
        if series > m:
            break
    m = target1_m if abs(target1_m - m) < abs(target2_m - m) else target2_m

    # 第二次修正
    d_highspeed = m * z_highspeed
    d_lowspeed = m * z_lowspeed
    center_distance = (d_lowspeed + d_highspeed) / 2

    # 齿宽
    b_lowspeed = np.ceil(thickness_factor * d_highspeed)
    b_highspeed = np.ceil(b_lowspeed / 10) * 10 if np.ceil(b_lowspeed / 10) * 10 - b_lowspeed >= 5 <= 10 else (
        np.ceil(b_lowspeed / 5 + 1) * 5 if np.ceil(b_lowspeed / 5 + 1) * 5 - b_lowspeed >= 5 <= 10
        else np.ceil(b_lowspeed / 5) * 5)

    print("  取大/小齿轮齿数分别为: %d / %d" % (z_lowspeed, z_highspeed))
    print("  修正传动比值为: %.2f" % i_gear)
    print("  取模数标准值为: %.3f" % m)
    print("  修正分度圆直径得大/小齿轮分度圆直径分别为: %.3f / %.3f" % (d_lowspeed, d_highspeed), "mm")
    print("  中心距为: %.3f" % center_distance)
    print("  大/小齿轮齿宽分别为: %d / %d" % (b_lowspeed, b_highspeed))


def Strength_Check():
    global m
    global b_lowspeed
    global hardness_high
    global hardness_low
    global stress_limit_low_flim
    global stress_limit_high_flim
    global stress_allowable_high_flim
    global stress_allowable_low_flim
    global z_lowspeed
    global z_highspeed

    load_factor = 1.4  # 载荷系数
    safety_factor = 1.4  # 安全系数

    # 计算极限弯曲应力
    if highspeed_gear_material.find("45") != -1:
        stress_limit_high_flim = 0.7 * hardness_high + 275
    if lowspeed_gear_material.find("45") != -1:
        stress_limit_low_flim = 0.7 * hardness_low + 275

    # 计算许用齿根应力
    stress_allowable_high_flim = stress_limit_high_flim / safety_factor
    stress_allowable_low_flim = stress_limit_low_flim / safety_factor

    # 验算齿根应力
    form_factor_highspeed = compound_form_factor[1][0]  # 小齿轮复合齿形系数
    form_factor_lowspeed = compound_form_factor[1][0]  # 小齿轮复合齿形系数

    # 线性插值（你最好是）求复合齿形系数
    for i in range(1, len(compound_form_factor[0]) - 1):
        form_factor_highspeed = compound_form_factor[1][i]
        if compound_form_factor[0][i] > z_highspeed:
            form_factor_highspeed = compound_form_factor[1][i] if abs(z_highspeed - compound_form_factor[0][i]) < abs(
                z_highspeed - compound_form_factor[0][i - 1]) else compound_form_factor[1][i - 1]
            break
    if z_highspeed > 250:  # inf修正
        form_factor_highspeed = compound_form_factor[1][len(compound_form_factor[0] - 1)]

    for i in range(1, len(compound_form_factor[0]) - 1):
        form_factor_lowspeed = compound_form_factor[1][i]
        if compound_form_factor[0][i] > z_lowspeed:
            form_factor_lowspeed = compound_form_factor[1][i] if abs(z_lowspeed - compound_form_factor[0][i]) < abs(
                z_lowspeed - compound_form_factor[0][i - 1]) else compound_form_factor[1][i - 1]
            break
    if z_lowspeed > 250:  # inf修正
        form_factor_lowspeed = compound_form_factor[1][len(compound_form_factor[0] - 1)]

    # 齿根应力
    stress_high_flim = 2 * load_factor * t_highspeed * form_factor_highspeed / (b_lowspeed * d_highspeed * m)
    stress_low_flim = stress_high_flim * form_factor_lowspeed / form_factor_highspeed

    print("·校核齿根弯曲疲劳强度")
    print("  计算大/小齿轮齿根极限应力为: %.2f / %.2f" % (stress_limit_low_flim, stress_limit_high_flim), "MPa")
    print("  取安全系数为: %.1f" % safety_factor)
    print("  计算大/小齿轮许用齿根应力为: %.2f / %.2f" % (stress_allowable_low_flim, stress_allowable_high_flim), "MPa")
    print("  大/小齿轮复合齿形系数由教材P116 表7-6得为: %.2f / %.2f" % (form_factor_lowspeed, form_factor_highspeed))
    print("  大齿轮齿根应力计算为: %.2f" % stress_low_flim, "MPa, " + ("符合标准" if stress_low_flim < stress_allowable_low_flim
                                                             else "不符合标准"))
    print("  小齿轮齿根应力计算为: %.2f" % stress_high_flim, "MPa, " + ("符合标准" if stress_high_flim < stress_allowable_high_flim
                                                              else "不符合标准"))


def gear_design():

    global addendum_h_factor
    global bottom_c_factor
    global b_lowspeed
    global b_highspeed
    global d_highspeed
    global d_lowspeed
    global m
    global alpha
    global addendum_height
    global bottom_clearance
    global height
    global base_circle_d_high
    global base_circle_d_low
    global addendum_circle_d_high
    global addendum_circle_d_low
    global root_d_high
    global root_d_low
    global pitch
    global tooth_thickness
    global spacewidth
    global d_gear_shaft_low
    global d_gear_shaft_high
    global t_highspeed
    global t_lowspeed
    global t_output
    global n_lowspeed
    global n_output

    addendum_height = addendum_h_factor * m  # 齿顶高
    bottom_clearance = bottom_c_factor * m  # 顶隙
    dedendum = bottom_clearance + addendum_height  # 齿根高
    height = addendum_height + dedendum  # 齿高

    base_circle_d_high = d_highspeed * np.cos(np.radians(alpha))  # 小齿轮基圆直径
    base_circle_d_low = d_lowspeed * np.cos(np.radians(alpha))  # 大齿轮基圆直径
    addendum_circle_d_high = d_highspeed + 2 * addendum_height  # 小齿轮齿顶圆直径
    addendum_circle_d_low = d_lowspeed + 2 * addendum_height  # 大齿轮齿顶圆直径
    root_d_high = d_highspeed - 2 * dedendum  # 小齿轮齿根圆直径
    root_d_low = d_lowspeed - 2 * dedendum  # 大齿轮齿根圆直径
    pitch = pi * m  # 齿距
    tooth_thickness = spacewidth = pitch / 2  # 标准齿厚/齿槽宽

    # 三次修正传动数据
    t_highspeed /= 10000
    n_lowspeed = n_output = n_highspeed / i_gear
    t_lowspeed = 9550 * p_lowspeed / n_lowspeed
    t_output = 9550 * p_output / n_output

    # 轴设计
    d_gear_shaft_high += 6
    tag2 = 0
    d_gear_shaft_low = 106 * np.cbrt(p_lowspeed / n_lowspeed) * 1.03
    for i in range(10, 26):
        if i > d_gear_shaft_low and tag2 == 0:
            d_gear_shaft_low = i
            tag2 = 1
    for i in range(26, 41, 2):
        if i > d_gear_shaft_low and tag2 == 0:
            d_gear_shaft_low = i
            tag2 = 1
    d_gear_shaft_low += 6

    print("·齿轮整体结构设计")
    print("  综上，得齿轮整体结构如下:")
    print("  齿顶高为: %.2f" % addendum_height)
    print("  顶隙: %.2f" % bottom_clearance)
    print("  齿根高为: %.2f" % dedendum)
    print("  齿高为: %.2f" % height)
    print("  大/小齿轮分度圆直径分别为: %.2f / %.2f" % (d_lowspeed , d_highspeed))
    print("  大/小齿轮基圆直径分别为: %.2f / %.2f" % (base_circle_d_low, base_circle_d_high))
    print("  大/小齿轮齿宽为: %.2f / %.2f" % (b_lowspeed, b_highspeed))
    print("  大/小齿轮齿顶圆直径为: %.2f / %.2f" % (addendum_circle_d_low, addendum_circle_d_high))
    print("  大/小齿轮齿根圆直径为: %.2f / %.2f" % (root_d_low, root_d_high))
    print("  大/小齿轮初定轴孔径为: %.2f / %.2f" % (d_gear_shaft_low, d_gear_shaft_high))
    print("------------------减速齿轮运算已结束-------------------")


def output_GearAbout():

    global z_highspeed
    global z_lowspeed
    global b_lowspeed
    global b_highspeed
    global d_highspeed
    global d_lowspeed
    global m
    global center_distance
    global addendum_height
    global bottom_clearance
    global height
    global base_circle_d_high
    global base_circle_d_low
    global addendum_circle_d_high
    global addendum_circle_d_low
    global root_d_high
    global root_d_low
    global pitch
    global tooth_thickness
    global spacewidth
    global d_gear_shaft_low
    global d_gear_shaft_high
    global t_lowspeed
    global t_output
    global n_lowspeed
    global n_output

    config["Gear"]["d_highspeed"] = str(d_highspeed)
    config["Gear"]["d_lowspeed"] = str(d_lowspeed)
    config["Gear"]["b_highspeed"] = str(b_highspeed)
    config["Gear"]["b_lowspeed"] = str(b_lowspeed)
    config["Gear"]["z_highspeed"] = str(z_highspeed)
    config["Gear"]["z_lowspeed"] = str(z_lowspeed)
    config["Gear"]["m"] = str(m)
    config["Gear"]["center_distance"] = str(center_distance)
    config["Gear"]["addendum_height"] = str(addendum_height)
    config["Gear"]["bottom_clearance"] = str(bottom_clearance)
    config["Gear"]["height"] = str(height)
    config["Gear"]["base_circle_d_high"] = str(base_circle_d_high)
    config["Gear"]["base_circle_d_low"] = str(base_circle_d_low)
    config["Gear"]["addendum_circle_d_high"] = str(addendum_circle_d_high)
    config["Gear"]["addendum_circle_d_low"] = str(addendum_circle_d_low)
    config["Gear"]["root_d_high"] = str(root_d_high)
    config["Gear"]["root_d_low"] = str(root_d_low)
    config["Gear"]["pitch"] = str(pitch)
    config["Gear"]["tooth_thickness"] = str(tooth_thickness)
    config["Gear"]["spacewidth"] = str(spacewidth)
    config["Gear"]["d_gear_shaft_low"] = str(d_gear_shaft_low)
    config["Gear"]["d_gear_shaft_high"] = str(d_gear_shaft_high)

    config["Machine"]["t_output"] = str(t_output)
    config["Machine"]["t_lowspeed"] = str(t_lowspeed)
    config["Machine"]["n_lowspeed"] = str(n_lowspeed)
    config["Machine"]["n_output"] = str(n_output)

    with open("./config.ini", "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")

    # 数据记录
    highspeed_gear_material = config["Gear"]["highspeed_gear_material"]
    lowspeed_gear_material = config["Gear"]["lowspeed_gear_material"]
    d_gear_shaft_high = float(config["Belt"]["d_large_wheel_shaft"])
    n_highspeed = float(config["Machine"]["n_highspeed"])
    p_highspeed = float(config["Machine"]["p_highspeed"])
    t_highspeed = float(config["Machine"]["t_highspeed"]) * 10000
    i_gear = float(config["Machine"]["i_gear"])
    p_lowspeed = float(config["Machine"]["p_lowspeed"])
    n_lowspeed = float(config["Machine"]["n_lowspeed"])
    t_lowspeed = float(config["Machine"]["t_lowspeed"])
    p_output = float(config["Machine"]["p_output"])
    n_output = float(config["Machine"]["n_output"])
    t_output = float(config["Machine"]["t_output"])
    efficiency_bearing = float(config["General"]["efficiency_bearing"])
    efficiency_gear = float(config["General"]["efficiency_gear"])
    efficiency_coupling = float(config["General"]["efficiency_coupling"])
    efficiency_roller = float(config["General"]["efficiency_roller"])

    # 导入标准模数
    gear_standard_modulus = pd.read_excel('./all_sheets/gear_standard_modulus.xls', sheet_name="Sheet1")
    train_data = np.array(gear_standard_modulus)
    gear_standard_modulus = train_data.tolist()
    # 导入标准模数
    compound_form_factor = pd.read_excel('./all_sheets/compound_form_factor.xls', sheet_name="Sheet1")
    train_data = np.array(compound_form_factor)
    compound_form_factor = train_data.tolist()

    # 将数据输出到可视文件中
    output_file = open("Calculated_Data.txt", mode='w+')
    temp = sys.stdout
    sys.stdout = output_file
    # 程序运行
    stress_cal()
    size_deisgn()
    Strength_Check()
    gear_design()
    output_GearAbout()
    # 返回输出状态
    sys.stdout = temp
    output_file.close()
