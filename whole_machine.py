import configparser as cp
import pandas as pd
import numpy as np
import sys
from numpy import pi

base_wall_thickness = 0.0  # 机座壁厚
hood_wall_thickness = 0.0  # 机盖壁厚
base_flange_thickness = 0.0  # 机座凸缘厚
hood_flange_thickness = 0.0  # 机盖凸缘厚
foundation_flange_thickness = 0.0  # 基底凸缘厚
base_rib_thickness = 0.0  # 机座肋厚
hood_rib_thickness = 0.0  # 机盖肋厚
boss_height = 0.0  # 轴承旁凸台高度
boss_radius = 0.0  # 轴承旁凸台半径
bearing_cover_diameter = 0.0  # 轴承端盖外径
foundation_bolt_d = 0.0  # 地脚螺钉直径
foundation_bolt_n = 0.0  # 地脚螺钉数目
foundation_bolt_PTH_d = 0.0  # 地脚螺钉通孔直径
foundation_bolt_seat_d = 0.0  # 地脚螺钉沉头座直径
foundation_flange_c1 = 0.0  # 底座凸缘尺寸
foundation_flange_c2 = 0.0
bearing_connection_bolt_d = 0.0  # 轴承旁连接螺栓直径
bearing_connection_bolt_PTH_d = 0.0  # 连接螺栓通孔直径
bearing_connection_bolt_seat_d = 0.0  # 连接螺栓沉头座直径
bearing_connection_flange_c1 = 0.0  # 凸缘尺寸
bearing_connection_flange_c2 = 0.0
shell_connection_bolt_d = 0.0  # 机座机盖旁连接螺栓直径
shell_connection_bolt_PTH_d = 0.0  # 连接螺栓通孔直径
shell_connection_bolt_seat_d = 0.0  # 连接螺栓沉头座直径
shell_connection_l = 175  # 螺栓间距
shell_connection_flange_c1 = 0.0  # 凸缘尺寸
shell_connection_flange_c2 = 0.0
dowel_pin_d = 0.0  # 定位销直径
bearing_cover_bolt_d = 0.0  # 轴承盖螺钉直径
seeker_cover_bolt_d = 0.0  # 窥视孔盖螺钉直径
length_1 = 0.0  # 机体外壁至轴承座断面的距离
delta_1 = 0.0  # 大齿轮顶圆与机体内壁的距离
delta_2 = 0.0  # 齿轮端面与机体内壁的距离


# def shaft_about():


