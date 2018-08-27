# -*- coding: utf-8 -*-
from PyMata.pymata import PyMata
import sqlite3
import serial
import time
import logging
import inspect

__version__ = "0.1.0"


class InvalidValueError(Exception):
    """
    无效参数错误
    """
    pass


class InvalidTypeError(Exception):
    """
    无效类型错误
    """
    pass


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


def check_pin_num(pin_num):
    """

    :param pin_num:
    :return:
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
        if 0 <= pin_num <= 13:
            _pin_type = PyMata.DIGITAL
        else:
            _pin_type = PyMata.ANALOG
    elif pin_num.startswith("d"):
        # 如果针脚编号是d开头的，将针脚类型设置为DIGITAL
        _pin_type = PyMata.DIGITAL
        try:
            pin_num = int(pin_num[1:])
        except TypeError:
            raise InvalidTypeError("invalid pin num")
    elif pin_num.startswith("a"):
        # 如果针脚编号是a开头的，将针脚类型设置为ANALOG
        _pin_type = PyMata.ANALOG
        try:
            pin_num = int(pin_num[1:])
        except TypeError:
            raise InvalidTypeError("invalid pin num")
        pin_num += 14
    else:
        raise InvalidTypeError("invalid pin num")
    return pin_num, _pin_type

class LED:
    """
    led灯对象
    """

    def __init__(self, pin_num, port="/dev/ttyACM0", debug=False):
        """

        :param pin_num: 数字针脚编号，范围0~19
        :param port: 虚谷连接arduino的COM口，默认为"/dev/ttyACM0"
        :param debug: 当为True的时候，会输出debug信息
        """
        self.pin_num = pin_num
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        # 针脚设置为输出模式，数字信号类型
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
        # 给针脚一个高电位，灯会点亮
        self.board.digital_write(self.pin_num, 1)

    def high(self):
        """
        置高电位
        :return:
        """
        self.board.digital_write(self.pin_num, 1)

    def off(self):
        """
        熄灭灯的方法
        :return: 
        """
        # 给针脚一个低电位，灯会熄灭
        self.board.digital_write(self.pin_num, 0)

    def low(self):
        """
        置低电位
        :return:
        """
        self.board.digital_write(self.pin_num, 0)


class Pin:
    """
    阵脚对象
    """
    IN = PyMata.INPUT
    OUT = PyMata.OUTPUT
    PWM = PyMata.PWM
    DIGITAL = PyMata.DIGITAL
    ANALOG = PyMata.ANALOG

    def __init__(self, pin_num, pin_model, pin_type=None, port="/dev/ttyACM0",
                 debug=False):
        """

        :param pin_num: 针脚，已a开头的表示为模拟信号针脚，已d开头的表示为数字信号针脚,编号范围0~19
        :param pin_model: 接受INPUT或者OUTPUT类型
        :param port: 虚谷连接arduino的COM口，默认为"/dev/ttyACM0"
        :param debug: 当为True的时候，会输出debug信息
        """
        pin_num, _pin_type = check_pin_num(pin_num)
        if not pin_type:
            pin_type = _pin_type
        self.pin_num = pin_num
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        self.board.set_pin_mode(self.pin_num, pin_model, pin_type)

    def high(self):
        """
        输出数字信号高电位值
        :return: 
        """
        self.board.digital_write(self.pin_num, 1)

    def on(self):
        """
        设置数字信号高电位
        :return:
        """
        self.board.digital_write(self.pin_num, 1)

    def low(self):
        """
        输出数字信号低电位值
        :return: 
        """
        self.board.digital_write(self.pin_num, 0)

    def off(self):
        """
        设置数字信号为低电位值
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
        """
        :param pin:  Pin对象
        """
        self.pin = pin

    def read(self):
        return self.pin.board.analog_read(self.pin.pin_num)


