from xugu_i2c import I2C
i2c = I2C(0x08)
i2c.write(b"hello")