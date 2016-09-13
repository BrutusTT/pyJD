# Usage

Each module can be started standalone using the following command line.


    <ModuleName> [--ip <IP Address>] [--port <Port>] [--name <Name Prefix>]

Parameters:

    []            - denotes optional parameter
    <ModuleName>  - can be one of the following: - JDModule
                                                 - JDVideo
                                                 - JDFollowFace
    <IP Address>  - default is 192.168.1.1
    <Port>        - default is 23
    <Name Prefix> - if a name is given it will be used as a prefix for the port names
                    e.g.:  --name test results in /test/JDModule/rpc

Example:

    $ JDModule --name MyRobot
