from xugu import * #导入xugu库
import time #导入时间模块
pin = Pin(7,Pin.OUT) #选择soc控制引脚
test = 20 #计数
l = [0,1] #IO口高低电平列表
while test > 0:
	pin.write_digital(l[0]) #默认写入列表的第一个参数
	l = l[: : -1] #列表参数交换
	time.sleep(1) #休眠一秒
	test-=1 #计数自减1
