import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

belt_type = 'A'  # 带型
P_design = 0.0  # 设计功率
P_single_belt = 0.0  # 单个带额定传输功率
delta_P = 0.0  # 额定功率增量
K_len = 0.0  # 长度修正系数
K_alpha = 0.0  # 包角修正系数
d_small = 0.0  # 小带轮直径
d_large = 0.0  # 大带轮直径
alpha_small = 0.0  # 小带轮包角
alpha_large = 0.0  # 大带轮包角
center_distance = 0.0  # 带轮中心距
belt_base_len = 0.0  # 带轮基准长度
belt_sum = 0.0  # 带数
mass_per_unit = 0.0  # 带单位长度质量
belt_speed = 0.0  # 带速
F_pull_0 = 0.0  # 每根带初拉力
F_Q = 0.0  # 轴上载荷
d_small_wheel_shaft = 0.0  # 小带轮设计轴孔径
d_large_wheel_shaft = 0.0  # 大带轮设计轴孔径
L_small_wheel = 0.0  # 小带轮设计轮毂宽
L_large_wheel = 0.0  # 大带轮设计轴孔宽


def belt_type_choose():  # 选择V带型号

    global belt_type
    global P_design
    # 取V带类型
    P_design = P_motor * K_A
    select_parameters = 506.7 * (P_design - 0.8) + 357.5
    # 因没有现成的运算函数，遂使用近似函数区分A带区与Z带区，但无法判定除此之外的其它带型
    if select_parameters > n_motor:
        belt_type = 'A'
    else:
        belt_type = 'Z'
    print("以下是V带传动部分")
    print("----------------------------------------------------")


def data_update():  # 更新相关参数

    global i_belt
    global i_gear
    global n_motor
    global n_highspeed
    global n_lowspeed
    global n_output
    global P_motor
    global P_highspeed
    global P_lowspeed
    global P_output
    global T_highspeed
    global T_lowspeed
    global T_output

    # 更新传动比
    i_belt = d_large / d_small
    i_gear = i_total / i_belt

    # 更新转速
    n_highspeed = n_motor / i_belt
    n_lowspeed = n_output = n_highspeed / i_gear

    # 更新转矩
    T_highspeed = 9550 * P_highspeed / n_highspeed
    T_lowspeed = 9550 * P_lowspeed / n_lowspeed
    T_output = 9550 * P_output / n_output


def belt_wheel_choose():  # 选择带轮直径
    global d_small
    global d_large
    global i_belt
    global P_single_belt

    # 取小带轮直径，参考标准系列，不同于课本，直接使用额定功率表各带型的界定范围参考，毕竟没函数
    for i in range(len(belt_P_scheduled)):

        if belt_P_scheduled[i][0] != belt_type:
            continue
        record = 0
        for stp in range(5):
            if belt_P_scheduled[i + stp][1] * pi * n_motor / 60000.0 < 5:
                continue
            if belt_P_scheduled[i + stp][1] * pi * n_motor / 60000.0 > 20:
                break
            d_small = belt_P_scheduled[i + stp][1]
            record = stp
        # 顺便取一下单根V带额定功率
        delta = n_motor
        last = delta
        for j in range(2, len(belt_P_scheduled[0])):
            delta = abs(n_motor - belt_P_scheduled[0][j])
            if delta > last:
                break
            P_single_belt = belt_P_scheduled[i + record][j]
            last = delta
        break

    # 取大带轮直径，参考标准系列
    last = 0.0
    targeting = 0.0
    d_large = d_small * i_belt
    for i in belt_wheel_designed:
        for j in i:
            last = targeting
            targeting = j
            # 保证带轮传动比不大于齿轮组的同时寻找合适尺寸
            if targeting >= d_large or ((targeting / d_small) > i_total / (targeting / d_small)):
                break
        if targeting >= d_large:
            break

    # 取更接近的值用作带轮
    mid = (last + targeting) / 2
    if d_large >= mid:
        d_large = targeting
    else:
        d_large = last

    # 第一轮更新数据
    data_update()

    print("·确定V带带轮直径")
    print("  初定带型号为: %s型" % belt_type)
    print("  对应小/大带轮直径为: %.0f / %.0f" % (d_small, d_large))
    print("  带轮传动比修正为: %.2f" % i_belt)
    print("  相关其它数据已完成修正")


