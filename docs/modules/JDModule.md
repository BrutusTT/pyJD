# JDModule

The JDModule can be used to set JD's joints to specified positions.

## Port List

``/JDModule/rpc``

### Port ``/JDModule/rpc``

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