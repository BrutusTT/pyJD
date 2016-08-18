



class I2C(object):
    
    
    def __init__(self, ezb):
        self._ezb = ezb


    def writeBinary(self, deviceAddress, b7, b6, b5, b4, b3, b2, b1, b0):
        b = (b0) + (b1 * 2) + (b2 * 4) + (b3 * 8) + (b4 * 16) + (b5 * 32) + (b6 * 64) + (b7 * 128)
        self.write(deviceAddress, bytearray(b))
        

    def write(self, deviceAddress, data):
        assert isinstance(data, bytearray)

        if len(data) == 0:
            raise Exception("I2C Data for Write cannot be empty")

        if (len(data) > 255):
            raise Exception("Can not send more than 255 bytes over I2C")

        if (deviceAddress >= 128):
            writeAddress8Bit = deviceAddress;
        else:
            writeAddress8Bit = deviceAddress << 1

        ba  = bytearray()
        ba += bytearray([writeAddress8Bit])
        ba += bytearray([len(data)])
        ba += data

        self._ezb.sendCommand(0, self._ezb.CmdI2CWrite, ba);


    def read(self, deviceAddress, expectedBytesReturn):

        if (deviceAddress >= 128):
            readAddress8Bit = deviceAddress | 1
        else:
            readAddress8Bit = (deviceAddress << 1) | 1

        return self._ezb.sendCommand( expectedBytesReturn, self._ezb.CmdI2CRead, bytearray([readAddress8Bit, expectedBytesReturn]))


    def setClockSpeed(self, rate):

        if (self._ezb.EZBType != self._ezb.EZ_B_Type_Enum.ezb4):
            return

#         self._ezb.log(False, "Setting i2c rate: {0}", rate);

        ba  = bytearray()
        ba += self._ezb.CmdV4I2CClockSpeed
        
        if rate > 255:
            ba += rate >> 8
            ba += rate - (rate >> 8)
        else:
            ba += rate

        self._ezb.sendCommand(self._ezb.CmdEZBv4, ba);
