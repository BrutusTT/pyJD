import socket
import time

from pyJD.pyEZB.I2C     import I2C
from pyJD.pyEZB.RGBEyes import RGBEyes

EMSG_ROBOT_NOT_FOUND = 'Could not connect to the robot at %s:%s'


class EZB(object):


    # Default IP Address and Port for the JD Humanoid Robot.
    ConnectedEndPointAddress    = '192.168.1.1'
    ConnectedEndPointPort       = 23

    CmdUnknown                  = 0
    CmdReleaseAllServos         = 1
    CmdGetUniqueID              = 2
    CmdEZBv3                    = 3
    CmdEZBv4                    = 4
    CmdSoundBeep                = 5
    CmdEZServo                  = 6
    CmdI2CWrite                 = 10
    CmdI2CRead                  = 11
    CmdBootLoader               = 14
    CmdSetPWMSpeed              = 15        # +23 (38)
    CmdSetServoSpeed            = 39        # +23 (62)
    CmdPing                     = 0x55
    CmdSetDigitalPortOn         = 100       # +23 (123)
    CmdSetDigitalPortOff        = 124       # +23 (147)
    CmdGetDigitalPort           = 148       # +23 (171)
    CmdSetServoPosition         = 172       # +23 (195)
    CmdGetADCValue              = 196       # +7 (203)
    CmdSendSerial               = 204       # +23 (227)
    CmdHC_SR04                  = 228       # +23 (251)
    CmdSoundStreamCmd           = 254


    # Existing motor ID's are D0-D9, D12-D14 and D16-D18 there are more limits
    LIMITS      = [ (30, 180),
                    (70, 170),
                    (0, 170),
                    (0, 170),
                    (0, 60),
                    (0, 180),
                    (0, 90),
                    (0, 60),
                    (0, 180),
                    (0, 180),
                    (0, 180),
                    (0, 160),
                    (0, 180),
                    (0, 130),
                    (0, 180),
                    (0, 160),
                    (0, 180),
                    (50, 130),
                    (0, 180),
                    (0, 180),
                    (0, 180) ]

    SERVO_SPEED_SLOWEST = 20
    SERVO_SPEED_FASTEST = 0

    CmdSoundInitStop = 0
    CmdSoundLoad     = 1
    CmdSoundPlay     = 2


    def __init__(self, ip = ConnectedEndPointAddress, port = ConnectedEndPointPort):
        self.ip          = ip
        self.port        = port
        self.sock        = None
        self.isConnected = False
        self.connect()
        self.init()


    def init(self):
        self.I2C     = I2C(self)
        self.rgbEyes = RGBEyes(self)

        # preset
        self.rgbEyes.setColor(xrange(18), 0, 0, 0)
        self.rgbEyes.setColor([0,1,2,9,10,11], 0, 0, 7)
        self.rgbEyes.setColor([4,13], 7, 7, 7)

        default_pose = [ ( 0, 110 ),    # head left - right
                         ( 1, 90  ),    # neck up - down
                         ( 6, 90  ),    # right hand closed
                         ( 5, 70  ),    # right elbow
                         ( 4, 20  ),    # right shoulder close - open
                         ( 3, 180  ),   # right shoulder rotation

                         ( 9, 90  ),    # left hand
                         ( 8, 70  ),    # left elbow
                         ( 7, 20  ),    # left shoulder close - open
                         ( 2, 10  ),    # left shoulder rotation

                         ( 14, 90  ),   # right feet
                         ( 13, 80  ),   # right knee
                         ( 12, 80  ),   # right hip

                         ( 18, 80  ),   # left feet
                         ( 17, 80  ),   # left knee
                         ( 16, 90  ),   # left hip
                       ]

        for idx, v in default_pose:
            self.setPosition(idx, v)
            time.sleep(0.25)


    def connect(self):
        try:
            self.sock = socket.create_connection((self.ip, self.port), timeout = 10)
            self.isConnected = True
        except:
            raise RuntimeError(EMSG_ROBOT_NOT_FOUND % (self.ip, self.port))


    def sendCommand(self, bytesToExpect, cmd, params = None):

        # check command
        if cmd == EZB.CmdUnknown:
            raise ValueError, "unknown command: %s" % cmd

        # prepare data
        cmd_data = bytearray([cmd])
        if params:
            if not isinstance(params, bytearray):
                cmd_data += bytearray([params])
            else:
                cmd_data += params

        # send data
        self.sock.send(cmd_data)

        if bytesToExpect > 0:
            return self.sock.recv(bytesToExpect)


    def __del__(self):
        if self.isConnected and self.sock:
            self.sock.close()


    def setPosition(self, servo, position):
        """ This method sets a position of the specified servo.

        The joint position values are clipped to the values defined in LIMITS.

        @param servo    - id of the servo
        @param position - absolute value for the given servo position
        """

        # clip joint limits
        low, high = self.LIMITS[servo]
        position  = min(max(low, int(position)), high)

        # send command
        self.sendCommand(0, EZB.CmdSetServoPosition + servo, position)


    def setServoSpeed(self, servo, speed):
        """ This method sets the speed of the specified servo.

        @param servo    - id of the servo
        @param position - absolute value for the given servo position
        """
        self.sendCommand(0, EZB.CmdSetServoSpeed + servo, speed)