def base_length_design():  # 选择V带基准长度
    global belt_type
    global d_small
    global d_large
    global center_distance
    global belt_base_len
    global K_len
    global alpha_small

    # 初定中心距及带基准长度
    center_distance_0 = 1.3 * (d_small + d_large)
    belt_base_len_0 = 2 * center_distance + pi * (d_small + d_large) / 2 + ((d_large - d_small) ** 2) / (
            4 * center_distance_0)

    # 由表取标准值进行更正
    row = 4 if belt_type == 'A' else 2
    delta = belt_base_len_0
    for i in range(1, len(belt_length_list[row])):
        if abs(belt_length_list[row][i] - belt_base_len) < delta:
            delta = belt_base_len_0 - belt_base_len
            belt_base_len = belt_length_list[row][i]
            K_len = belt_length_list[row + 1][i]
        else:
            break

    # 确定中心距及小带轮包角
    center_distance = center_distance_0 + (belt_base_len - belt_base_len_0) / 2
    alpha_small = 180 - 57.3 * (d_large - d_small) / center_distance

    print("·确定中心距及V带基准长度")
    print("  根据0.7(d_d1 + d_d2) <= a_0 <= 2(d_d1 + d_d2), 初定中心距为: %.2f" % center_distance_0)
    print("  初定V带基准长度: %.2f" % belt_base_len_0)
    print("  由标准值确定V带基准长度为: %.2f" % belt_base_len)
    print("  再确定中心距为: %.2f" % center_distance)
    print("  小带轮包角计算为: %.2f°" % alpha_small)


def belt_count():  # 计算带数
    global belt_type
    global P_design
    global P_single_belt
    global delta_P
    global K_len
    global K_alpha
    global belt_sum
    global alpha_small

    # 选用额定功率增量
    for i in range(1, len(belt_deltaP_scheduled)):
        if belt_deltaP_scheduled[i][0] == belt_type:
            # 按传动比算范围
            target_i = 0
            for j in range(0, 3):
                if i_belt >= belt_deltaP_scheduled[i + j][1]:
                    target_i = j
            # 按转速选列
            target_n = 2
            delta = n_motor
            last = delta
            for j in range(2, len(belt_deltaP_scheduled[0])):
                delta = abs(n_motor - belt_deltaP_scheduled[0][j])
                if delta > last: break
                last = delta
                target_n = j
            delta_P = belt_deltaP_scheduled[i + target_i][target_n]
            break

    # 取包角修正系数
    delta = alpha_small
    last = delta
    K_alpha = Wrap_Angle_Correction[1][0]
    for i in range(19):
        delta = abs(alpha_small - Wrap_Angle_Correction[0][i])
        if delta > last: break
        last = delta
        K_alpha = Wrap_Angle_Correction[1][i]

    # 计算V带总数
    belt_sum = np.ceil(P_design / ((P_single_belt + delta_P) * K_alpha * K_len))

    print("·确定V带根数")
    print("  由先前运算结果取得单根V带额定功率为: %.2f kW" % P_single_belt)
    print("  取得额定功率增量为: %.2f kW" % delta_P)
    print("  取得包角修正系数为: %.2f" % K_alpha)
    print("  取得带长修正系数为: %.2f" % K_len)
    print("  计算得V带根数为: %d" % belt_sum)


def aft_design():  # 计算其它部件参数
    global mass_per_unit
    global belt_type
    global P_design
    global d_small
    global belt_speed
    global F_pull_0
    global F_Q
    global d_small_wheel_shaft
    global d_large_wheel_shaft
    global L_small_wheel
    global L_large_wheel

    # 单位长度质量
    if belt_type == 'A': mass_per_unit = 0.10
    if belt_type == 'Z': mass_per_unit = 0.06

    # 带速及轴上载荷
    belt_speed = pi * d_small * n_motor / 60000
    F_pull_0 = 500 * P_design / (belt_sum * belt_speed) * (2.5 / K_alpha - 1) + mass_per_unit * (belt_speed ** 2)
    F_Q = 2 * F_pull_0 * belt_sum * np.sin(np.radians(alpha_small) / 2)

    # 初定轴孔径及轮毂宽度
    d_small_wheel_shaft = 110 * np.cbrt(P_motor / n_motor) * 1.03
    d_large_wheel_shaft = 110 * np.cbrt(P_highspeed / n_highspeed) * 1.03

    print("·结构设计计算")
    print("  V带单位长度质量查表得为: %.2f" % mass_per_unit)
    print("  单根带所受初拉力为: %.2f N" % F_pull_0)
    print("  轴上载荷为: %.2f N" % F_Q)
    print("  以45钢为轴用材料，开单键槽")
    print("  根据圆截面轴的扭转强度条件，初定小带轮轴的计算直径为: %.2f" % d_small_wheel_shaft)
    print("  大带轮轴的计算直径为: %.2f" % d_large_wheel_shaft)

    # 根据标准尺寸系列选直径，常用的40以内有规律可循
    tag1 = tag2 = 0
    for i in range(10, 26):
        if i > d_small_wheel_shaft and tag1 == 0:
            d_small_wheel_shaft = i
            tag1 = 1
        if i > d_large_wheel_shaft and tag2 == 0:
            d_large_wheel_shaft = i
            tag2 = 1
    for i in range(26, 41, 2):
        if i > d_small_wheel_shaft and tag1 == 0:
            d_small_wheel_shaft = i
            tag1 = 1
        if i > d_large_wheel_shaft and tag2 == 0:
            d_large_wheel_shaft = i
            tag2 = 1
    L_small_wheel = np.ceil(1.7 * d_small_wheel_shaft)
    L_large_wheel = np.ceil(1.7 * d_large_wheel_shaft)

    print("  根据圆截面轴的标准尺寸，暂定小带轮轴的直径为: %.2f" % d_small_wheel_shaft)
    print("  大带轮轴的直径为: %.2f" % d_large_wheel_shaft)
    print("  故根据《机械设计课程设计》，轮毂宽度荐用值取1.5~2倍轴孔宽度，则:")
    print("  小带轮轮毂的宽度为: %.2f" % L_small_wheel)
    print("  大带轮轮毂的宽度为: %.2f" % L_large_wheel)
    print("-------------------带轮运算已结束--------------------")


