"""Extract the position of a ping-pong ball from an image.

Uses OpenCV to perform a series of image processing tasks on a set of images in order to find the center of a ping-pong ball. 
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys
import os
import cv2
import numpy as np

class BallExtractor:
    """Identifies and extracts a white ping-pong ball from an image."""

    def prompt(self):
        config, err = self.__parse_args(sys.argv[1:])
        if err:
            print('\n{}\n\n{}\n').format(err, self.__usage())
            return

        paths = self.__build_paths(config)
        return self.extract(paths)


    def extract(self, paths):
        """Runs extraction procedure."""

        paths = self.__sanitize_file_paths(paths)

        # load raw images from each path
        raws = []
        for path in paths:
            img = cv2.imread(path)
            raws.append(img)

        for raw in raws:
            blur = cv2.GaussianBlur(raw, (11, 11), 0)
            ycrcb = cv2.cvtColor(blur, cv2.COLOR_BGR2YCrCb)

            low = np.array([60, 0, 0])
            high = np.array([255, 144, 129])

            mask = cv2.inRange(ycrcb, low, high)
            masked = cv2.bitwise_and(raw, raw, mask=mask)
            masked = cv2.cvtColor(masked, cv2.COLOR_YCrCb2RGB)
            masked = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)

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
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    cv2.circle(raw, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(raw, (i[0], i[1]), 2, (0, 0, 255), 3)
                    cv2.circle(mask, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(mask, (i[0], i[1]), 2, (0, 0, 255), 3)

            cv2.imshow('Results', raw)
            cv2.imshow('Mask', mask)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __build_paths(self, config):
        files = self.__sanitize_file_paths(config['files'])
        directories = self.__sanitize_directory_paths(config['directories'])
        paths = list(set(files + directories))
        paths.sort()
        return paths

    def __check_extension(self, path):
        _, ext = os.path.splitext(path)
        ext = ext.upper()
        return ext == '.JPG' or ext == '.JPEG'

    def __normalize_prefix(self, path):
        if path[0] != '/' and path[0:2] != './' and path[0] != '.':
            return './' + path
        else:
            return path

    def __sanitize_file_paths(self, paths):
        cleared = []
        for f in paths:
            f = self.__normalize_prefix(f)
            if not os.path.isfile(f):
                print('*** WARN: `{}` does not exist!'
                      ' Skipping... ***'.format(f))
            elif not self.__check_extension(f):
                print('*** WARN: `{}` is not a JPG file!'
                      ' Skipping... ***'.format(f))
            else:
                cleared.append(f)
        return cleared

    def __sanitize_directory_paths(self, paths):
        cleared = []
        for d in paths:
            d = self.__normalize_prefix(d)
            if not os.path.isdir(d):
                print('*** WARN: `{}` does not exist!'
                      ' Skipping... ***'.format(f))
            else:
                files = os.listdir(d)
                for i in range(len(files)):
                    files[i] = os.path.join(d, files[i])
                cleared = cleared + self.__sanitize_file_paths(files)
        return cleared

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
        config = self.__default_config()
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

    def __default_config(self):
        return {'files': [],'directories': []}

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
