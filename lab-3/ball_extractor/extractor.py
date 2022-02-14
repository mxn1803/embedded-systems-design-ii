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
        self.__path_accumulator = PathAccumulator(['.jpg', '.jpeg'])
        self.__config_parser = ConfigParser()

    def prompt(self):
        config, err = self.__config_parser.parse(sys.argv[1:])
        if err:
            print('\n{}\n\n{}\n').format(err, self.__config_parser.usage())
            return

        paths = self.__build_paths(config)
        _ = self.extract(paths)

    def extract(self, paths):
        """Runs extraction procedure."""

        def load_raws(paths):
            raws = []
            for path in paths:
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
                for i in circles[0,:]:
                    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        paths = self.__path_accumulator.path_walk(paths)
        raws = load_raws(paths)
        results, result_masks = [], []

        for raw in raws:
            masked, mask = mask_raw(raw)
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
            draw_circles(circles, raw)
            draw_circles(circles, mask)
            results.append(raw)
            result_masks.append(mask)

            cv2.imshow('Image', raw)
            cv2.imshow('Mask', mask)
            cv2.waitKey(0)

        # self.__save_results(config, raw, mask)

        cv2.destroyAllWindows()
        return circles

    def __save_results(self, config, results, masks):
        if not os.path.isdir(config['output']):
            os.makedirs(os.path.join(config['output'], 'results'))
            os.makedirs(os.path.join(config['output'], 'masks'))
        for i in range(len(results)):
            cv2.imwrite(config['output'])

    def __build_paths(self, config):
        files = config['files']
        directories = config['directories']
        return self.__path_accumulator.path_walk(files + directories)

def main():
    ball_extractor = BallExtractor()
    ball_extractor.prompt()

if __name__ == '__main__':
    main()
