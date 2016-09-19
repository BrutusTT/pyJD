####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
#                                                                                                  #
#    This file is part of pyJD (Python/Yarp Tools for the JD robot).                               #
#                                                                                                  #
#    pyJD is free software: you can redistribute it and/or modify it under the terms of the        #
#    GNU Affero General Public License as published by the Free Software Foundation, either        #
#    version 3 of the License, or (at your option) any later version.                              #
#                                                                                                  #
#    pyJD is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;             #
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     #
#    See the GNU Affero General Public License for more details.                                   #
#                                                                                                  #
#    You should have received a copy of the GNU Affero General Public License                      #
#    along with pyJD.  If not, see <http://www.gnu.org/licenses/>.                                 #
####################################################################################################
from pyJD.EZModule  import EZModule, main
from pyJD.pyEZB.EZB import EZB


class Emotions(EZModule):
    """ The JDModule class provides a yarp module to control the JD robots motors. """

    JD = EZB()

    NEUT = ( (0, 0, 7), (0, 0, 7), (0, 0, 7),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),

             (0, 0, 7), (0, 0, 7), (0, 0, 7),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),
           )

    HAPP = ( (0, 0, 7), (0, 0, 7), (0, 0, 7),
             (0, 0, 0), (0, 7, 0), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),

             (0, 0, 7), (0, 0, 7), (0, 0, 7),
             (0, 0, 0), (0, 7, 0), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),
           )

    SW01 = ( (7, 7, 7), (0, 0, 0), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (7, 7, 7),

             (0, 0, 0), (0, 0, 0), (7, 7, 7),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (7, 7, 7), (0, 0, 0), (0, 0, 0),
           )

    SW02 = ( (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),

             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
           )

    SW03 = ( (0, 0, 0), (0, 0, 0), (7, 7, 7),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (7, 7, 7), (0, 0, 0), (0, 0, 0),

             (7, 7, 7), (0, 0, 0), (0, 0, 0),
             (0, 0, 0), (7, 7, 7), (0, 0, 0),
             (0, 0, 0), (0, 0, 0), (7, 7, 7),
           )

    SW04 = ( (0, 0, 0), (0, 0, 0), (0, 0, 0),
             (7, 7, 7), (7, 7, 7), (7, 7, 7),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),

             (0, 0, 0), (0, 0, 0), (0, 0, 0),
             (7, 7, 7), (7, 7, 7), (7, 7, 7),
             (0, 0, 0), (0, 0, 0), (0, 0, 0),
           )

    DIZZ = [SW01, SW02, SW03, SW04]


    def respond(self, command, reply):
        """ This is the respond hook method which gets called upon receiving a bottle via RPC port.

        @param command - input bottle
        @param reply - output bottle
        @return boolean
        """
        if command.get(0).toString() == 'neutral':
            self.JD.rgbEyes.setArray(Emotions.NEUT)

        elif command.get(0).toString() == 'happy':
            self.JD.rgbEyes.setArray(Emotions.HAPP)

        elif command.get(0).toString() == 'dizzy':

            for array in Emotions.DIZZ:
                self.JD.rgbEyes.setArray(array)
            for array in Emotions.DIZZ:
                self.JD.rgbEyes.setArray(array)
            self.JD.rgbEyes.setArray(Emotions.NEUT)

        # reply with success
        reply.addString('nack')
        return True


if __name__ == '__main__':
    main(Emotions)
    