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
import yarp

from pyJD.EZModule import EZModule, main


class JDFollowFace(EZModule):
    """ The JDFollowFace class provides a module which uses a given face position to calculate
        a gazing direction for the JD Humanoid in order to look at the face.
    """


    def configure(self, rf):
        EZModule.configure(self, rf)

        self.faceInPort      = self.createInputPort('face', 'buffered')
        self.positionOutPort = self.createOutputPort('position', 'buffered')
        return True


    def updateModule(self):

        # read the bottle
        input_bottle = self.faceInPort.read()

        # get the envelope as bottle
        envelope_bottle = self.faceInPort.prepare()
        envelope_bottle.clear()
        self.faceInPort.getEnvelope(envelope_bottle)

        # if bottle exists run the convert method
        if input_bottle:
            self.onBottle(input_bottle, envelope_bottle)

        return True


    def onBottle(self, bottle, envelope_bottle):

        if bottle.get(0).asInt() == 0:
            return

        # pick first face
        faces = bottle.get(1).asList()
        face  = faces.get(0).asList()

        center_x = face.get(1).asInt()
        center_y = face.get(2).asInt()

        print center_x, center_y,

        center_x -= 160

        z = 1.0
        x = (center_x * 0.5) / 320
        y = 0.0

        print z, x, y

        bottle = yarp.Bottle()
        bottle.clear()

        bottle.addDouble(0.0)
        bottle.addDouble(x)
        bottle.addDouble(0.0)
        bottle.addDouble(-1.0)
        self.positionOutPort.write(bottle)


if __name__ == '__main__':
    main(JDFollowFace)