def output_BeltAbout():
    global belt_type
    global P_design
    global P_single_belt
    global delta_P
    global K_len
    global K_alpha
    global d_small
    global d_large
    global alpha_small
    global alpha_large
    global center_distance
    global belt_base_len
    global belt_sum
    global mass_per_unit
    global belt_speed
    global F_pull_0
    global F_Q
    global d_small_wheel_shaft
    global d_large_wheel_shaft
    global L_small_wheel
    global L_large_wheel

    config["Belt"]["belt_type"] = belt_type
    config["Belt"]["P_design"] = str(P_design)
    config["Belt"]["P_single_belt"] = str(P_single_belt)
    config["Belt"]["delta_P"] = str(delta_P)
    config["Belt"]["K_len"] = str(K_len)
    config["Belt"]["K_alpha"] = str(K_alpha)
    config["Belt"]["d_small"] = str(d_small)
    config["Belt"]["d_large"] = str(d_large)
    config["Belt"]["alpha_small"] = str(alpha_small)
    config["Belt"]["alpha_large"] = str(alpha_large)
    config["Belt"]["center_distance"] = str(center_distance)
    config["Belt"]["belt_base_len"] = str(belt_base_len)
    config["Belt"]["belt_sum"] = str(belt_sum)
    config["Belt"]["mass_per_unit"] = str(mass_per_unit)
    config["Belt"]["belt_speed"] = str(belt_speed)
    config["Belt"]["F_pull_0"] = str(F_pull_0)
    config["Belt"]["F_Q"] = str(F_Q)
    config["Belt"]["d_small_wheel_shaft"] = str(d_small_wheel_shaft)
    config["Belt"]["d_large_wheel_shaft"] = str(d_large_wheel_shaft)
    config["Belt"]["L_small_wheel"] = str(L_small_wheel)
    config["Belt"]["L_large_wheel"] = str(L_large_wheel)

    with open("./config.ini", "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")

    # 数据记录
    K_A = float(config["Belt"]["K_A"])
    efficiency_belt = float(config["General"]["efficiency_belt"])
    efficiency_bearing = float(config["General"]["efficiency_bearing"])
    efficiency_gear = float(config["General"]["efficiency_gear"])
    efficiency_coupling = float(config["General"]["efficiency_coupling"])
    efficiency_roller = float(config["General"]["efficiency_roller"])
    n_motor = float(config["Machine"]["n_motor"])
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
    i_total = float(config["Machine"]["i_total"])
    i_belt = float(config["Machine"]["i_belt"])
    i_gear = float(config["Machine"]["i_gear"])

    # 导入额定功率数据
    belt_P_scheduled = pd.read_excel('./all_sheets/belt_P_scheduled.xls', sheet_name="Sheet1")
    train_data = np.array(belt_P_scheduled)
    belt_P_scheduled = train_data.tolist()
    # 导入额定功率增量数据
    belt_deltaP_scheduled = pd.read_excel('./all_sheets/belt_deltaP_scheduled.xls', sheet_name="Sheet1")
    train_data = np.array(belt_deltaP_scheduled)
    belt_deltaP_scheduled = train_data.tolist()
    # 导入包角修正系数数据
    Wrap_Angle_Correction = pd.read_excel('./all_sheets/Wrap_Angle_Correction.xls', sheet_name="Sheet1")
    train_data = np.array(Wrap_Angle_Correction)
    Wrap_Angle_Correction = train_data.tolist()
    # 导入带轮标准系列数据
    belt_wheel_designed = pd.read_excel('./all_sheets/belt_wheel_designed.xls', sheet_name="Sheet1")
    train_data = np.array(belt_wheel_designed)
    belt_wheel_designed = train_data.tolist()
    # 导入V带基准长度标准系列数据
    belt_length_list = pd.read_excel('./all_sheets/belt_length_list.xls', sheet_name="Sheet1")
    train_data = np.array(belt_length_list)
    belt_length_list = train_data.tolist()

    # 将数据输出到可视文件中
    output_file = open("Calculated_Data.txt", mode='w+')
    temp = sys.stdout
    sys.stdout = output_file
    # 程序运行
    belt_type_choose()
    belt_wheel_choose()
    base_length_design()
    belt_count()
    aft_design()
    output_BeltAbout()
    # 返回输出状态
    sys.stdout = temp
    output_file.close()
