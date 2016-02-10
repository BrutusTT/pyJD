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

JDModule:

    python -m pyJD.JDModule --ip <IP Address> --port <Port>


JDLookAtModule:

    python -m pyJD.JDLookAtModule --ip <IP Address> --port <Port>

Without parameters the default is IP: 192.168.1.1 and Port: 23.


## General

The package contains Yarp modules that can be used to control the JD Humanoid Robot. Once the 
modules are started, they provide RPC Ports.

The **JDModule** is used to control motor position.

    command message: "set pos <motor_id> <position>"
        <motor_id>: integer [0 - 23]
        <position>: integer [0 - 180]

    Example:
        set pos 0 130   - Looks to the left

The **JDLookAtModule** is used to control the gaze.

    command message: "<near-far> <left-right> <up-down>"
        <near-far>:   float - distance in meters [  0.1, -inf ] (Be aware: negative distance!)
        <left-right>: float - distance in meters [ -inf,  inf ]
        <up-down>:    float - distance in meters [ -inf,  inf ]

    Example:
        -1.0 0.5 0.0   - Looks to the left (Fixation Point: 1m in front + 50cm to the left side)




Happy hacking!

## License

See COPYING for licensing info.
