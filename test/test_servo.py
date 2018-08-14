from xugu import Servo

servo = Servo(1)  # 初始化1号针脚的舵机
servo.angle(60)   # 舵机转动60°
servo.angle(-40)  # 舵机反方法转动40°
servo.speed(40)   # 舵机持续转动，每次转动40°