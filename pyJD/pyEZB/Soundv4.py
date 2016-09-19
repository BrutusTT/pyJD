import time
from pyJD.pyEZB.EZB import EZB


EMSG_ROBOT_NOT_FOUND = 'Could not connect to the robot at %s:%s'


class Soundv4(EZB):

    # Default IP Address and Port for the JD Humanoid Robot.
    ConnectedEndPointAddress    = '192.168.1.1'
    ConnectedEndPointPort       = 24

    # <summary>
    # The recommended size of the the audio packets
    # </summary>
    RECOMMENDED_PACKET_SIZE = 256

    # <summary>
    # The recommended size of the prebuffer before playing the audio
    # </summary>
    RECOMMENDED_PREBUFFER_SIZE = 20000

    # <summary>
    # The sample rate at which the data is played back on the EZ-B
    # </summary>
    AUDIO_SAMPLE_BITRATE = 14700

    # <summary>
    # The size of each packet which is transmitted over the wire to the EZ-B.
    # </summary>
    PACKET_SIZE = RECOMMENDED_PACKET_SIZE

    # <summary>
    # The ammount of data to prebuffer to the EZ-B before playing the audio. The EZ-B has a 50k
    # buffer, so this value cannot be any higher than that.
    # </summary>
    PREBUFFER_SIZE = RECOMMENDED_PREBUFFER_SIZE


    def playAudio(self, audio):
        self.position = 0
        self.playing  = False

#        audio  = [ x for x in range(255) ] * 100000
        while self.position < len(audio):
            time.sleep(0.001)
            data   = self.prepareAudio(audio)
            print len(audio), len(data), self.position

            if not self.playing and self.position > self.PREBUFFER_SIZE:
                self.sendCommand(0, EZB.CmdSoundStreamCmd, EZB.CmdSoundPlay)
                self.playing = True

            self.sendCommand(0, EZB.CmdSoundStreamCmd, data)



    def prepareAudio(self, audio):

        bTmp             = audio[self.position : self.position + self.PACKET_SIZE]

        self.position   += len(bTmp)

        bArray           = bytearray([0]*len(bTmp))

        highest          = 0
        lowest           = 255
        average          = 0
        total            = 0
        volumeMultiplier = 1.0 # self.volume / 100

        for idx in xrange(len(bTmp)):

            newVal = float(bTmp[idx])
            print newVal

            if newVal > 128:
                newVal = max(128, 128 + ((newVal - 128) * volumeMultiplier))
            elif newVal < 128:
                newVal = min(128, 128 - ((128 - newVal) * volumeMultiplier))

            if newVal > 255:
                newVal     = 255.0
            elif newVal < 0:
                newVal      = 0.0


            highest = max(highest, int(newVal))
            lowest  = min(lowest,  int(newVal))
            total  += int(newVal)

            bArray[idx] = int(newVal)

        average = int(total / len(bTmp))
        dlength = len(bArray)
        dataTmp = bytearray()
        dataTmp.append(EZB.CmdSoundLoad)
        dataTmp.append(int(dlength / 255))
        dataTmp.append(int(dlength % 255))
        dataTmp += bArray

        return dataTmp
