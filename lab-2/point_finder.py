"""Calculates position of an object in 3D space given two (x, y) coordinates.

A command line utility that prompts the user for two (x, y) coordinates and 
prints the position in 3D space as an (x, y, z) coordinate. Core functionality 
may also be hooked into by an external module.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

class DepthFinder:
    """Calculates the 3D position of an object given two (x, y) coordinates."""

    def depth(
        self,
        x_left=0,
        x_right=0,
        b=60,
        f=6,
        ps=0.006,
        x_num_px=752,
        cx_left=376,
        cx_right=376
    ):
        """Hook into the core functionality of a DepthFinder.

        Args:
            x_left   int|float: The left centroid in pixels, default is 0.
            x_right  int|float: The right centroid in pixels, default is 0.
            b        int|float: The baseline of the camera in millimeters,
                                default is 60.
            f        int|float: The focal length in millimeters, default is 6.
            ps       int|float: The size of a single pixel in millimeters,
                                default is 0.006.
            x_num_px int|float: The FOV width (x-axis) in pixels, default is
                                752.
            cx_left  int|float: The center point of the left camera in
                                pixels, default is 376.
            cx_right int|float: The center point of the right camera in
                                pixels, default is 376.

        Returns:
            (float, float)|str: A tuple containing the depth and disparity in
                                millimeters. If an input error occured, this
                                will be a string containing the error message.
        """

        parameters = locals()
        parameters.pop('self')
        parameters, err = self.__sanitize(parameters)

        if err:
            return None, None, err

        d = abs((x_left - cx_left) - (x_right - cx_right)) * ps
        z = b * f / d

        return z, d, err

    def prompt(self):
        """Runs a small command line interface."""

        b = 60
        f = 6
        ps = 0.006
        x_num_px = 752
        cx_left = 376
        cx_right = 376
        x_left = raw_input('Please enter the left centroid: ')
        x_right = raw_input('Please enter the right centroid: ')

        parameters, err = self.__sanitize({
            'b': b,
            'f': f,
            'ps': ps,
            'x_num_px': x_num_px,
            'cx_left': cx_left,
            'cx_right': cx_right,
            'x_left': x_left,
            'x_right': x_right
        })

        if err:
            print('\n{}\n'.format(err))
            return

        z, d, err = self.depth(**parameters)

        print('\nDispatiry: {:.3f} mm\nZ        : {:.0f} mm\n'.format(d, z))

    def __sanitize(self, parameters):
        # identical centroids cause division by zero 
        if parameters['x_left'] == parameters['x_right']:
            return (
                dict(parameters),
                '*** Error: Two centroids must not be identical! ***'
            )

        try:
            for k, v in parameters.iteritems():
                parameters[k] = float(v)
            return parameters, None
        except (TypeError, ValueError):
            return (
                dict(parameters),
                '*** Error: All entries must be numbers! ***'
            )

def main():
    depthFinder = DepthFinder()
    depthFinder.prompt()

if __name__ == '__main__':
    main()
