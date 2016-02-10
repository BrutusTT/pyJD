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
import yarp


from pyJD.EZModule import EZModule, createArgParser


class JDModule(EZModule):
    """ The JDModule class provides a yarp module to control the JD robots motors. """


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



def main():
    """ This is a main method to run the module from command line. """
    
    args = createArgParser()

    yarp.Network.init()

    resource_finder = yarp.ResourceFinder()
    resource_finder.setVerbose(True)

    # resource_finder.configure(argc,argv);

    module = JDModule(args.ip, args.port, args.name)
    module.runModule(resource_finder)

    yarp.Network.fini()


if __name__ == '__main__':
    main()
    