def structure_design():

    global base_wall_thickness, hood_wall_thickness, base_flange_thickness, hood_flange_thickness, \
        foundation_flange_thickness, base_rib_thickness, hood_rib_thickness, bearing_cover_diameter, \
        foundation_bolt_d, foundation_bolt_n, foundation_bolt_seat_d, \
        foundation_bolt_PTH_d, foundation_flange_c1, foundation_flange_c2, \
        bearing_connection_bolt_d, bearing_connection_bolt_seat_d, \
        bearing_connection_bolt_PTH_d, bearing_connection_flange_c1, bearing_connection_flange_c2, \
        shell_connection_bolt_d, shell_connection_bolt_seat_d, \
        shell_connection_bolt_PTH_d, shell_connection_flange_c1, shell_connection_flange_c2, \
        dowel_pin_d, bearing_cover_bolt_d, seeker_cover_bolt_d, length_1, delta_1, delta_2, boss_radius

    # 初步计算参数
    base_wall_thickness = 0.03 * center_distance if 0.03 * center_distance >= 8 else 8
    hood_wall_thickness = 0.85 * base_wall_thickness if 0.85 * base_wall_thickness >= 8 else 8
    base_flange_thickness = 1.5 * base_wall_thickness
    hood_flange_thickness = 1.5 * hood_wall_thickness
    foundation_flange_thickness = 2.5 * base_wall_thickness
    base_rib_thickness = np.ceil(0.85 * base_wall_thickness)
    hood_rib_thickness = np.ceil(0.85 * hood_wall_thickness)

    # 地脚螺钉参数
    if center_distance > 100:
        if center_distance > 200:
            if center_distance > 250:
                if center_distance > 350:
                    foundation_bolt_d = 30
                    foundation_bolt_PTH_d = 40
                    foundation_bolt_seat_d = 85
                    foundation_flange_c1 = 50
                    foundation_flange_c2 = 50
                else:
                    foundation_bolt_d = 24
                    foundation_bolt_PTH_d = 30
                    foundation_bolt_seat_d = 60
                    foundation_flange_c1 = 35
                    foundation_flange_c2 = 30
            else:
                foundation_bolt_d = 20
                foundation_bolt_PTH_d = 25
                foundation_bolt_seat_d = 48
                foundation_flange_c1 = 30
                foundation_flange_c2 = 25
        else:
            foundation_bolt_d = 16
            foundation_bolt_PTH_d = 20
            foundation_bolt_seat_d = 45
            foundation_flange_c1 = 25
            foundation_flange_c2 = 23
    else:
        foundation_bolt_d = 12
        foundation_bolt_PTH_d = 15
        foundation_bolt_seat_d = 32
        foundation_flange_c1 = 22
        foundation_flange_c2 = 20
    foundation_bolt_n = 4 if center_distance <= 250 else 6

    # 轴承旁连接螺栓参数
    bearing_connection_bolt_cal_d = 0.75 * foundation_bolt_d
    for i in range(7):
        bearing_connection_bolt_d = Standard_reducer_con_bolt[0][i]
        bearing_connection_bolt_PTH_d = Standard_reducer_con_bolt[1][i]
        bearing_connection_bolt_seat_d = Standard_reducer_con_bolt[2][i]
        bearing_connection_flange_c1 = Standard_reducer_con_bolt[3][i]
        bearing_connection_flange_c2 = Standard_reducer_con_bolt[4][i]
        if Standard_reducer_con_bolt[0][i] > bearing_connection_bolt_cal_d:
            break

    # 机座机盖连接螺栓参数
    shell_connection_bolt_cal_d = 0.6 * foundation_bolt_d
    for i in range(7):
        shell_connection_bolt_d = Standard_reducer_con_bolt[0][i]
        shell_connection_bolt_PTH_d = Standard_reducer_con_bolt[1][i]
        shell_connection_bolt_seat_d = Standard_reducer_con_bolt[2][i]
        shell_connection_flange_c1 = Standard_reducer_con_bolt[3][i]
        shell_connection_flange_c2 = Standard_reducer_con_bolt[4][i]
        if Standard_reducer_con_bolt[0][i] > shell_connection_bolt_cal_d:
            break

    # 其余参数
    dowel_pin_d = np.ceil(0.7 * shell_connection_bolt_d)
    bearing_cover_bolt_d = np.ceil(0.4 * foundation_bolt_d)
    seeker_cover_bolt_d = np.ceil(0.3 * foundation_bolt_d)
    length_1 = shell_connection_flange_c1 + shell_connection_flange_c2 + 6
    delta_1 = np.ceil(1.2 * base_wall_thickness)
    delta_2 = base_wall_thickness if 10 <= base_wall_thickness <= 15 else (10 if base_wall_thickness < 10 else 15)
    boss_radius = shell_connection_flange_c2

    print("以下是机体结构计算部分")
    print("·机箱尺寸")
    print("  机座壁厚为: %.2f" % base_wall_thickness)
    print("  机盖壁厚为: %.2f" % hood_wall_thickness)
    print("  机座 / 机盖 / 机器底座凸缘厚为: %.2f / %.2f / %.2f" % (base_flange_thickness, hood_wall_thickness,
                                                        foundation_flange_thickness))
    print("  机座 / 机盖肋板厚为: %.2f , %.2f" % (base_rib_thickness, hood_rib_thickness))
    print("  轴承旁凸台半径为: %.2f" % bearing_cover_bolt_d)
    print("  轴承盖外径为: %.2f" % boss_radius)
    print("·地脚螺钉尺寸")
    print("  直径: %.2f" % foundation_bolt_d)
    print("  数量: %.2f" % foundation_bolt_n)
    print("  通孔直径: %.2f" % foundation_bolt_PTH_d)
    print("  沉头座直径: %.2f" % foundation_bolt_seat_d)
    print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (foundation_flange_c1, foundation_flange_c2))
    print("·轴承旁连接螺栓尺寸")
    print("  直径: %.2f" % bearing_connection_bolt_d)
    print("  通孔直径: %.2f" % bearing_connection_bolt_PTH_d)
    print("  沉头座直径: %.2f" % bearing_connection_bolt_seat_d)
    print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (bearing_connection_flange_c1, bearing_connection_flange_c2))
    print("·机座机盖连接螺栓尺寸")
    print("  直径: %.2f" % shell_connection_bolt_d)
    print("  通孔直径: %.2f" % shell_connection_bolt_PTH_d)
    print("  沉头座直径: %.2f" % shell_connection_bolt_seat_d)
    print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (shell_connection_flange_c1, shell_connection_flange_c2))
    print("·吊环螺钉尺寸")
    print("·其它组件")
    print("  定位销直径: %.2f" % dowel_pin_d)
    print("  轴承盖螺钉直径: %.2f" % bearing_cover_bolt_d)
    print("  窥视孔盖螺钉直径: %.2f" % seeker_cover_bolt_d)
    print("  机体外壁至轴承座端面的距离: %.2f" % length_1)
    print("  大齿轮顶圆与机体内壁的距离: %.2f" % delta_1)
    print("  齿轮端面与机体内壁的距离: %.2f" % delta_2)
    print("------------------机箱结构运算已结束-------------------")


