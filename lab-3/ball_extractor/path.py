"""Manages paths in a filesystem."""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import os

class PathAccumulator:
    """Describes a path accumulator."""

    def __init__(self, ext=[]):
        """Initializes a path accumulator.

        Args:
            ext [str]: A list of extentions to look for. Default is `[]`.
        """

        for i in range(len(ext)):
            ext[i] = ext[i].upper()
        self.__extensions = set(ext)
        self.__paths = set()

    def paths(self):
        """Accessor to the accumulated paths.
        
        Returns:
            [str]: A list of normalized file paths.
        """

        output = list(self.__paths)
        output.sort()
        return output

    def normalize_prefix(self, path):
        """Normalizes a file prefix.

        If relative, it adds a `./` in front if not already there. If absolute (
        starting with `/`), it is left alone.

        Args:
            path str: The path to normalize.
        
        Returns:
            str: The normalized file path.
        """

        if path[0] != '/' and path[0:2] != './' and path[0] != '.':
            return './' + path
        else:
            return path

    def check_extension(self, path):
        """Checks if a path leads to a file that matches the given extentions.

        Args:
            path str: The path to a file.
        
        Returns:
            bool: `True` if it matches, `False` otherwise.
        """

        _, ext = os.path.splitext(path)
        ext = ext.upper()
        return ext in self.__extensions

    def gather_file(self, path):
        """Attempts to gather a file if it exists and matches a valid extention.

        Otherwise, the file will be skipped and a warning will be printed.

        Args:
            path str: The path to a file.
        """

        path = self.normalize_prefix(path)
        if not os.path.isfile(path):
            print('*** WARN: `{}` does not exist!'
                  ' Skipping... ***'.format(path))
        elif not self.check_extension(path):
            print('*** WARN: `{}` is not a JPG file!'
                  ' Skipping... ***'.format(path))
        else:
            self.__paths.add(path)

    def gather_directory(self, path):
        """Attempts to gather all files in a directory if they match they exist
        and match a valid extention.

        Otherwise, the file will be skipped and a warning will be printed.

        Args:
            path str: The path to a directory.
        """

        path = self.normalize_prefix(path)
        if not os.path.isdir(path):
            print('*** WARN: `{}` does not exist!'
                  ' Skipping... ***'.format(path))
        else:
            files = os.listdir(path)
            for f in files:
                self.gather_file(os.path.join(path, f))

    def path_walk(self, paths = []):
        """Attempts to gather all files in a set of paths to directories and
        files if they exist and match a valid extention.

        Otherwise, the file will be skipped and a warning will be printed.

        Args:
            path str: The path to a file.
        """

        if type(paths) is str:
            paths = [paths]

        for p in paths:
            if os.path.isdir(p):
                self.gather_directory(p)
            elif os.path.isfile(p):
                self.gather_file(p)
        return self.paths()