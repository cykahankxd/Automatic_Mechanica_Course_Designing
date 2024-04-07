import configparser as cp
import pandas as pd
import numpy as np
import sys


class whole_machine_compress:

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
        self.center_distance = float(self.config["Gear"]["center_distance"])
        self.base_wall_thickness = 0.0  # 机座壁厚
        self.hood_wall_thickness = 0.0  # 机盖壁厚
        self.base_flange_thickness = 0.0  # 机座凸缘厚
        self.hood_flange_thickness = 0.0  # 机盖凸缘厚
        self.foundation_flange_thickness = 0.0  # 基底凸缘厚
        self.base_rib_thickness = 0.0  # 机座肋厚
        self.hood_rib_thickness = 0.0  # 机盖肋厚
        self.boss_height = 0.0  # 轴承旁凸台高度
        self.boss_radius = 0.0  # 轴承旁凸台半径
        self.foundation_bolt_d = 0.0  # 地脚螺钉直径
        self.foundation_bolt_n = 0.0  # 地脚螺钉数目
        self.foundation_bolt_PTH_d = 0.0  # 地脚螺钉通孔直径
        self.foundation_bolt_seat_d = 0.0  # 地脚螺钉沉头座直径
        self.foundation_flange_c1 = 0.0  # 底座凸缘尺寸
        self.foundation_flange_c2 = 0.0
        self.bearing_connection_bolt_d = 0.0  # 轴承旁连接螺栓直径
        self.bearing_connection_bolt_PTH_d = 0.0  # 连接螺栓通孔直径
        self.bearing_connection_bolt_seat_d = 0.0  # 连接螺栓沉头座直径
        self.bearing_connection_flange_c1 = 0.0  # 凸缘尺寸
        self.bearing_connection_flange_c2 = 0.0
        self.shell_connection_bolt_d = 0.0  # 机座机盖旁连接螺栓直径
        self.shell_connection_bolt_PTH_d = 0.0  # 连接螺栓通孔直径
        self.shell_connection_bolt_seat_d = 0.0  # 连接螺栓沉头座直径
        self.shell_connection_l = 175  # 螺栓间距
        self.shell_connection_flange_c1 = 0.0  # 凸缘尺寸
        self.shell_connection_flange_c2 = 0.0
        self.dowel_pin_d = 0.0  # 定位销直径
        self.bearing_cover_bolt_d = 0.0  # 轴承盖螺钉直径
        self.seeker_cover_bolt_d = 0.0  # 窥视孔盖螺钉直径
        self.length_1 = 0.0  # 机体外壁至轴承座断面的距离
        self.length_2 = 0.0  # 机体内壁至轴承座断面的距离
        self.delta_1 = 0.0  # 大齿轮顶圆与机体内壁的距离
        self.delta_2 = 0.0  # 齿轮端面与机体内壁的距离

        # 导入标准连接螺栓
        Standard_reducer_con_bolt = pd.read_excel('./all_sheets/Standard_reducer_con_bolt.xls', sheet_name="Sheet1")
        train_data = np.array(Standard_reducer_con_bolt)
        self.Standard_reducer_con_bolt = train_data.tolist()
        # 导入标准国标六角头螺栓
        standard_bolt = pd.read_excel('./all_sheets/standard_bolt.xls', sheet_name="Sheet1")
        train_data = np.array(standard_bolt)
        self.standard_bolt = train_data.tolist()

        # 将数据输出到可视文件中
        output_file = open("./outputs/Calculated_Data_Whole_Machine.txt", mode='w+')
        self.output_tmp = sys.stdout
        sys.stdout = output_file

    def structure_design(self):
        # 初步计算参数
        self.base_wall_thickness = 0.03 * self.center_distance if 0.03 * self.center_distance >= 8 else 8
        self.hood_wall_thickness = 0.85 * self.base_wall_thickness if 0.85 * self.base_wall_thickness >= 8 else 8
        self.base_flange_thickness = 1.5 * self.base_wall_thickness
        self.hood_flange_thickness = 1.5 * self.hood_wall_thickness
        self.foundation_flange_thickness = 2.5 * self.base_wall_thickness
        self.base_rib_thickness = np.ceil(0.85 * self.base_wall_thickness)
        self.hood_rib_thickness = np.ceil(0.85 * self.hood_wall_thickness)

        # 地脚螺钉参数
        if self.center_distance > 100:
            if self.center_distance > 200:
                if self.center_distance > 250:
                    if self.center_distance > 350:
                        self.foundation_bolt_d = 30
                        self.foundation_bolt_PTH_d = 40
                        self.foundation_bolt_seat_d = 85
                        self.foundation_flange_c1 = 50
                        self.foundation_flange_c2 = 50
                    else:
                        self.foundation_bolt_d = 24
                        self.foundation_bolt_PTH_d = 30
                        self.foundation_bolt_seat_d = 60
                        self.foundation_flange_c1 = 35
                        self.foundation_flange_c2 = 30
                else:
                    self.foundation_bolt_d = 20
                    self.foundation_bolt_PTH_d = 25
                    self.foundation_bolt_seat_d = 48
                    self.foundation_flange_c1 = 30
                    self.foundation_flange_c2 = 25
            else:
                self.foundation_bolt_d = 16
                self.foundation_bolt_PTH_d = 20
                self.foundation_bolt_seat_d = 45
                self.foundation_flange_c1 = 25
                self.foundation_flange_c2 = 23
        else:
            self.foundation_bolt_d = 12
            self.foundation_bolt_PTH_d = 15
            self.foundation_bolt_seat_d = 32
            self.foundation_flange_c1 = 22
            self.foundation_flange_c2 = 20
        self.foundation_bolt_n = 4 if self.center_distance <= 250 else 6

        # 轴承旁连接螺栓参数
        bearing_connection_bolt_cal_d = 0.75 * self.foundation_bolt_d
        for i in range(7):
            self.bearing_connection_bolt_d = self.Standard_reducer_con_bolt[0][i]
            self.bearing_connection_bolt_PTH_d = self.Standard_reducer_con_bolt[1][i]
            self.bearing_connection_bolt_seat_d = self.Standard_reducer_con_bolt[2][i]
            self.bearing_connection_flange_c1 = self.Standard_reducer_con_bolt[3][i]
            self.bearing_connection_flange_c2 = self.Standard_reducer_con_bolt[4][i]
            if self.Standard_reducer_con_bolt[0][i] > bearing_connection_bolt_cal_d:
                break

        # 机座机盖连接螺栓参数
        shell_connection_bolt_cal_d = 0.6 * self.foundation_bolt_d
        for i in range(7):
            self.shell_connection_bolt_d = self.Standard_reducer_con_bolt[0][i]
            self.shell_connection_bolt_PTH_d = self.Standard_reducer_con_bolt[1][i]
            self.shell_connection_bolt_seat_d = self.Standard_reducer_con_bolt[2][i]
            self.shell_connection_flange_c1 = self.Standard_reducer_con_bolt[3][i]
            self.shell_connection_flange_c2 = self.Standard_reducer_con_bolt[4][i]
            if self.Standard_reducer_con_bolt[0][i] > shell_connection_bolt_cal_d:
                break

        # 其余参数
        self.dowel_pin_d = np.ceil(0.7 * self.shell_connection_bolt_d)
        self.bearing_cover_bolt_d = np.ceil(0.4 * self.foundation_bolt_d)
        for i in range(1, len(self.standard_bolt[0])):
            if self.standard_bolt[0][i] > self.bearing_cover_bolt_d:
                self.bearing_cover_bolt_d = self.standard_bolt[0][i] if abs(
                    self.bearing_cover_bolt_d - self.standard_bolt[0][i]) < \
                                                                        abs(self.bearing_cover_bolt_d -
                                                                            self.standard_bolt[0][i - 1]) else \
                                                                            self.standard_bolt[0][i - 1]
                break
        self.seeker_cover_bolt_d = np.ceil(0.3 * self.foundation_bolt_d)
        for i in range(1, len(self.standard_bolt[0])):
            if self.standard_bolt[0][i] > self.seeker_cover_bolt_d:
                self.seeker_cover_bolt_d = self.standard_bolt[0][i] if abs(
                    self.seeker_cover_bolt_d - self.standard_bolt[0][i]) < \
                                                                       abs(self.seeker_cover_bolt_d -
                                                                           self.standard_bolt[0][i - 1]) else \
                                                                           self.standard_bolt[0][i - 1]
        self.length_1 = self.shell_connection_flange_c1 + self.shell_connection_flange_c2 + 6
        self.length_2 = self.base_wall_thickness + self.length_1
        self.delta_1 = np.ceil(1.2 * self.base_wall_thickness)
        self.delta_2 = self.base_wall_thickness if 10 <= self.base_wall_thickness <= 15 else (10 if self.base_wall_thickness < 10 else 15)
        self.boss_radius = self.shell_connection_flange_c2

        print("以下是机体结构计算部分")
        print("·机箱尺寸")
        print("  机座壁厚为: %.2f" % self.base_wall_thickness)
        print("  机盖壁厚为: %.2f" % self.hood_wall_thickness)
        print("  机座 / 机盖 / 机器底座凸缘厚为: %.2f / %.2f / %.2f" % (self.base_flange_thickness, self.hood_wall_thickness,
                                                            self.foundation_flange_thickness))
        print("  机座 / 机盖肋板厚为: %.2f , %.2f" % (self.base_rib_thickness, self.hood_rib_thickness))
        print("  轴承旁凸台半径为: %.2f" % self.boss_radius)
        print("·地脚螺钉尺寸")
        print("  直径: %.2f" % self.foundation_bolt_d)
        print("  数量: %.2f" % self.foundation_bolt_n)
        print("  通孔直径: %.2f" % self.foundation_bolt_PTH_d)
        print("  沉头座直径: %.2f" % self.foundation_bolt_seat_d)
        print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (self.foundation_flange_c1, self.foundation_flange_c2))
        print("·轴承旁连接螺栓尺寸")
        print("  直径: %.2f" % self.bearing_connection_bolt_d)
        print("  通孔直径: %.2f" % self.bearing_connection_bolt_PTH_d)
        print("  沉头座直径: %.2f" % self.bearing_connection_bolt_seat_d)
        print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (self.bearing_connection_flange_c1, self.bearing_connection_flange_c2))
        print("·机座机盖连接螺栓尺寸")
        print("  直径: %.2f" % self.shell_connection_bolt_d)
        print("  通孔直径: %.2f" % self.shell_connection_bolt_PTH_d)
        print("  沉头座直径: %.2f" % self.shell_connection_bolt_seat_d)
        print("  底座凸缘尺寸1 / 2: %.2f , %.2f" % (self.shell_connection_flange_c1, self.shell_connection_flange_c2))
        print("·其它组件")
        print("  定位销直径: %.2f" % self.dowel_pin_d)
        print("  轴承盖螺钉直径: %.2f" % self.bearing_cover_bolt_d)
        print("  窥视孔盖螺钉直径: %.2f" % self.seeker_cover_bolt_d)
        print("  机体外壁至轴承座端面的距离: %.2f" % self.length_1)
        print("  机体内壁至轴承座端面的距离: %.2f" % self.length_2)
        print("  大齿轮顶圆与机体内壁的距离: %.2f" % self.delta_1)
        print("  齿轮端面与机体内壁的距离: %.2f" % self.delta_2)

    def machine_about_output(self):
        self.config["Machine"]["base_wall_thickness"] = str(self.base_wall_thickness)
        self.config["Machine"]["hood_wall_thickness"] = str(self.hood_wall_thickness)
        self.config["Machine"]["base_flange_thickness"] = str(self.base_flange_thickness)
        self.config["Machine"]["hood_flange_thickness"] = str(self.hood_flange_thickness)
        self.config["Machine"]["foundation_flange_thickness"] = str(self.foundation_flange_thickness)
        self.config["Machine"]["base_rib_thickness"] = str(self.base_rib_thickness)
        self.config["Machine"]["hood_rib_thickness"] = str(self.hood_rib_thickness)
        self.config["Machine"]["boss_radius"] = str(self.boss_radius)
        self.config["Machine"]["foundation_bolt_d"] = str(self.foundation_bolt_d)
        self.config["Machine"]["foundation_bolt_n"] = str(self.foundation_bolt_n)
        self.config["Machine"]["foundation_bolt_PTH_d"] = str(self.foundation_bolt_PTH_d)
        self.config["Machine"]["foundation_bolt_seat_d"] = str(self.foundation_bolt_seat_d)
        self.config["Machine"]["foundation_flange_c1"] = str(self.foundation_flange_c1)
        self.config["Machine"]["foundation_flange_c2"] = str(self.foundation_flange_c2)
        self.config["Machine"]["bearing_connection_bolt_d"] = str(self.bearing_connection_bolt_d)
        self.config["Machine"]["bearing_connection_bolt_PTH_d"] = str(self.bearing_connection_bolt_PTH_d)
        self.config["Machine"]["bearing_connection_bolt_seat_d"] = str(self.bearing_connection_bolt_seat_d)
        self.config["Machine"]["bearing_connection_flange_c1"] = str(self.bearing_connection_flange_c1)
        self.config["Machine"]["bearing_connection_flange_c2"] = str(self.bearing_connection_flange_c2)
        self.config["Machine"]["shell_connection_bolt_d"] = str(self.shell_connection_bolt_d)
        self.config["Machine"]["shell_connection_bolt_PTH_d"] = str(self.shell_connection_bolt_PTH_d)
        self.config["Machine"]["shell_connection_bolt_seat_d"] = str(self.shell_connection_bolt_seat_d)
        self.config["Machine"]["shell_connection_flange_c1"] = str(self.shell_connection_flange_c1)
        self.config["Machine"]["shell_connection_flange_c2"] = str(self.shell_connection_flange_c2)
        self.config["Machine"]["dowel_pin_d"] = str(self.dowel_pin_d)
        self.config["Machine"]["bearing_cover_bolt_d"] = str(self.bearing_cover_bolt_d)
        self.config["Machine"]["seeker_cover_bolt_d"] = str(self.seeker_cover_bolt_d)
        self.config["Machine"]["length_1"] = str(self.length_1)
        self.config["Machine"]["length_2"] = str(self.length_2)
        self.config["Machine"]["delta_1"] = str(self.delta_1)
        self.config["Machine"]["delta_2"] = str(self.delta_2)

        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)


def whole_machine_start():
    local_class = whole_machine_compress()
    # 程序运行
    local_class.structure_design()
    local_class.machine_about_output()
    print("▲以上部分所用螺钉均以 GB/T 5782-2000 及 GB/T 5783-2000 为设计基准，详见《机械设计课程设计》")
    print("------------------机箱结构运算已结束-------------------")
    # 返回输出状态
    sys.stdout = local_class.output_tmp
    local_class.output_tmp.close()


if __name__ == "__main__":
    whole_machine_start()
