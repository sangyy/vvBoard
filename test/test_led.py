import time

from xugu import LED

led = LED(13) # 初始化13号针脚的LED灯

while 1:
    led.on()  # 点亮LED灯
    time.sleep(1)
    led.off() # 熄灭LED灯
    time.sleep(1)
