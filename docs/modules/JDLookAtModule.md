# JDLookAtModule

The module is used to control the gaze.

## Port List

``/JDLookAtModule/rpc``

### Port ``/JDLookAtModule/rpc``

* **Type**: RPC

	    command message: "<near-far> <left-right> <down-up>"
	        <near-far>:   float - distance in meters [  0.1, -inf ] (Be aware: negative distance!)
	        <left-right>: float - distance in meters [ -inf,  inf ]
	        <down-up>:    float - distance in meters [ -inf,  inf ]
	
	    Example:
	        -1.0 0.5 0.0   - Looks to the left (Fixation Point: 1m in front + 50cm to the left side)