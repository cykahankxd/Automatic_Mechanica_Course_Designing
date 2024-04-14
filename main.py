import configparser as cp
import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import messagebox

import ttkbootstrap as ttk
import scripts.electric_motor
import scripts.belt
import scripts.gear
import scripts.whole_machine
import scripts.shaft


class AMCD_GUI_Class(tk.Tk):
    def __init__(self):
        super(AMCD_GUI_Class, self).__init__()
        self.iconbitmap("./cover.ico")
        self.title("机械设计课设自动机")
        self.geometry("320x320")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.notebook = Notebook(self)

        self.normal_mode = ttk.Frame(self.notebook)
        self.advanced_mode = ttk.Frame(self.notebook)

        self.notebook.add(self.normal_mode, text="基础设置")
        self.notebook.add(self.advanced_mode, text="高级选项")
        self.notebook.pack(fill=tk.BOTH, expand=1)
        # 导入config
        self.config = cp.ConfigParser()
        self.config.read("./config.ini")
        # 数据记录
        self.F_belt = float(self.config["General"]["F_belt"])  # 运输带工作拉力
        self.V_belt = float(self.config["General"]["V_belt"])  # 运输带工作速度
        self.D_roller = float(self.config["General"]["D_roller"])  # 滚筒直径
        self.high_motorspeed_tag = int(self.config["General"]["high_motorspeed_tag"])  # 是否选择高速优先
        self.efficiency_belt = float(self.config["General"]["efficiency_belt"])  # V带传输效率
        self.efficiency_bearing = float(self.config["General"]["efficiency_bearing"])  # 轴承传输效率
        self.efficiency_gear = float(self.config["General"]["efficiency_gear"])  # 齿轮传输效率
        self.efficiency_coupling = float(self.config["General"]["efficiency_coupling"])  # 联轴器传输效率
        self.efficiency_roller = float(self.config["General"]["efficiency_roller"])  # 滚筒传输效率
        self.work_time_everyday = float(self.config["General"]["work_time_everyday"])  # 每日工作时长
        self.heavy_load_tag = int(self.config["General"]["heavy_load_tag"])  # 起动是否重载
        self.load_change_level = int(self.config["General"]["load_change_level"])  # 载荷变化幅度
        self.highspeed_gear_material = self.config["Gear"]["highspeed_gear_material"]  # 小齿轮材料倾向
        self.lowspeed_gear_material = self.config["Gear"]["lowspeed_gear_material"]  # 大齿轮材料倾向
        self.efficiency_total = self.efficiency_belt * (
                self.efficiency_bearing ** 3) * self.efficiency_gear * self.efficiency_coupling * self.efficiency_roller  # 总传动效率
        # 基础设置
        tk.Label(self.normal_mode, text="运输带工作拉力F", font=("微软雅黑", 10)).grid(row=1, column=1)
        self.F_belt_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.F_belt_entry.insert(0, str(self.F_belt))
        self.F_belt_entry.grid(row=1, column=2)

        tk.Label(self.normal_mode, text="运输带工作速度V", font=("微软雅黑", 10)).grid(row=2, column=1)
        self.V_belt_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.V_belt_entry.insert(0, str(self.V_belt))
        self.V_belt_entry.grid(row=2, column=2)

        tk.Label(self.normal_mode, text="滚筒直径D", font=("微软雅黑", 10)).grid(row=3, column=1)
        self.D_roller_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.D_roller_entry.insert(0, str(self.D_roller))
        self.D_roller_entry.grid(row=3, column=2)

        tk.Label(self.normal_mode, text="带轮效率", font=("微软雅黑", 10)).grid(row=4, column=1)
        self.efficiency_belt_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.efficiency_belt_entry.insert(0, str(self.efficiency_belt))
        self.efficiency_belt_entry.grid(row=4, column=2)

        tk.Label(self.normal_mode, text="轴承效率", font=("微软雅黑", 10)).grid(row=5, column=1)
        self.efficiency_bearing_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.efficiency_bearing_entry.insert(0, str(self.efficiency_bearing))
        self.efficiency_bearing_entry.grid(row=5, column=2)

        tk.Label(self.normal_mode, text="齿轮效率", font=("微软雅黑", 10)).grid(row=6, column=1)
        self.efficiency_gear_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.efficiency_gear_entry.insert(0, str(self.efficiency_gear))
        self.efficiency_gear_entry.grid(row=6, column=2)

        tk.Label(self.normal_mode, text="联轴器效率", font=("微软雅黑", 10)).grid(row=7, column=1)
        self.efficiency_coupling_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.efficiency_coupling_entry.insert(0, str(self.efficiency_coupling))
        self.efficiency_coupling_entry.grid(row=7, column=2)

        tk.Label(self.normal_mode, text="滚筒效率", font=("微软雅黑", 10)).grid(row=8, column=1)
        self.efficiency_roller_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.efficiency_roller_entry.insert(0, str(self.efficiency_roller))
        self.efficiency_roller_entry.grid(row=8, column=2)

        tk.Label(self.normal_mode, text="每日工作时长", font=("微软雅黑", 10)).grid(row=9, column=1)
        self.work_time_everyday_entry = tk.Entry(self.normal_mode, font=("微软雅黑", 10))
        self.work_time_everyday_entry.insert(0, str(self.work_time_everyday))
        self.work_time_everyday_entry.grid(row=9, column=2)

        tk.Button(self.normal_mode, text="保存数据", font=("微软雅黑", 10), command=self.save_config).grid(row=10, column=1)
        tk.Button(self.normal_mode, text="开始运算", font=("微软雅黑", 10), command=self.cal_start).grid(row=10, column=2)
        # 高级设置
        self.heavy_load_tag_tmp = tk.IntVar()
        self.heavy_load_tag_check = tk.Checkbutton(self.advanced_mode, variable=self.heavy_load_tag_tmp,
                                                   text="装置起动是否重载",
                                                   font=("微软雅黑", 10), onvalue=1, offvalue=0,
                                                   command=self.heavy_load_confirm)
        self.heavy_load_tag_check.grid(row=1, column=1, sticky='w')

        tk.Label(self.advanced_mode, text="载荷变动幅度", font=("微软雅黑", 10)).grid(
            row=2, column=1, sticky='w')
        self.load_change_level_tmp = tk.IntVar()
        self.load_change_level_tmp.set(self.load_change_level)
        tk.Radiobutton(self.advanced_mode, variable=self.load_change_level_tmp,
                       text="平稳", value=0).grid(row=2, column=2, sticky='w')
        tk.Radiobutton(self.advanced_mode, variable=self.load_change_level_tmp,
                       text="小", value=1).grid(row=3, column=2, sticky='w')
        tk.Radiobutton(self.advanced_mode, variable=self.load_change_level_tmp,
                       text="较大", value=2).grid(row=4, column=2, sticky='w')
        tk.Radiobutton(self.advanced_mode, variable=self.load_change_level_tmp,
                       text="很大", value=3).grid(row=5, column=2, sticky='w')

        tk.Label(self.advanced_mode, text="小齿轮材料选择", font=("微软雅黑", 10)).grid(row=6, column=1, sticky='w')
        self.highspeed_gear_material_tmp = tk.StringVar()
        self.highspeed_gear_material_tmp.set(self.highspeed_gear_material)
        tk.Radiobutton(self.advanced_mode, variable=self.highspeed_gear_material_tmp,
                       text="45钢淬火+回火", value="45 quenched and tempered").grid(row=6, column=2, sticky='w')
        tk.Radiobutton(self.advanced_mode, variable=self.highspeed_gear_material_tmp,
                       text="45钢正火", value="45 normalizing").grid(row=7, column=2, sticky='w')

        tk.Label(self.advanced_mode, text="大齿轮材料选择", font=("微软雅黑", 10)).grid(row=8, column=1, sticky='w')
        self.lowspeed_gear_material_tmp = tk.StringVar()
        self.lowspeed_gear_material_tmp.set(self.lowspeed_gear_material)
        tk.Radiobutton(self.advanced_mode, variable=self.lowspeed_gear_material_tmp,
                       text="45钢淬火+回火", value="45 quenched and tempered").grid(row=8, column=2, sticky='w')
        tk.Radiobutton(self.advanced_mode, variable=self.lowspeed_gear_material_tmp,
                       text="45钢正火", value="45 normalizing").grid(row=9, column=2, sticky='w')

        tk.Button(self.advanced_mode, text="保存数据", font=("微软雅黑", 10), command=self.save_config).grid(
            row=10, column=1)

    def on_closing(self):
        if messagebox.askokcancel("退出", "要退出程序吗"):
            self.destroy()

    def heavy_load_confirm(self):
        self.heavy_load_tag = self.heavy_load_tag_tmp.get()

    def save_config(self):  # 记录数据并导出，用作后续运算
        self.config["General"]["F_belt"] = self.F_belt_entry.get()
        self.config["General"]["V_belt"] = self.V_belt_entry.get()
        self.config["General"]["D_roller"] = self.D_roller_entry.get()
        self.config["General"]["efficiency_belt"] = self.efficiency_belt_entry.get()
        self.config["General"]["efficiency_bearing"] = self.efficiency_bearing_entry.get()
        self.config["General"]["efficiency_gear"] = self.efficiency_gear_entry.get()
        self.config["General"]["efficiency_coupling"] = self.efficiency_coupling_entry.get()
        self.config["General"]["efficiency_roller"] = self.efficiency_roller_entry.get()
        self.config["General"]["work_time_everyday"] = self.work_time_everyday_entry.get()
        self.config["General"]["heavy_load_tag"] = str(self.heavy_load_tag)
        self.config["General"]["load_change_level"] = str(self.load_change_level_tmp.get())
        self.config["Gear"]["highspeed_gear_material"] = self.highspeed_gear_material_tmp.get()
        self.config["Gear"]["lowspeed_gear_material"] = self.lowspeed_gear_material_tmp.get()
        # 再次计算总传动效率
        try:
            self.efficiency_total = self.efficiency_belt * (self.efficiency_bearing ** 3) * \
                                    self.efficiency_gear * self.efficiency_coupling * self.efficiency_roller  # 总传动效率
        except:
            messagebox.showerror("错误", "输入数据有误！")
            return
        self.config["General"]["efficiency_total"] = str(self.efficiency_total)
        with open("./config.ini", "w") as configfile:
            self.config.write(configfile)

    def cal_start(self):
        self.save_config()
        scripts.electric_motor.electric_motor_start()
        scripts.belt.belt_start()
        scripts.gear.gear_start()
        scripts.whole_machine.whole_machine_start()
        scripts.shaft.shaft_start()
        messagebox.askokcancel("", "已完成运算！")


def gui_start():
    local_gui = AMCD_GUI_Class()
    local_gui.mainloop()


if __name__ == "__main__":
    # gui启动
    gui_start()
