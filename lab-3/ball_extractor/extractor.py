"""Extract the position of a ping-pong ball from an image.

Uses OpenCV to perform a series of image processing tasks on a set of images in
order to find the center of a ping-pong ball.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys
import os
import cv2
import numpy as np

from path import PathAccumulator
from config import ConfigParser

class BallExtractor:
    """Identifies and extracts a white ping-pong ball from an image."""

    def __init__(self):
        """Initializes a ball extractor."""

        self.__path_accumulator = PathAccumulator(['.jpg', '.jpeg'])
        self.__config_parser = ConfigParser()

    def extract(self, srcs, dst='./out'):
        """Runs extraction procedure.
            
        Args:
            srcs [str]: A list containing a series of filepaths to images that
                        are staged for processing.
            dst  str:   The output directory to house the results. Will be
                        created if it does not currently exist. Default is
                        './out'.

        Returns:
            [[float]]: A list of circles found by OpenCV's HoughCircle
                       implementation.
        """

        def load_raws(srcs):
            raws = []
            for path in srcs:
                img = cv2.imread(path)
                raws.append(img)
            return raws

        def mask_raw(raw):
            blur = cv2.GaussianBlur(raw, (11, 11), 0)
            ycrcb = cv2.cvtColor(blur, cv2.COLOR_BGR2YCrCb)

            # YCrCb bounds
            low = np.array([60, 0, 0])
            high = np.array([255, 144, 129])

            mask = cv2.inRange(ycrcb, low, high)
            masked = cv2.bitwise_and(raw, raw, mask=mask)
            masked = cv2.cvtColor(masked, cv2.COLOR_YCrCb2RGB)
            masked = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)
            return masked, mask

        def draw_circles(circles, img):
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for [(x, y, r)] in circles:
                    cv2.circle(img, (x, y), r, (0, 255, 0), 2)
                    cv2.circle(img, (x, y), 2, (0, 0, 255), 3)

        paths = self.__path_accumulator.path_walk(srcs)
        raws = load_raws(paths)
        results, result_masks = [], []

        if os.path.isdir(dst):
            for f in os.listdir(dst):
                os.remove(os.path.join(dst, f))
        else:
            os.makedirs(dst)

        for i in range(len(raws)):
            masked, mask = mask_raw(raws[i])
            circles = cv2.HoughCircles(
                image=masked,
                method=cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=120,
                param1=60,
                param2=30,
                minRadius=30,
                maxRadius=180
            )
            draw_circles(circles, raws[i])
            draw_circles(circles, mask)

            circles_list = circles.tolist()
            results.append(raws[i])
            result_masks.append(mask)
            self.__save_image(paths[i], dst, raws[i], mask)
        return circles_list[0]

    def prompt(self):
        """Runs a small command line interface."""
        
        configuration, err = self.__config_parser.parse(sys.argv[1:])
        if err:
            print('\n{}\n\n{}\n').format(err, self.__config_parser.usage())
            return

        paths = self.__build_paths(configuration)
        _ = self.extract(paths, configuration['output'])

    def __save_image(self, src, dst, raw, mask):
        [name, ext] = os.path.basename(src).split('.')
        cv2.imwrite(os.path.join(dst, name + '.' + ext), raw)
        cv2.imwrite(os.path.join(dst, name + '-mask.' + ext), mask)
        print('Result: ' + os.path.join(dst, name + '.' + ext))
        print('Mask  : ' + os.path.join(dst, name + '-mask.' + ext))

    def __build_paths(self, config):
        files = config['files']
        directories = config['directories']
        return self.__path_accumulator.path_walk(files + directories)

def main():
    ball_extractor = BallExtractor()
    ball_extractor.prompt()

if __name__ == '__main__':
    main()
