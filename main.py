import configparser as cp
import scripts.electric_motor
import scripts.belt
import scripts.gear
import scripts.whole_machine
import scripts.shaft


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
    config["General"]["efficiency_total"] = str(efficiency_total)
    with open("./config.ini", "w") as configfile:
        config.write(configfile)
    # 正式进行运算
    scripts.electric_motor.electric_motor_start()
    scripts.belt.belt_start()
    scripts.gear.gear_start()
    scripts.whole_machine.whole_machine_start()
    scripts.shaft.shaft_start()
