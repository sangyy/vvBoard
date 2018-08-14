from xugu import I2C

i2c = I2C(I2C.ANALOG, 3, 4)  # 初始化i2c设备，3号针脚作为时钟线，4号针脚作为数字线
data = i2c.read(0x42, 0x10)  # 从0x42地址的0x10寄存器读取数据