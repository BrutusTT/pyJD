# JDModule

The JDModule can be used to set JD's joints to specified positions.

## ``/JDModule/rpc``

* **Type**: RPC
* **Message Format**: ``set pos <joint_id> <position>``
* **Parameter**

	* ``<joint_id>: integer [0 - 23]``  
	* ``<position>: integer [0 - 180]``
* **Response**
	* ``ack`` - command processed
	* ``nack`` - error occurred
* **Message Example**
	* ``set pos 0 13`` - JD looks to the left.

## ``/JDModule/lookAt:i``

* **Type**: Buffered Port
* **Message Format**: ``<near-far> <left-right> <down-up>``
* **Parameter**

	* ``<near-far>``      float - distance in meters [  0.1, -inf ] ***Be aware: negative distance!***
	* ``<left-right>``     float - distance in meters [ -inf,  inf ]
	* ``<down-up>``    float - distance in meters [ -inf,  inf ]
	
* **Message Example**
	* ``-1.0 0.5 0.0``   - Looks to the left (Fixation Point: 1m in front + 50cm to the left side) 

## ``/JDModule/pointLeft:i``

* **Type**: Buffered Port
* **Message Format**: ``<near-far> <left-right> <down-up>``
* **Parameter**

	* ``<near-far>``      float - distance in meters [  inf, -inf ] ***Be aware: negative distance!***
	* ``<left-right>``     float - distance in meters [ -inf,  inf ]
	* ``<down-up>``    float - distance in meters [ -inf,  inf ]

* **Message Example**
	* ``-1.0 0.5 0.0``   - Points to the left (Point: 1m in front + 50cm to the left side)

## ``/JDModule/pointRight:i``

* **Type**: Buffered Port
* **Message Format**: ``<near-far> <left-right> <down-up>``
* **Parameter**

	* ``<near-far>``      float - distance in meters [  inf, -inf ] ***Be aware: negative distance!***
	* ``<left-right>``     float - distance in meters [ -inf,  inf ]
	* ``<down-up>``    float - distance in meters [ -inf,  inf ]
	
* **Message Example**
	* ``-1.0 0.5 0.0``   - Points to the left (Point: 1m in front + 50cm to the left side)
