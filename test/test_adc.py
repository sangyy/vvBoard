import time

from xugu import Pin, ADC

p = Pin(2, Pin.INPUT, Pin.ANALOG) # 初始化2号模拟信号针脚，设置为输入模式
adc = ADC(p)  # 初始话模拟信号对象
while 1:
     print(adc.read())  # 读取模拟信号电位值
     time.sleep(1)