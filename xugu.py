# -*- coding: utf-8 -*-
from PyMata.pymata import PyMata
from flask import Flask
import sqlite3
import serial
import time


class InvalidValueError(Exception):
    pass

class InvalidTypeError(Exception):
    pass

class LED:
    """
    led灯对象
    """
    def __init__(self, pin_num, port="/dev/ttyACM0", debug=False):
        self.pin_num = pin_num
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        self.board.set_pin_mode(pin_num, self.board.OUTPUT, self.board.DIGITAL)

    def light(self, value):
        """
        控制led灯开关
        :param value: 当value==1或者True时，灯为点亮状态，当value==0或者False时，
        灯为熄灭状态
        :return: 
        """
        if value is True or value == 1:
            self.board.digital_write(self.pin_num, 1)
        elif value is False or value == 0:
            self.board.digital_write(self.pin_num, 0)
        else:
            raise InvalidValueError("invalid value")

    def on(self):
        """
        点亮灯的方法
        :return: 
        """
        self.board.digital_write(self.pin_num, 1)

    def off(self):
        """
        熄灭灯的方法
        :return: 
        """
        self.board.digital_write(self.pin_num, 0)


class Pin:
    """
    阵脚对象
    """
    INPUT = PyMata.INPUT
    OUTPUT = PyMata.OUTPUT
    DIGITAL = PyMata.DIGITAL
    ANALOG = PyMata.ANALOG

    def __init__(self, pin_num, pin_model, port="/dev/ttyACM0",
                 debug=False):
        pin_num = pin_num.lower()
        if pin_num.startswith("d"):
            pin_type = PyMata.DIGITAL
            try:
                self.pin_num = int(pin_num[1:])
            except TypeError:
                raise InvalidTypeError("invalid pin num")
        elif pin_num.startswith("a"):
            pin_type = PyMata.ANALOG
            try:
                self.pin_num = int(pin_num[1:])
            except TypeError:
                raise InvalidTypeError("invalid pin num")
            self.pin_num += 14
        else:
            raise InvalidTypeError("invalid pin num")
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        self.board.set_pin_mode(self.pin_num, pin_model, pin_type)

    def high(self):
        """
        输出数字信号高电位值
        :return: 
        """
        self.board.digital_write(self.pin_num, 1)

    def low(self):
        """
        输出数字信号低电位值
        :return: 
        """
        self.board.digital_write(self.pin_num, 0)

    def value(self):
        """
        获取数字信号电位值
        :return: 
        """
        return self.board.digital_read(self.pin_num)


class ADC:
    """
    模拟信号转换数字信号
    """
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return self.pin.board.analog_read(self.pin.pin_num)


class DAC:
    """
    数字信号转换模拟信号
    """
    def __init__(self, pin):
        self.pin = pin

    def write(self, value):
        self.pin.board.analog_write(self.pin.pin_num, value)


class Servo:
    """
    舵机对象
    """
    def __init__(self, pin_num, port="/dev/ttyACM0", debug=False):
        self.pin_num = pin_num
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        self.board.servo_config(pin_num)

    def angle(self, angle):
        """
        舵机转动方法
        :param angle: 舵机转动角度
        :return: 
        """
        self.board.analog_write(self.pin_num, angle)

    def speed(self, angle):
        """
        舵机持续转动方法
        :param angle: 舵机转动角度
        :return: 
        """
        while 1:
            self.board.analog_write(self.pin_num, angle)
            time.sleep(0.5)


class I2C:

    DIGITAL = PyMata.DIGITAL
    ANALOG = PyMata.ANALOG

    def __init__(self, pin_type, clk_pin, data_pin, port="/dev/ttyACM0",
                 debug=False):
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        self.i2c = self.board.i2c_config(0, pin_type, clk_pin, data_pin)

    def read(self, addr=0x48, register=0, read_byte=2):
        self.board.i2c_write(addr, PyMata.I2C_READ_CONTINUOUSLY)
        time.sleep(0.5)
        self.board.i2c_read(addr, register, read_byte, PyMata.I2C_READ)
        time.sleep(0.5)
        data = self.board.i2c_get_read_data(addr)
        return data

    def write(self, value, addr=0x48, register=0):
        self.board.i2c_write(addr, addr, register, value)

class SerialMgt:
    def __init__(self, port='/dev/ttyS2', baudrate=115200):
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
    time.sleep(microseconds/1000)


def save_value(pin_num, value):
    """
    将针脚上的值保存到sqlite中
    :param pin_num: 针脚编号，d0~d13, a0~a5
    :param value: 针脚对应的值，类型为整数
    :return: 
    """
    pin_num = pin_num.lower()
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pin_data
                      (pin_num TEXT PRIMARY KEY, data integer )''')
    c.execute("INSERT OR REPLACE INTO pin_data VALUES (?, ?)",[pin_num, value])
    conn.commit()
    conn.close()

def read_value(pin_num):
    """
    从sqlite中读取针脚对应的值
    :param pin_num: 针脚编号，d0~d13, a0~a5
    :return: 针脚对应的数值
    """
    pin_num = pin_num.lower()
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("SELECT data from pin_data where pin_num=?", [pin_num])
    data = c.fetchall()
    if data:
        return data[0][0]
    else:
        return None
