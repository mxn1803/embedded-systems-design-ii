import os

class PathAccumulator:
    def __init__(self, ext=[]):
        for i in range(len(ext)):
            ext[i] = ext[i].upper()
        self.__extensions = set(ext)
        self.__paths = set()

    def paths(self):
        output = list(self.__paths)
        output.sort()
        return output

    def normalize_prefix(self, path):
        if path[0] != '/' and path[0:2] != './' and path[0] != '.':
            return './' + path
        else:
            return path

    def check_extension(self, path):
        _, ext = os.path.splitext(path)
        ext = ext.upper()
        return ext in self.__extensions

    def gather_file(self, path):
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
        path = self.normalize_prefix(path)
        if not os.path.isdir(path):
            print('*** WARN: `{}` does not exist!'
                  ' Skipping... ***'.format(path))
        else:
            files = os.listdir(path)
            for f in files:
                self.gather_file(os.path.join(path, f))

    def path_walk(self, paths = []):
        if type(paths) is str:
            paths = [paths]

        for p in paths:
            if os.path.isdir(p):
                self.gather_directory(p)
            elif os.path.isfile(p):
                self.gather_file(p)
        return self.paths()