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
#    See the GNU General Public License for more details.                                          #
#                                                                                                  #
#    You should have received a copy of the GNU Affero General Public License                      #
#    along with pyJD.  If not, see <http://www.gnu.org/licenses/>.                                 #
####################################################################################################
import math
import yarp

from pyJD.EZModule import EZModule, createArgParser


def dotproduct(vec_1, vec_2):
    """ This method calculates the dot-product of two vectors. """
    return sum((a*b) for a, b in zip(vec_1, vec_2))


def length(vec):
    """ This method calculates the length of a vector. """
    return math.sqrt(dotproduct(vec, vec))


def angle(vec_1, vec_2):
    """ This method calculates the angle between two vectors. """
    return math.acos(dotproduct(vec_1, vec_2) / (length(vec_1) * length(vec_2)))


def rad2deg(rad):
    """ This method calculates the degree from radians. """
    return 180.0 * rad / math.pi


class JDLookAtModule(EZModule):
    """ The JDLookAtModule class provides a yarp module to control the JD robots gaze direction. """


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

        # calculate the angles
        angle_d0 = rad2deg( angle([1.0, 0.0, 0.0], [left_right, down_up, near_far]) )
        angle_d1 = rad2deg( angle([0.0, 1.0, 0.0], [left_right, down_up, near_far]) )

        # send it to the motors
        self.sendPosition(0, angle_d0 + 20)
        self.sendPosition(1, angle_d1)

        # reply with success
        reply.addString('ack')
        return True


def main():
    """ This is a main method to run the module from command line. """
    args = createArgParser()

    yarp.Network.init()

    resource_finder = yarp.ResourceFinder()
    resource_finder.setVerbose(True)

    # resource_finder.configure(argc,argv);

    module = JDLookAtModule(args.ip, args.port, args.name)
    module.runModule(resource_finder)

    yarp.Network.fini()


if __name__ == '__main__':
    main()
