from xugu_i2c import I2C
i2c = I2C(0x08)
data = i2c.read()
print(data)
