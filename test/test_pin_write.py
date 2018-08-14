import time

from xugu import Pin

p = Pin(13, Pin.OUTPUT, Pin.DIGITAL)  # 初始化13号数字信号针脚，设置为输出模式

while 1:
     p.high()   # 给针脚设置高电位值
     time.sleep(1)
     p.low()    # 给针脚设置低电位值
     time.sleep(0.5)