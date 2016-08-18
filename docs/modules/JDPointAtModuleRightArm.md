# JDPointAtModuleRightArm

The module is used to control the arms in order to point towards a given point. However, the module does not take impossible positions into account.

## ``/JDPointAtModuleRightArm/rpc``

* **Type**: RPC

	    command message: "<near-far> <left-right> <down-up>"
	        <near-far>:   float - distance in meters [  inf, -inf ] (Be aware: negative distance!)
	        <left-right>: float - distance in meters [ -inf,  inf ]
	        <down-up>:    float - distance in meters [ -inf,  inf ]
	
	    Example:
	        -1.0 0.5 0.0   - Points to the left (Point: 1m in front + 50cm to the left side)