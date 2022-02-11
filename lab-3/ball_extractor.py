"""Extract the position of a ping-pong ball from an image.

Uses OpenCV to perform a series of image processing tasks on a set of images in order to find the center of a ping-pong ball. 
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys
import cv2

class BallExtractor:
    """Identifies and extracts a white ping-pong ball from an image."""

    def __init__(self):
        self.__parse_args(sys.argv[1:])
        print(self.__usage())

    def extract(self):
        """Runs extraction procedure."""
        print('I am extracting the ball...')

    def __parse_args(self, args):
        print('I am parsing the arguments...')

    def __usage(self):
        return ('\nUsage: python ball_extractor.py [options]'
                '\n'
                '\n    options: -i, --image-file    The path to a single image'
                '\n                                 file (JPG format only).'
                '\n                                 If the `-d` flag is also'
                '\n                                 provided, this option is'
                '\n                                 ignored. Processing will'
                '\n                                 only be performed on this'
                '\n                                 file.'
                '\n'
                '\n             -d, --directory     Directory where many images'
                '\n                                 (JPG format only) exist.'
                '\n                                 This flag takes precedence'
                '\n                                 over the `-i` flag.'
                '\n                                 Processing will be done on'
                '\n                                 all valid images in this'
                '\n                                 directory. Default is `.`.'
                '\n')

def main():
    ball_extractor = BallExtractor()
    ball_extractor.extract()

if __name__ == '__main__':
    main()
