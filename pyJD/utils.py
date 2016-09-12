####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
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
import math


def dotproduct(vec_1, vec_2):
    """ This method calculates the dot-product of two vectors. """
    return sum((a*b) for a, b in zip(vec_1, vec_2))


def length(vec):
    """ This method calculates the length of a vector. """
    return math.sqrt(dotproduct(vec, vec))


def angle(vec_1, vec_2):
    """ This method calculates the angle between two vectors. """
    if length(vec_1) == 0 or length(vec_2) == 0:
        return 0
    return math.acos(dotproduct(vec_1, vec_2) / (length(vec_1) * length(vec_2)))


def rad2deg(rad):
    """ This method calculates the degree from radians. """
    return 180.0 * rad / math.pi
