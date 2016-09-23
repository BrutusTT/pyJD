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
        self.ip       = ip
        self.port     = int(port)
        self.prefix   = prefix
#         self.last_pos = [-1] * len(EZModule.LIMITS)


    def configure(self, rf):

        name = self.__class__.__name__
        if self.prefix:
            name = self.prefix + '/' + name

        self.setName(name)

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
        for x in dir(self):
            if x.endswith('Port') and 'interrupt' in dir(getattr(self, x)):
                getattr(self, x).interrupt()
        return True


    def close(self):
        self.rpc_port.close()
        for x in dir(self):
            if x.endswith('Port') and 'close' in dir(getattr(self, x)):
                getattr(self, x).close()
        return True


    def getPeriod(self):
        return 0.1


    def updateModule(self):
        # XXX: I do not know why we need that, but if method is empty the module gets stuck
        time.sleep(0.000001)
        return True


    def createInputPort(self, name, mode = 'unbuffered'):
        """ This method returns an input port.

        @param obj      - the object that the port is created for
        @param name     - if a name is provided it gets appended to the modules name
        @param buffered - if buffered is True a buffered port will be used otherwise not;
                          default is True.
        @result port
        """
        return self.__createPort(name + ':i', None, mode)


    def __createPort(self, name, target = None, mode = 'unbuffered'):
        """ This method returns a port object.

        @param name     - yarp name for the port
        @param obj      - object for which the port is created
        @param buffered - if buffered is True a buffered port will be used otherwise not;
                          default is True.
        @result port
        """
        # create port
        if mode == 'buffered':
            port = yarp.BufferedPortBottle()

        elif mode == 'rpcclient':
            port = yarp.RpcClient()

        elif mode == 'rpcserver':
            port = yarp.RpcServer()

        else:
            port = yarp.Port()

        # build port name
        port_name = ['']

        # prefix handling
        if hasattr(self, 'prefix') and self.prefix:
            port_name.append(self.prefix)

        port_name.append(self.__class__.__name__)
        port_name.append(name)

        # open port
        if not port.open('/'.join(port_name)):
            raise RuntimeError, EMSG_YARP_NOT_FOUND

        # add output if given
        if target:
            port.addOutput(target)

        if hasattr(self, '_ports'):
            self._ports.append(port)

        return port


    def createOutputPort(self, name, target = None, mode = 'unbuffered'):
        """ This method returns an output port.

        @param obj      - the object that the port is created for
        @param name     - if a name is provided it gets appended to the modules name
        @param buffered - if buffered is True a buffered port will be used otherwise not;
                          default is True.
        @result port
        """
        return self.__createPort(name + ':o', target, mode)


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
    module.runModule(resource_finder)

    yarp.Network.fini()