class DAC:
    """
    数字信号转换模拟信号
    """

    def __init__(self, pin):
        """

        :param pin:  Pin对象
        """
        self.pin = pin

    def write(self, value):
        self.pin.board.analog_write(self.pin.pin_num, value)


class Servo:
    """
    舵机对象
    """

    def __init__(self, pin_num, port="/dev/ttyACM0", debug=False):
        """

        :param pin_num: 接入舵机的针脚编号，编号范围0~19
        :param port: 虚谷连接舵机的COM口，默认为"/dev/ttyACM0"
        :param debug: 当为True的时候，会输出debug信息
        """
        pin_num, _ = check_pin_num(pin_num)
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
        """

        :param pin_type: DIGITAL 或者 ANALOG
        :param clk_pin: 时钟总线接入的针脚
        :param data_pin: 数据总线接入的针脚
        :param port: 虚谷连接I2C设备的COM口，默认为"/dev/ttyACM0"
        :param debug: 当为True的时候，会输出debug信息
        """
        self.board = PyMata(port, bluetooth=False, verbose=debug)
        # i2c设备初始化
        self.i2c = self.board.i2c_config(0, pin_type, clk_pin, data_pin)

    def read(self, addr=0x48, register=0, read_byte=2):
        """

        :param addr: i2c设备的一个地址
        :param register: i2c设备某个地址的寄存器
        :param read_byte: 一次读取的字节数量
        :return:
        """
        # 向i2c的一个地址发送一个信号
        self.board.i2c_write(addr, PyMata.I2C_READ_CONTINUOUSLY)
        time.sleep(0.5)
        # 读取这个地址的寄存器中缓存的数据
        self.board.i2c_read(addr, register, read_byte, PyMata.I2C_READ)
        time.sleep(0.5)
        # 获取该地址中的数据
        data = self.board.i2c_get_read_data(addr)
        return data

    def write(self, value, addr=0x48, register=0):
        self.board.i2c_write(addr, addr, register, value)


class XuguLog:
    """
    xugu 日志对象，自动生成一个日志文件，该文件名为主函数文件名，后缀自动改为log
    """

    def __init__(self):
        format = logging.Formatter('%(message)s')
        self.logger = logging.getLogger('xuguglog')
        log_name = inspect.stack()[-1][1]
        handler = logging.FileHandler(log_name, mode="w")
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

    def __init__(self, port='/dev/ttyS2', baudrate=115200):
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


class S2W:
    """
    数据保存对象，提供保存数据和读取数据的静态方法
    """

    @staticmethod
    def write_data(pin_num, value):
        """
        将针脚上的值保存到sqlite中
        :param pin_num: 针脚编号，d0~d13, a0~a5
        :param value: 针脚对应的值，类型为整数
        :return:
        """
        pin_num = pin_num.lower()
        # 初始化sqlite3数据库连接，将数据文件存放到当前目录的example.db文件中
        conn = sqlite3.connect('example.db')
        # 初始化游标
        c = conn.cursor()
        # 初始化表，如果表不存在，就创建一张表
        c.execute('''CREATE TABLE IF NOT EXISTS pin_data
                              (pin_num TEXT PRIMARY KEY, data integer )''')
        # 向表中插入一条数据
        c.execute("INSERT OR REPLACE INTO pin_data VALUES (?, ?)",
                  [pin_num, value])
        # 将数据写入到文件中
        conn.commit()
        # 关闭连接
        conn.close()

    @staticmethod
    def read_value(pin_num):
        """
        从sqlite中读取针脚对应的值
        :param pin_num: 针脚编号，d0~d13, a0~a5
        :return: 针脚对应的数值
        """
        pin_num = pin_num.lower()
        conn = sqlite3.connect("example.db")
        c = conn.cursor()
        # 从表中读取针脚编号对应的数值
        c.execute("SELECT data from pin_data where pin_num=?", [pin_num])
        data = c.fetchall()
        conn.close()
        if data:
            return data[0][0]
        else:
            return None
