# -*- coding: utf-8 -*-
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from pymata_aio.private_constants import PrivateConstants
import serial
import time
import logging
import inspect
import subprocess
import time
A0 = "a0"
A1 = "a1"
A2 = "a2"
A3 = "a3"
A4 = "a4"
A5 = "a5"
D1 = "d1"
D2 = "d2"
D3 = "d3"
D4 = "d4"
D5 = "d5"
D6 = "d6"
D7 = "d7"
D8 = "d8"
D9 = "d9"
D10 = "d10"
D11 = "d11"
D12 = "d12"
D13 = "d13"
#board = PyMata3(arduino_wait=2, com_port="/dev/ttyS1", log_output=False)


def check_pin_num(pin_num):
    """
    :param pin_num:
    :return: pin_num
    """
    if not isinstance(pin_num, str):
        try:
            pin_num = str(pin_num)
        except TypeError:
            raise InvalidTypeError("invalid pin num")
    pin_num = pin_num.lower()
    if pin_num.isdigit():
        # 如果传入的针脚是数字
        pin_num = int(pin_num)
    elif pin_num.startswith("d"):
        try:
            pin_num = int(pin_num[1:])
        except TypeError:
            raise InvalidTypeError("invalid pin num")
    elif pin_num.startswith("a"):
        try:
            pin_num = int(pin_num[1:])+14
        except TypeError:
            raise InvalidTypeError("invalid pin num")
    else:
        raise InvalidTypeError("invalid pin num")
    
    return pin_num
class LED:
    """
    led灯对象
    """
    def __init__(self, pin_num):
        """
        :param pin_num: 数字针脚编号，范围0~19
        """
        pin_num = check_pin_num(pin_num)
        self.pin_num = pin_num
        # 针脚设置为输出模式，数字信号类型
        board.set_pin_mode(pin_num, Constants.OUTPUT)

    def on(self):
        """
        点亮灯的方法
        :return: 
        """
        # 给针脚一个高电位，灯会点亮
        board.digital_write(self.pin_num, 1)

    def high(self):
        """
        置高电位
        :return:
        """
        board.digital_write(self.pin_num, 1)

    def off(self):
        """
        熄灭灯的方法
        :return: 
        """
        # 给针脚一个低电位，灯会熄灭
        board.digital_write(self.pin_num, 0)

    def low(self):
        """
        置低电位
        :return:
        """
        board.digital_write(self.pin_num, 0)

class Pin:
    """
    阵脚对象
    """
    IN = Constants.INPUT
    OUT = Constants.OUTPUT
    PWM = Constants.PWM
    ANALOG = Constants.ANALOG
    def __init__(self, pin_num, pin_model):
        """
        :param pin_num: 针脚，以a开头的表示为模拟信号针脚，已d开头的表示为数字信号针脚,编号范围0~19
        :param pin_model: 接受INPUT或者OUTPUT类型
        """
        pin_num = check_pin_num(pin_num)
        self.pin_num = pin_num
        self.pin_model = pin_model
        board.set_pin_mode(self.pin_num, self.pin_model)
        
    def read_digital(self):
        """
        获取数字信号电位值
        :return: 
        """
        return board.digital_read(self.pin_num)
        
    def write_digital(self, value):
        """
        设置数字信号电位值
        :return:
        """
        board.digital_write(self.pin_num, value)
        
    def read_analog(self):
        """
        获取模拟信号电位值
        :return: 
        """
        pin_num = self.pin_num - 14
        board.set_pin_mode(pin_num, Pin.ANALOG)
        board.sleep(1)
        return board.analog_read(pin_num)
        
    def write_analog(self, value):
        """
        设置模拟电位值
        :return
        """
        board.servo_config(self.pin_num)
        board.analog_write(self.pin_num, value)
 


class Servo:
    """
    舵机对象
    """
    def __init__(self, pin_num):
        """
        :param pin_num: 接入舵机的针脚编号，编号范围0~19
        """
        pin_num = check_pin_num(pin_num)
        self.pin_num = pin_num
        board.servo_config(pin_num)

    def write_angle(self, value):
        """
        舵机转动方法
        :param angle: 舵机转动角度
        :return: 
        """
        try:
            angle = int(value)
        except ValueError:
            raise InvalidValueError("invalid angle")
        board.analog_write(self.pin_num, value)

