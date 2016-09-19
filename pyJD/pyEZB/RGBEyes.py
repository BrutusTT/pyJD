

class RGBEyes(object):

    I2C_ADDRESS     = 0xa0
    BRIGHTNESS_MAX  = 7
    BRIGHTNESS_MIN  = 0
    INDEX_MAX       = 18


    def __init__(self, ezb):
        self._ezb = ezb

        self._reds   = bytearray(RGBEyes.INDEX_MAX)
        self._greens = bytearray(RGBEyes.INDEX_MAX)
        self._blues  = bytearray(RGBEyes.INDEX_MAX)


    def setArray(self, values, I2CAddress = I2C_ADDRESS):

        data = bytearray()

        for index, (r, g, b) in enumerate(values):

            if index > 17:
                raise Exception("Index out of range for RGB Eyes ({0})".format(index))

            r = min(r, RGBEyes.BRIGHTNESS_MAX)
            g = min(g, RGBEyes.BRIGHTNESS_MAX)
            b = min(b, RGBEyes.BRIGHTNESS_MAX)

            self._reds[index]   = r
            self._greens[index] = g
            self._blues[index]  = b

            packet0 = (index << 3) | r
            packet1 = (g << 4) | b

            data += bytearray([packet0])
            data += bytearray([packet1])

        self._ezb.I2C.write(I2CAddress, data)


    def setColor(self, indexes, r, g, b, I2CAddress = I2C_ADDRESS):

        r = min(r, RGBEyes.BRIGHTNESS_MAX)
        g = min(g, RGBEyes.BRIGHTNESS_MAX)
        b = min(b, RGBEyes.BRIGHTNESS_MAX)

        data = bytearray()

        for index in indexes:

            if index > 17:
                raise Exception("Index out of range for RGB Eyes ({0})".format(index))

            self._reds[index]   = r
            self._greens[index] = g
            self._blues[index]  = b

            packet0 = (index << 3) | r
            packet1 = (g << 4) | b

            data += bytearray([packet0])
            data += bytearray([packet1])

        self._ezb.I2C.write(I2CAddress, data)
