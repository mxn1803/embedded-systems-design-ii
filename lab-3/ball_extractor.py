"""Extract the position of a ping-pong ball from an image.

Uses OpenCV to perform a series of image processing tasks on a set of images in order to find the center of a ping-pong ball. 
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys
import os
import cv2

class BallExtractor:
    """Identifies and extracts a white ping-pong ball from an image."""

    def __init__(self):
        config, err = self.__parse_args(sys.argv[1:])
        if err: return self.__handle_err(err)
        self.__config = config

        paths, err = self.__build_paths()
        if err: return self.__handle_err(err)
        self.__paths = paths

        print paths

    def extract(self):
        """Runs extraction procedure."""
        print('I am extracting the ball...')

    def __build_paths(self):
        file = self.__config['file']
        if file: return self.__check_file_path(file)

        directory = self.__config['directory']
        return self.__check_directory_path(directory)

    def __check_extension(self, path):
        _, ext = os.path.splitext(path)
        ext = ext.upper()
        return ext == '.JPG' or ext == '.JPEG'

    def __check_file_path(self, file):
        err = None
        token = './{}' if file[0] != '/' else '{}'
        file = token.format(file)
        if not os.path.isfile(file):
            err = '*** Error: `{}` does not exist! ***'.format(file)
        if not self.__check_extension(file):
            err = '*** Error: `{}` is not a JPG file! ***'.format(file)

        if err: return [], err
        return [file], err

    def __check_directory_path(self, directory):
        err = None
        if not os.path.isdir(directory):
            token = './{}/' if directory[0] != '/' else '{}/'
            directory = token.format(directory)
            err = '*** Error: `{}` does not exist! ***'.format(directory)

        if err: return [], err

        jpgs = []
        for file in os.listdir(directory):
            if self.__check_extension(os.path.join(directory, file)):
                jpgs.append(os.path.join(directory, file))
        return jpgs, err

    def __parse_args(self, args):
        if len(args) % 2 != 0 or len(args) > 4:
            return None, '*** Error: Invalid number of arguments! ***'

        arg_dict = {}
        for i in range(0, len(args), 2):
            arg_dict[args[i]] = args[i + 1]

        config = self.__default_config()

        for flag, value in arg_dict.iteritems():
            if flag == '-f' or flag == '--file':
                config['file'] = value
            elif flag == '-d' or flag == '--directory':
                config['directory'] = value
            else:
                return (
                    None,
                    '*** Error: Invalid argument `{}`! ***'.format(flag)
                )

        return config, None

    def __default_config(self):
        return {'file': '','directory': '.'}

    def __handle_err(self, err):
        print('\n{}\n\n{}\n').format(err, self.__usage())

    def __usage(self):
        return ('Usage: python ball_extractor.py [options]'
                '\n'
                '\n    options: -f, --file         The path to a single image'
                '\n                                file (JPG format only).'
                '\n                                If the `-d` flag is also'
                '\n                                provided, this option takes'
                '\n                                precedent. Processing will'
                '\n                                only be performed on this'
                '\n                                file.'
                '\n'
                '\n             -d, --directory    Directory where many images'
                '\n                                (JPG format only) exist.'
                '\n                                This flag takes precedence'
                '\n                                over the `-i` flag.'
                '\n                                Processing will be done on'
                '\n                                all valid images in this'
                '\n                                directory. Default is `.`.')

def main():
    ball_extractor = BallExtractor()
    ball_extractor.extract()

if __name__ == '__main__':
    main()

                # ext = v[-4:].uppercase()
                # if ext != '.JPG' or ext != '.JPEG':
                #     return None, '*** Error: Not a JPG file! ***'