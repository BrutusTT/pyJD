import StringIO
import socket
import cv2
import numpy as np


EMSG_ROBOT_NOT_FOUND = 'Could not connect to the robot at %s:%s'


class EZBv4Video(object):

    # Default IP Address and Port for the JD Humanoid Robot.
    ConnectedEndPointAddress    = '192.168.1.1'
    ConnectedEndPointPort       = 24


    Res160x120              = 0
    Res320x240              = 1
    Res640x480              = 2

    START                   = 3
    STOP                    = 4

    RESERVED_compression    = 10
    RESERVED_brightness     = 11
    FreqAuto                = 12
    RESERVED_ExposureMode   = 13
    RESERVED_SetReg         = 14
    RESERVED_SetRetryCount  = 15
    RESERVED_SetBufferSize  = 16

    MirrorEnable            = 21
    MirrorDisable           = 22

    Freq50hz                = 23
    Freq60hz                = 24

    BacklightOff            = 25
    BacklightOn             = 26

    IndoorAuto              = 27
    IndoorForce             = 28

    RESERVED_LED_Red        = 29
    RESERVED_LED_Green      = 30
    RESERVED_LED_Blue       = 31

    Auto0                   = 0
    Auto1                   = 1
    Auto2                   = 2
    Auto3                   = 3
    Auto4                   = 4

    BlacknWhite             = 0x18
    ColorNegative           = 0x40
    BlacknWhiteNegative     = 0x58
    Normal                  = 0x00

    BUFFER_SIZE             = 1024


    def __init__(self, ip = ConnectedEndPointAddress, port = ConnectedEndPointPort):
        self.ip          = ip
        self.port        = port
        self.sock        = None
        self.isConnected = False
        self.connect()


    def connect(self):
        try:
            self.sock = socket.create_connection((self.ip, self.port), timeout = 3000)
            self.isConnected = True
        except:
            raise RuntimeError(EMSG_ROBOT_NOT_FOUND % (self.ip, self.port))


    def getImage(self):

        chunks = []
        bytes_recd = 0
        while bytes_recd < EZBv4Video.BUFFER_SIZE:
            chunk = self.sock.recv(min(EZBv4Video.BUFFER_SIZE - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return ''.join(chunks)


    def getImages(self):

        chunks       = []
        foundStart   = False
        self.stopped = False

        self.sock.send(bytearray([EZBv4Video.START]))

        while not self.stopped:

            self.sock.send(bytearray([EZBv4Video.Res160x120]))

            # fill the buffer
            chunk = self.sock.recv(EZBv4Video.BUFFER_SIZE)
            if chunk == '':
                raise RuntimeError("socket connection broken")

            # try to find image start
            try:
                foundStart = chunk.index('EZIMG')
            except ValueError:
                foundStart = -1

            # if image start was found let the image start with the magic numbers
            if foundStart == -1:
                chunks.append(chunk)

            else:

                # append to prev image
                chunks.append(chunk[:foundStart])

                # process buffer
                self.processImage(''.join(chunks))

                # create new buffer
                chunks     = [ chunk[foundStart:] ]

        self.sock.close()
        self.isConnected = False


    @staticmethod
    def createOpencvImageFromStringio(img_stream, cv2_img_flag = 0):
        img_stream.seek(0)
        return cv2.imdecode( np.asarray(bytearray(img_stream.read()), dtype = np.uint8),
                             cv2_img_flag )


    def processImage(self, _buffer):

        # not an image
        if not _buffer.startswith('EZIMG'):
            return

        image = self.createOpencvImageFromStringio(StringIO.StringIO(_buffer[9:]), 1)
        self.openCVImageHook(image)


    @staticmethod
    def openCVImageHook(image):
        cv2.imshow('JD', image)

        # stop if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass


    def __del__(self):
        if self.isConnected and self.sock:
            self.sock.close()