def machine_about_output():

    global base_wall_thickness, hood_wall_thickness, base_flange_thickness, hood_flange_thickness, \
        foundation_flange_thickness, base_rib_thickness, hood_rib_thickness, bearing_cover_diameter, \
        foundation_bolt_d, foundation_bolt_n, foundation_bolt_seat_d, \
        foundation_bolt_PTH_d, foundation_flange_c1, foundation_flange_c2, \
        bearing_connection_bolt_d, bearing_connection_bolt_seat_d, \
        bearing_connection_bolt_PTH_d, bearing_connection_flange_c1, bearing_connection_flange_c2, \
        shell_connection_bolt_d, shell_connection_bolt_seat_d, \
        shell_connection_bolt_PTH_d, shell_connection_flange_c1, shell_connection_flange_c2, \
        dowel_pin_d, bearing_cover_bolt_d, seeker_cover_bolt_d, length_1, delta_1, delta_2, boss_radius

    config["Machine"]["base_wall_thickness"] = str(base_wall_thickness)
    config["Machine"]["base_wall_thickness"] = str(hood_wall_thickness)
    config["Machine"]["base_wall_thickness"] = str(base_flange_thickness)
    config["Machine"]["base_wall_thickness"] = str(hood_flange_thickness)
    config["Machine"]["base_wall_thickness"] = str(foundation_flange_thickness)
    config["Machine"]["base_wall_thickness"] = str(base_rib_thickness)
    config["Machine"]["base_wall_thickness"] = str(hood_rib_thickness)
    config["Machine"]["base_wall_thickness"] = str(boss_radius)
    config["Machine"]["base_wall_thickness"] = str(bearing_cover_diameter)
    config["Machine"]["base_wall_thickness"] = str(foundation_bolt_d)
    config["Machine"]["base_wall_thickness"] = str(foundation_bolt_n)
    config["Machine"]["base_wall_thickness"] = str(foundation_bolt_PTH_d)
    config["Machine"]["base_wall_thickness"] = str(foundation_bolt_seat_d)
    config["Machine"]["base_wall_thickness"] = str(foundation_flange_c1)
    config["Machine"]["base_wall_thickness"] = str(foundation_flange_c2)
    config["Machine"]["base_wall_thickness"] = str(bearing_connection_bolt_d)
    config["Machine"]["base_wall_thickness"] = str(bearing_connection_bolt_PTH_d)
    config["Machine"]["base_wall_thickness"] = str(bearing_connection_bolt_seat_d)
    config["Machine"]["base_wall_thickness"] = str(bearing_connection_flange_c1)
    config["Machine"]["base_wall_thickness"] = str(bearing_connection_flange_c2)
    config["Machine"]["base_wall_thickness"] = str(shell_connection_bolt_d)
    config["Machine"]["base_wall_thickness"] = str(shell_connection_bolt_PTH_d)
    config["Machine"]["base_wall_thickness"] = str(shell_connection_bolt_seat_d)
    config["Machine"]["base_wall_thickness"] = str(shell_connection_flange_c1)
    config["Machine"]["base_wall_thickness"] = str(shell_connection_flange_c2)
    config["Machine"]["base_wall_thickness"] = str(dowel_pin_d)
    config["Machine"]["base_wall_thickness"] = str(bearing_cover_bolt_d)
    config["Machine"]["base_wall_thickness"] = str(seeker_cover_bolt_d)
    config["Machine"]["base_wall_thickness"] = str(length_1)
    config["Machine"]["base_wall_thickness"] = str(delta_1)
    config["Machine"]["base_wall_thickness"] = str(delta_2)


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
    center_distance = float(config["Gear"]["center_distance"])

    # 导入标准连接螺栓
    Standard_reducer_con_bolt = pd.read_excel('./all_sheets/Standard_reducer_con_bolt.xls', sheet_name="Sheet1")
    train_data = np.array(Standard_reducer_con_bolt)
    Standard_reducer_con_bolt = train_data.tolist()

    # # 将数据输出到可视文件中
    # output_file = open("Calculated_Data.txt", mode='w+')
    # temp = sys.stdout
    # sys.stdout = output_file
    # 程序运行
    structure_design()
    # # 返回输出状态
    # sys.stdout = temp
    # output_file.close()
