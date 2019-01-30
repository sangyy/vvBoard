from ctypes import *


class PythonStructure(Structure):
    _fields_ = [('reg_string',c_char),('buf_string',c_char*1024)]

class I2C():
    def __init__(self,register):
        self.iic = CDLL('./libstw_i2c.so')
        self.iic.stw_i2c_open()
        self.python_structure = PythonStructure()
        self.PARAM = c_char * 2
        self.reg_string = self.PARAM()
        self.reg_string[0] = 0x00
        self.reg_string[1] = 0x00
        self.iic_address=register
    def read(self,bytes = None):
        PARAM = c_char * 1024
        buf_string = PARAM()
        if not bytes:
            buf_string = self.iic.stw_i2c_read(0x01,self.iic_address,self.reg_string,0x02,0x00,0xfe,buf_string)
            return str(c_char_p(buf_string).value).replace("\\xff","")[2:-1].encode()
        buf_string = self.iic.stw_i2c_read(0x01,self.iic_address,self.reg_string,0x02,0x00,bytes,buf_string)
        return c_char_p(buf_string).value
    def write(self,pstr):
        s = len(pstr)
        PARAM = c_char * s
        buf_string = PARAM()
        for i in range(s):
            buf_string[i] = pstr[i]
        buf_string = self.iic.stw_i2c_write(0x00,self.iic_address,self.reg_string,0x02,0x00,s ,buf_string)
    def read_byte(self):
        PARAM = c_char * 1024
        buf_string = PARAM()
        buf_string = self.iic.stw_i2c_read(0x01,self.iic_address,self.reg_string,0x02,0x00,0x01,buf_string)
        return str(c_char_p(buf_string).value).replace("\\xff","")[2:-1][0].encode()
    def write_byte(self,pstr):
        s = len(pstr)
        assert s == 1,"Only one byte can be written"
        PARAM = c_char * s
        buf_string = PARAM()
        for i in range(s):
            buf_string[i] = pstr[i]
        buf_string = self.iic.stw_i2c_write(0x00,self.iic_address,self.reg_string,0x02,0x00,1 ,buf_string)

