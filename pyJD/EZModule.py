####################################################################################################
#    Copyright (C) 2016 by Ingo Keller, Katrin Lohan                                               #
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
import argparse
import socket
import time
import yarp

EMSG_YARP_NOT_FOUND  = "Could not connect to the yarp server. Try running 'yarp detect'."
EMSG_ROBOT_NOT_FOUND = 'Could not connect to the robot at %s:%s'


class EZModule(yarp.RFModule):
    """ The EZBModule class provides a base class for developing modules for the JD robot.
    """

    # Default IP Address and Port for the JD Humanoid Robot.
    TCP_IP      = '192.168.1.1'
    TCP_PORT    = 23

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


    def __init__(self, ip, port, prefix):
        yarp.RFModule.__init__(self)
        self.ip     = ip
        self.port   = int(port)
        self.prefix = prefix


    def configure(self, rf):

        name = self.__class__.__name__ 
        if self.prefix:
            name = self.prefix + '/' + name

        self.setName(name)

        try:
            self.ezb = socket.create_connection((self.ip, self.port), timeout = 1)
        except:
            raise RuntimeError(EMSG_ROBOT_NOT_FOUND % (self.ip, self.port))

        # RPC Port
        self.rpc_port = yarp.RpcServer()

        # name settings
        port_name = '/%s/%s' % (name, 'rpc')

        if not self.rpc_port.open(port_name):
            raise RuntimeError, EMSG_YARP_NOT_FOUND

        self.attach_rpc_server(self.rpc_port)

        return True


    def interruptModule(self):
        self.rpc_port.interrupt()
        return True


    def close(self):
        self.rpc_port.close()
        self.ezb.close()
        return True


    def getPeriod(self):
        return 0.1


    def updateModule(self):
        # XXX: I do not know why we need that, but if method is empty the module gets stuck
        time.sleep(0.000001)
        return True


    def clip_limits(self, servo, position):
        """ This method clips the position based on the servo limits.

        @param servo    - id of the servo
        @param position - absolute value for the given servo position
        @return integer - clipped absolute position
        """
        limit = self.LIMITS[servo]
        if position < limit[0]:
            position = limit[0]
        elif position > limit[1]:
            position = limit[1]
        return position


    def sendPosition(self, servo, position):
        """ This method sends a position to the specified servo. 
        
        @param servo    - id of the servo
        @param position - absolute value for the given servo position
        """
        position = self.clip_limits(servo, int(position))
        self.ezb.send(chr(0xac + servo) + chr(position))


####################################################################################################
#
# Default methods for running the modules standalone 
#
####################################################################################################
def createArgParser():
    """ This method creates a base argument parser. 
    
    @return Argument Parser object
    """
    parser = argparse.ArgumentParser(description='Create a JDModule to control the JD robot.')
    parser.add_argument( '-i', '--ip', 
                         dest       = 'ip', 
                         default    = str(EZModule.TCP_IP),
                         help       = 'IP address for the JD robot.')
    parser.add_argument( '-p', '--port', 
                         dest       = 'port', 
                         default    = str(EZModule.TCP_PORT),
                         help       = 'Port for the JD robot')
    parser.add_argument( '-n', '--name', 
                         dest       = 'name', 
                         default    = '',
                         help       = 'Name prefix for Yarp port names')

    return parser.parse_args()


def main(module_cls):
    """ This is a main method to run a module from command line. 

    @param module_cls - an EZModule based class that can be started as a standalone module.
    """
    args = createArgParser()

    yarp.Network.init()

    resource_finder = yarp.ResourceFinder()
    resource_finder.setVerbose(True)

    # resource_finder.configure(argc,argv);

    module = module_cls(args.ip, args.port, args.name)
    module.configure(resource_finder)
    module.runModule(resource_finder)

    yarp.Network.fini()
