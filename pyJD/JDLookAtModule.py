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
####################################################################################################
from pyJD.EZModule  import EZModule, main
from pyJD.utils     import rad2deg, angle


class JDLookAtModule(EZModule):
    """ The JDLookAtModule class provides a yarp module to control the JD robots gaze direction. """

    CUR_Z = 0.0
    CUR_X = 0.0
    CUR_Y = 0.0


    def respond(self, command, reply):
        """ This is the respond hook method which gets called upon receiving a bottle via RPC port.

        @param command - input bottle
        @param reply - output bottle
        @return boolean
        """

        # get the coordinates from the bottle
        near_far    = command.get(0).asDouble() * -1.0
        left_right  = command.get(1).asDouble()
        down_up     = command.get(2).asDouble()

        if command.size() > 3:
            near_far    += self.CUR_Z
            left_right  += self.CUR_X
            down_up     += self.CUR_Y

        # calculate the angles
        angle_d0 = rad2deg( angle([1.0, 0.0, 0.0], [left_right, down_up, near_far]) )
        angle_d1 = rad2deg( angle([0.0, 1.0, 0.0], [left_right, down_up, near_far]) )

        # send it to the motors
        self.sendPosition(0, angle_d0 + 20)
        self.sendPosition(1, angle_d1)

        self.CUR_Z = near_far
        self.CUR_X = left_right
        self.CUR_Y = down_up

        # reply with success
        reply.addString('ack')
        return True



if __name__ == '__main__':
    main(JDLookAtModule)
