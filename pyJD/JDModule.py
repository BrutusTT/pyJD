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
from pyJD.utils     import rad2deg, angle
from pyJD.pyEZB.EZB import EZB


class JDModule(EZModule):
    """ The JDModule class provides a yarp module to control the JD robots motors. """


    def configure(self, rf):
        EZModule.configure(self, rf)

        self.lookAtPort     = self.createInputPort('lookAt',     'buffered')
        self.pointLeftPort  = self.createInputPort('pointLeft',  'buffered')
        self.pointRightPort = self.createInputPort('pointRight', 'buffered')
        
        # set init poses
        EZB()
            
        return True

    
    def updateModule(self):
        
        # read the bottle              
        lookAt_bottle    = self.lookAtPort.read(False)
        if lookAt_bottle:
            self.lookAt(lookAt_bottle)
 
        pointLeft_bottle = self.pointLeftPort.read(False)
        if pointLeft_bottle:
            self.pointLeft(pointLeft_bottle)
 
        pointRight_bottle = self.pointRightPort.read(False)
        if pointRight_bottle:
            self.pointRight(pointRight_bottle)

        return True


    def respond(self, command, reply):
        """ This is the respond hook method which gets called upon receiving a bottle via RPC port.

        @param command - input bottle
        @param reply - output bottle
        @return boolean
        """

        if command.get(0).toString() == 'set':

            if command.get(1).toString() == 'pos':

                # send it to the motors
                self.sendPosition(command.get(2).asInt(), command.get(3).asInt())

                # reply with success
                reply.addString('ack')
                return True

        # reply with success
        reply.addString('nack')
        return True


    def lookAt(self, bottle):
        """ This method executes the lookAt command.

        @param bottle - Message Format: <near-far:double> <left-right:double> <down-up:double>
        """

        # get the coordinates from the bottle
        near_far     = bottle.get(0).asDouble() * -1.0
        left_right   = bottle.get(1).asDouble()
        down_up      = bottle.get(2).asDouble()

        # calculate the angles
        angle_d0 = rad2deg( angle([1.0, 0.0, 0.0], [left_right, down_up, near_far]) ) + 20
        angle_d1 = rad2deg( angle([0.0, 1.0, 0.0], [left_right, down_up, near_far]) )

        # send it to the motors
        self.sendPosition(0, angle_d0)
        self.sendPosition(1, angle_d1)
        

    def pointLeft(self, bottle):
        """ This method executes the point command with the left arm.

        @param bottle - Message Format: <near-far:double> <left-right:double> <down-up:double>
        """
        
        # get the coordinates from the bottle
        near_far    = bottle.get(0).asDouble() * -1.0
        left_right  = bottle.get(1).asDouble() * -1.0
        down_up     = bottle.get(2).asDouble()

        # calculate the angles
        angle_d4 = rad2deg( angle([1.0, 0.0, 0.0], [left_right, down_up, near_far]) ) / 3
        angle_d3 = rad2deg( angle([0.0, 1.0, 0.0], [left_right, down_up, near_far]) )

        # send it to the motors
        self.sendPosition(4, angle_d4)
        self.sendPosition(3, angle_d3)
        self.sendPosition(5, 90)
        self.sendPosition(6, 90)
        

    def pointRight(self, bottle):
        """ This method executes the point command with the right arm.

        @param bottle - Message Format: <near-far:double> <left-right:double> <down-up:double>
        """

        # get the coordinates from the bottle
        near_far    = bottle.get(0).asDouble() * -1.0
        left_right  = bottle.get(1).asDouble() * -1.0
        down_up     = bottle.get(2).asDouble() * -1.0

        # calculate the angles
        angle_d7 = rad2deg( angle([1.0, 0.0, 0.0], [left_right, down_up, near_far]) ) / 3
        angle_d2 = rad2deg( angle([0.0, 1.0, 0.0], [left_right, down_up, near_far]) )

        # send it to the motors
        self.sendPosition(7, angle_d7)
        self.sendPosition(2, angle_d2)
        self.sendPosition(8, 90)
        self.sendPosition(9, 90)


if __name__ == '__main__':
    main(JDModule)
