import time

from xugu import *


p = Pin(A2, Pin.INPUT) # 初始化2号数字信号针脚，设置为输入模式
while 1:
     print(p.value())  #读取针脚电位值
     time.sleep(1)