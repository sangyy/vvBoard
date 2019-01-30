from xugu_i2c import I2C
i2c = I2C(0x08)
s = i2c.read_byte()
print(s)
