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
import numpy as np
import cv2
import yarp

from pyJD.EZModule         import EZModule, main
from pyJD.pyEZB.EZBv4Video import EZBv4Video


class JDVideo(EZModule):
    """ The JDVideo class provides a yarp module to retrieve the JD's video stream. """


    def configure(self, rf):
        EZModule.configure(self, rf)

        self.bufImageOut, self.bufArrayOut = self.createImageBuffer(320, 200)
        self.imgOutPort = yarp.Port()
        self.imgOutPort.open('/JDVideo/img:o')

        self.video = EZBv4Video()
        self.video.openCVImageHook = self.onImage
        return True


    def runModule(self, rf = None):
        self.configure(rf)
        self.video.getImages()


    def onImage(self, image):

        # and convert image back to something the yarpview can understand
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (320, 200))
        self.bufArrayOut[:,:] = image

        # Send the result to the output port
        self.imgOutPort.write(self.bufImageOut)


    def interruptModule(self):
        self.imgOutPort.interrupt()
        return EZModule.interruptModule(self)


    def close(self):
        self.imgOutPort.close()
        return EZModule.close(self)


    @staticmethod
    def createImageBuffer(width = 320, height = 240, channels = 3):
        """ This method creates image buffers with the specified \a width, \a height and number of
            color channels \a channels.

        @param width    - integer specifying the width of the image   (default: 320)
        @param height   - integer specifying the height of the image  (default: 240)
        @param channels - integer specifying number of color channels (default: 3)
        @return image, buffer array
        """

        if channels == 1:
            buf_image = yarp.ImageFloat()
            buf_image.resize(width, height)

            buf_array = np.zeros((height, width), dtype = np.float32)

        else:
            buf_image = yarp.ImageRgb()
            buf_image.resize(width, height)

            buf_array = np.zeros((height, width, channels), dtype = np.uint8)

        buf_image.setExternal( buf_array,
                               buf_array.shape[1],
                               buf_array.shape[0] )

        return buf_image, buf_array


if __name__ == '__main__':
    main(JDVideo)
