"""Extract the position of a ping-pong ball from an image.

Uses OpenCV to perform a series of image processing tasks on a set of images in
order to find the center of a ping-pong ball. 
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys
import cv2
import numpy as np

from path_accumulator import PathAccumulator

class BallExtractor:
    """Identifies and extracts a white ping-pong ball from an image."""

    def __init__(self):
        self.__path_accumulator = PathAccumulator(['.jpg', '.jpeg'])

    def prompt(self):
        config, err = self.__parse_args(sys.argv[1:])
        if err:
            print('\n{}\n\n{}\n').format(err, self.__usage())
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
            cv2.imshow('Results', raw)
            cv2.imshow('Mask', mask)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        return circles

    def __build_paths(self, config):
        files = config['files']
        directories = config['directories']
        return self.__path_accumulator.path_walk(files + directories)

    def __parse_args(self, args):
        # if no arguments provided, print usage
        if len(args) == 0:
            print('\n{}\n'.format(self.__usage()))
            exit(0)

        # see if `-h` or `--help` was invoked first
        for arg in args:
            if arg == '-h' or arg == '--help':
                print('\n{}\n'.format(self.__usage()))
                exit(0)

        # extract configuration
        flags = []
        values = []
        for i in range(len(args)):
            if i % 2 == 0:
                flags.append(args[i])
            else:
                values.append(args[i])

        # should have one key per one value
        if len(flags) != len(values):
            return (
                None,
                '*** Error: Invalid number of arguments! ***'
            )

        arg_dict = dict.fromkeys(flags)
        for i in range(len(flags)):
            key = flags[i]
            value = values[i]
            if not arg_dict[key]:
                arg_dict[key] = []
            arg_dict[key].append(value)

        # override defaults
        defaults = {'files': [],'directories': []}
        config = defaults.copy()
        d_overriden = False
        for flag, values in arg_dict.iteritems():
            if flag == '-f' or flag == '--file':
                config['files'] = config['files'] + values
            elif flag == '-d' or flag == '--directory':
                if not d_overriden:
                    config['directories'] = values
                    d_overriden = True
                else:
                    config['directories'] = config['directories'] + values
            else:
                return (
                    None,
                    '*** Error: Invalid argument `{}`! ***'.format(flag)
                )
        return config, None

    def __usage(self):
        return ('Usage: python ball_extractor.py [options]'
                '\n'
                '\n    options: -f, --file      FILE         The path to a'
                '\n                                          single image file'
                '\n                                          (JPG format only).'
                '\n                                          Many single image'
                '\n                                          flags can be'
                '\n                                          passed in'
                '\n                                          succession for'
                '\n                                          processing.'
                '\n'
                '\n             -d, --directory DIRECTORY    Directory with'
                '\n                                          image files (JPG'
                '\n                                          format only). This'
                '\n                                          flag gives the'
                '\n                                          user the ability'
                '\n                                          to funnel many'
                '\n                                          images into the'
                '\n                                          processor at once'
                '\n                                          with one flag.'
                '\n'
                '\n             -h, --help                   Show this help'
                '\n                                          message and exit.')

def main():
    ball_extractor = BallExtractor()
    ball_extractor.prompt()

if __name__ == '__main__':
    main()
