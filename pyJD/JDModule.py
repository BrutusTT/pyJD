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
import os.path      as     op
import time

from pyJD.EZModule  import EZModule, main
from pyJD.utils     import rad2deg, angle
from pyJD.pyEZB.EZB import EZB

from pyJD           import DATA_PATH



class JDModule(EZModule):
    """ The JDModule class provides a yarp module to control the JD robots motors. """


    def configure(self, rf):
        EZModule.configure(self, rf)

        self.lookAtPort     = self.createInputPort('lookAt',     'buffered')
        self.pointLeftPort  = self.createInputPort('pointLeft',  'buffered')
        self.pointRightPort = self.createInputPort('pointRight', 'buffered')
        self.patternPort    = self.createInputPort('pattern',    'buffered')
        self.patterns       = {}

        self._loadMovementPatterns()

        # initialize JD Humanoid poses
        self.ezb = EZB()

        return True


    def updateModule(self):

        # read the bottle
        look_at_bottle    = self.lookAtPort.read(False)
        if look_at_bottle:
            self.lookAt(look_at_bottle)

        point_left_bottle = self.pointLeftPort.read(False)
        if point_left_bottle:
            self.pointLeft(point_left_bottle)

        point_right_bottle = self.pointRightPort.read(False)
        if point_right_bottle:
            self.pointRight(point_right_bottle)

        pattern_bottle = self.patternPort.read(False)
        if pattern_bottle:
            self.pattern(pattern_bottle)

        return True


    def respond(self, command, reply):
        """ This is the respond hook method which gets called upon receiving a bottle via RPC port.

        @param command - input bottle
        @param reply - output bottle
        @return boolean
        """

        cmd = command.get(0).toString()
        if cmd == 'set':

            if command.get(1).toString() == 'pos':

                # send it to the motors
                self.ezb.setPosition(command.get(2).asInt(), command.get(3).asInt())

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
        self.ezb.setPosition(0, angle_d0)
        self.ezb.setPosition(1, angle_d1)


    def pointLeft(self, bottle):
        """ This method executes the point command with the left arm.

        @param bottle - Message Format: <near-far:double> <left-right:double> <down-up:double>
        """

        # get the coordinates from the bottle
        near_far    = bottle.get(0).asDouble() * -1.0
        left_right  = bottle.get(1).asDouble() * -1.0
        down_up     = bottle.get(2).asDouble() * -1.0

        # calculate the angles
        point_to  = [left_right, down_up, near_far]
        angle_d3 = 180 -  rad2deg( angle((0.0, 1.0, 0.0), point_to) )
        angle_d4 = 180 - (rad2deg( angle((1.0, 0.0, 0.0), point_to) ) - 90)

        # split angle d4 into d4 and d5 values
        angle_d5 = max(  0, angle_d4 - 180) + 90
        angle_d4 = min(180, angle_d4)

        # send it to the motors
        self.ezb.setPosition(6, 90)
        self.ezb.setPosition(5, angle_d5)
        self.ezb.setPosition(4, angle_d4)
        self.ezb.setPosition(3, angle_d3)

        print angle_d3, angle_d4, angle_d5


    def pointRight(self, bottle):
        """ This method executes the point command with the right arm.

        @param bottle - Message Format: <near-far:double> <left-right:double> <down-up:double>
        """

        # get the coordinates from the bottle
        near_far    = bottle.get(0).asDouble() * -1.0
        left_right  = bottle.get(1).asDouble() * -1.0
        down_up     = bottle.get(2).asDouble() * -1.0

        # calculate the angles
        point_to = [left_right, down_up, near_far]
        angle_d2 = rad2deg( angle((0.0, 1.0, 0.0), point_to) )
        angle_d7 = 90 - rad2deg( angle((1.0, 0.0, 0.0), point_to) )

        # split angle d4 into d4 and d5 values
        angle_d8 = min(  1, angle_d7) + 90
        angle_d7 = max(  1, angle_d7)

        # send it to the motors
        self.ezb.setPosition(9, 90)
        self.ezb.setPosition(8, angle_d8)
        self.ezb.setPosition(7, angle_d7)
        self.ezb.setPosition(2, angle_d2)

        print angle_d2, angle_d7, angle_d8

    def pattern(self, bottle):
        pattern = bottle.get(0).toString()

        if pattern in self.patterns:

            saved_pose = self.ezb.getCurrentPose()

            for servo, position in self.patterns[pattern]:
                self.ezb.setPosition(servo, position)
                time.sleep(0.1)

            # reset pose
            self.ezb.setPose(saved_pose)


    def _loadMovementPatterns(self):
        """ Loads the movement patterns from the configuration file. """

        pattern_file  = op.join(DATA_PATH, 'patterns.csv')

        # do not care if we do not have a pattern file
        if not op.isfile(pattern_file):
            return

        name          = None
        with open(pattern_file, 'r') as file_handle:

            # parse lines
            for line in file_handle.read().split('\n'):

                line = line.strip()

                # ignore empty
                if not line:
                    continue

                # new pattern name
                elif line.startswith('['):
                    name = line[1:line.index(']')].strip()
                    self.patterns[name] = []

                # new step
                elif '\t' in line:
                    joint, position = line.split('\t')
                    self.patterns[name].append( (int(joint), int(position)) )

            names = self.patterns.keys()
            names.sort()

            print 'Patterns loaded'
            print '==============='
            for name in names:
                print name, len(self.patterns[name])


if __name__ == '__main__':
    main(JDModule)
