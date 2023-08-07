import electric_motor
import tkinter as tk
import configparser as cp

class Auto_Class_Design(tk.Tk):
    def __init__(self):
        super(Auto_Class_Design, self).__init__()
        self.iconbitmap("./cover.ico")
        self.title("Class Design Auto Spawner")
        self.geometry("240x235")

    # def motor_connect(self):



if __name__ == "__main__":
    # 导入config
    config = cp.ConfigParser()
    config.read("./config.ini")
    # 数据记录
    efficiency_belt = float(config["General"]["efficiency_belt"])  # V带传输效率
    efficiency_bearing = float(config["General"]["efficiency_bearing"])  # 轴承传输效率
    efficiency_gear = float(config["General"]["efficiency_gear"])  # 齿轮传输效率
    efficiency_coupling = float(config["General"]["efficiency_coupling"])  # 联轴器传输效率
    efficiency_roller = float(config["General"]["efficiency_roller"])  # 滚筒传输效率
    # 初步计算，包括总传动效率等
    efficiency_total = efficiency_belt * (
                efficiency_bearing ** 3) * efficiency_gear * efficiency_coupling * efficiency_roller
    # 记录数据并导出，用作后续运算
    config["General"]["efficiency_total"] = efficiency_total
    with open("./config.ini", "w") as configfile:
        config.write(configfile)

