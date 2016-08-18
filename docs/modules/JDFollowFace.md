# JDFollowFace

This module is used to calculate the head joint positions provided that it receives a face position. The output port of this module should be connected to the [JDLookAtModule](JDLookAtModule.md).

## Port List

### ``/JDFollowFace/face``

* **Type**: Input
* **Message Format**: `` <face_count> (  (<x0> <y0>) (<x1> <y1>) ...  )``
* **Parameter**
	* ``<face_count>: integer`` - number of faces in the list
	* ``<xn>: integer`` - x-center of the n-th face
	* ``<yn>: integer`` - y-center of the n-th face

### ``/JDFollowFace/position``

* **Type**: Output
* **Message Format**: ``<near_far> <left_right> <down_up>``
* **Parameter**
	* ``<near_far>: double`` 
	* ``<left_right>: double``
	* ``<down_up>: double`` 