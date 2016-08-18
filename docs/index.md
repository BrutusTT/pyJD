# pyJD - A Python/Yarp Wrapper for the JD robot

pyJD is a collection of [Yarp](https://github.com/robotology/yarp) Modules to control the 
[EZ-Robot JD Humanoid Robot](https://www.google.de/#q=EZ-Robot+JD+Humanoid+Robot). 

## Installation

1- Install the dependencies:

You need Yarp installed with the python bindings. For more details see 
[full instructions](http://wiki.icub.org/yarpdoc/install.html).

Example: OSX using [Homebrew](http://brew.sh)

    brew tap homebrew/x11
    brew install --with-python yarp


2- Download the source code: 

    git clone https://github.com/BrutusTT/pyJD

3- build and install:

    cd pyJD
    python setup.py install


## Running the Modules

Each module can be started standalone using the following command line.


    python -m pyJD.<ModuleName> [--ip <IP Address>] [--port <Port>] [--name <Name Prefix>]

Parameters:

    []            - denotes optional parameter
    <ModuleName>  - can be one of the following: - JDModule
                                                 - JDLookAtModule
                                                 - JDPointAtModuleLeftArm
                                                 - JDPointAtModuleRightArm
    <IP Address>  - default is 192.168.1.1
    <Port>        - default is 23
    <Name Prefix> - if a name is given it will be used as a prefix for the port names
                    e.g.:  --name test results in /test/JDModule/rpc

Example:

    python -m pyJD.JDLookAtModule --name MyRobot


# Modules

The package contains Yarp modules that can be used to control the JD Humanoid Robot. 

* [Modules](modules/index.md)

Happy hacking!

## License

See COPYING for licensing info.
