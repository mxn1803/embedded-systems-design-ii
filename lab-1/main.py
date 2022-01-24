def main():
    try:
        # useful constants
        b = 60                   # baseline (mm)
        f = 6                    # focal length (mm)
        ps = .006                # pixel size (mm)
        x_num_px = 752           # field of view width (px)
        cx_left = x_num_px >> 1  # center point of left camera (px)
        cx_right = x_num_px >> 1 # center point of right camera (px)

        x_left = int(raw_input('Please enter the left centroid: '))
        x_right = int(raw_input('Please enter the right centroid: '))

        # calculate disparity and depth (mm)
        d = abs((x_left - cx_left) - (x_right - cx_right)) * ps
        z = b * f / d

        print('\nDispatiry: {} mm\nZ        : {} mm\n'.format(d, z))
    except ValueError:
        print('\n*** ERROR: Both entries must be a valid number. ***\n')

if __name__ == '__main__':
    main()
