import time

from xugu import Pin, DAC

p = Pin(2, Pin.OUTPUT, Pin.ANALOG) # 初始化2号模拟信号针脚，设置为输出模式
dac = DAC(p)  # 初始话模拟信号对象

while 1:
     dac.write(300)  # 给针脚设置电位值
     time.sleep(1)