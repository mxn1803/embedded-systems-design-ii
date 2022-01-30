"""Calculates position of an object in 3D space given two (x, y) coordinates.

A command line utility that prompts the user for two (x, y) coordinates and 
prints the position in 3D space as an (x, y, z) coordinate. Core functionality 
may also be hooked into by an external module.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

class Binocular:
    """Determines the location of objects in 3D space using binocular math."""

    def __init__(
        self,
        baseline=60,
        focal_length=6,
        pixel_size=0.006,
        fov_width=752,
        fov_height=480,
        left_center=(376, 240),
        right_center=(376, 240)
    ):
        """Initializes a set of binoculars.

        Args:
            baseline     int|float:              The baseline of the camera in
                                                 millimeters, default is 60.
            focal_length int|float:              The focal length in
                                                 millimeters, default is 6.
            pixel_size   int|float:              The size of a single pixel in
                                                 millimeters, default is 0.006.
            fov_width    int|float:              The FOV width (x-axis) in
                                                 pixels, default is 752.
            fov_height   int|float:              The FOV height (y-axis) in
                                                 pixels, default is 480.
            left_center  (int|float, int|float): The coordinates of the center
                                                 point of the left camera in
                                                 pixels, default is (376, 240).
            right_center (int|float, int|float): The coordinates of the center
                                                 point of the right camera in
                                                 pixels, default is (376, 240).
        """

        parameters, err = self.__sanitize_floats(
            baseline,
            focal_length,
            pixel_size,
            fov_width,
            fov_height,
            left_center,
            right_center
        )

        if err:
            raise ValueError(err)

        self.__baseline = parameters[0]
        self.__focal_length = parameters[1]
        self.__pixel_size = parameters[2]
        self.__fov_width = parameters[3]
        self.__fov_height = parameters[4]
        self.__left_center = parameters[5]
        self.__right_center = parameters[6]

    def position(self, left, right):
        """Finds the location of a centroid in 3D spaces given two perspectives.

        Args:
            left  (int|float, int|float): A tuple containing the (x, y)
                                          coordinates of the centroid from the
                                          perspective of the left camera.
            right (int|float, int|float): A tuple containing the (x, y)
                                          coordinates of the centroid from the
                                          perspective of the right camera.

        Returns:
            ((float, float, float, float), str): The X, Y, and Z coordinate of
                                                 the centroid along with the
                                                 disparity, all in millimeters.
                                                 If an error occured, the
                                                 message will be included in a
                                                 tailing string.
        """

        left, left_err = self.__sanitize_floats(*left)
        right, right_err = self.__sanitize_floats(*right)

        err = left_err or right_err or None

        if err:
            return (None, None, None, None), err

        return (
            self.__x_position(left, right),
            self.__y_position(left, right),
            self.__z_position(left, right),
            self.__disparity(left, right)
        ), None

    def prompt(self):
        """Runs a small command line interface."""

        left = raw_input('Please enter the centroid as perceived'
                         ' by the left camera in "X Y" form: ')
        right = raw_input('Please enter the centroid as perceived'
                         ' by the right camera in "X Y" form: ')

        left, right, err = self.__sanitize_input_format(left, right)

        if err:
            print('\n{}\n'.format(err))
            return

        (x, y, z, d), err = self.position(left, right)

        print('\nX         : {:5.0f} mm\n'
              'Y         : {:5.0f} mm\n'
              'Z         : {:5.0f} mm\n'
              'Disparity : {:5.1f} mm\n').format(x, y, z, d)

    def __sanitize_input_format(self, left, right):
        left = tuple(left.strip().split(' '))
        right = tuple(right.strip().split(' '))

        if len(left) != 2 or len(right) != 2:
            return (
                left,
                right,
                '*** Error: All entries must be'
                ' of the form "X Y" (ex. "476 240")! ***'
            )

        left, left_err = self.__sanitize_floats(*left)
        right, right_err = self.__sanitize_floats(*right)
        err = left_err or right_err or None

        if err:
            return left, right, err

        return left, right, None

    def __sanitize_floats(self, *args):
        unsanitized = args
        sanitized = []
        try:
            for arg in args:
                if type(arg) is tuple:
                    # recursion for nested tuples
                    elements, err = self.__sanitize_floats(*arg)

                    if err:
                        raise ValueError

                    sanitized.append(elements)
                else:
                    sanitized.append(float(arg))
            return tuple(sanitized), None
        except (TypeError, ValueError):
            return (
                unsanitized,
                '*** Error: All entries must be numbers! ***'
            )

    def __disparity(self, left, right):
        return abs(
            (left[0] - self.__left_center[0]) -
            (right[0] - self.__right_center[0])
        ) * self.__pixel_size

    def __x_position(self, left, right):
        return self.__z_position(left, right) * \
               (left[0] - self.__left_center[0]) * \
               self.__pixel_size / \
               self.__focal_length

    def __y_position(self, left, right):
        return self.__z_position(left, right) * \
               (left[1] - self.__left_center[1]) * \
               self.__pixel_size / \
               self.__focal_length

    def __z_position(self, left, right):
        d = self.__disparity(left, right)
        if d <= 0.0:
            return float('inf')
        return self.__baseline * self.__focal_length / d

def main():
    binoculars = Binoculars()
    binoculars.prompt()

if __name__ == '__main__':
    main()