class I2C:
    """
    I2C设备
    """
    def __init__(self, read_delay_time=0):
        """
        :param read_delay_time: i2c延迟时间
        :return
        """
        # i2c设备初始化
        self.i2c = board.i2c_config(read_delay_time)

    def readfrom(self, address, register, read_byte=2,\
            read_type=Constants.I2C_READ_CONTINUOUSLY, cb=None, cb_type=None):
        """
        :param address: i2c设备的一个地址
        :param register: i2c设备某个地址的寄存器
        :param read_byte: 一次读取的字节数量
        :param read_type: Constants.I2C_READ, Constants.I2C_READ_CONTINUOUSLY或Constants.I2C_STOP_READING
        :param cb: 可选的回调引用
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call或Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :return: data
        """
        # 向i2c的一个地址发送一个信号
        # board.i2c_write_request(addr, Constants.I2C_READ_CONTINUOUSLY)
        time.sleep(0.5)
        # 读取这个地址的寄存器中缓存的数据
        board.i2c_read_request(address, register, read_byte, \
                read_type, cb, cb_type)
        time.sleep(0.5)
        # 获取该地址中的数据
        data = board.i2c_read_data(address)
        return data

    def writeto(self, address, args):
        """
        :param address: i2c设备的一个地址
        :param args: 要发送到设备的可变字节数,作为列表传入
        :return:
        """
        board.i2c_write_request(address, args)

class XuguLog:
    """
    xugu 日志对象，自动生成一个日志文件，该文件名为主函数文件名，后缀自动改为log
    """
    def __init__(self, filename):
        format = logging.Formatter('%(message)s')
        self.logger = logging.getLogger('xuguglog')
        #log_name = inspect.stack()[-1][1]
        handler = logging.FileHandler(filename, mode="w")
        handler.setFormatter(format)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
 

    def write(self, value):
        """
        向日志文件写入数据
        :param value:
        :return:
        """
        self.logger.debug(value)

class SerialMgt:
    """
    封装串口对象
    """
    def __init__(self, port='/dev/ttyS1', baudrate=115200):
        """
        :param port: 虚谷连接PC的串口号，默认是'/dev/ttyS2'
        :param baudrate: 串口号速率，默认是115200
        """
        self.ser = serial.Serial(port=port, baudrate=baudrate,
                                 bytesize=8, timeout=5)

    def read(self, bytes=100):
        """
        从串口读取数据
        :param bytes: 读取字节数
        :return: 如果串口是打开状态，返回读取到的字节，如果是关闭的，返回空
        """
        if self.ser.isOpen():
            return self.ser.read(bytes)
        else:
            return None

    def write(self, data):
        """
        向串口写数据
        :param data: 写入的数据
        :return: 如果串口是打开状态，返回True，如果是关闭的，返回False
        """
        if self.ser.isOpen():
            self.ser.write(data)
            return True
        else:
            return False

def sleep_ms(microseconds):
    """
    封装睡眠函数，接受毫秒
    :param microseconds: 毫秒
    :return:
    """
    time.sleep(microseconds / 1000)

def arduino_burn():
    """
    :return:
    """
    subprocess.call("/home/scope/software/virtual_udisk/scripts/arduino_burn.sh /home/scope/software/resource/StandardFirmata.ino /home/scope/software/log/arduino_burn_log.txt", shell=True)

def check_firmata(port="/dev/ttyS1", baud_rate=57600):
    """
    检测是否支持firmata协议
    :return:
    """
    arduino = serial.Serial(port, baud_rate, timeout=1, writeTimeout=0)
    arduino.close()
    time.sleep(1)
    arduino.open()
    time.sleep(1)

    arduino.write(b'\xf0' + b'\x69' + b'\xf7')    

    _start = False
    recv_info = []
    for i in range(100):
        if arduino.inWaiting():
            data = arduino.read()
            if data == b"\xf0":
                _start = True
            if _start:
                recv_info.append(data)
                if data == b"\xf7":
                    break
        else:
            time.sleep(0.1)
    """
    23 for atmel, 25 for lgt
    """
    if len(recv_info) in [23,25]:
        return True
    else:
        return False

def auto_check():
    if not check_firmata():
        print("not found firmata protocol, burn it.")
        arduino_burn()
        print("burn complete")

auto_check()
board = PyMata3(arduino_wait=2, com_port="/dev/ttyS1", log_output=False)
