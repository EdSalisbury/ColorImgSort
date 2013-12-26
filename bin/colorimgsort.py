#!/bin/env python

# ColorImgSort
# Sorts images based on color
# by Ed Salisbury <ed@edsalisbury.net>
# Written: 2013/12/24

import argparse
import os
import os.path
import math
from PIL import Image


class ImgSort():

    def __init__(self, **kwargs):
        """Class constructor - sets up the internal variables"""

        self.path = kwargs['path']
        self.prefix = kwargs['prefix']
        self.num_points = kwargs['num_points']
        self.blur_radius = kwargs['blur_radius']
        self.num_colors = kwargs['num_colors']

    def points(self, width, height):
        """Returns points based on an image size and the number of points

        Returns points that are distributed evenly across an image.  If you
        think about intersecting lines, 9 points would create 3 horizontal
        lines and 3 vertical lines, and would return the 9 intersecting points.
        Due to the way this works, the number of points must be a perfect
        square (4, 9, 16, 25, etc.)
        """

        num_lines = int(math.sqrt(self.num_points))

        if num_lines ** 2 != self.num_points:
            raise RuntimeError("Number of points must be a perfect square")

        chunk_width = int(width / (num_lines + 1))
        chunk_height = int(height / (num_lines + 1))

        x_list = []
        y_list = []
        for i in range(1, num_lines + 1):
            x_list.append(chunk_width * i)
            y_list.append(chunk_height * i)

        xy_list = []
        for y in y_list:
            for x in x_list:
                xy_list.append((x, y))

        return xy_list

    def diamond_points(self, x, y):
        """Returns the list of points that form a diamond around the origin

        Makes concentric diamonds around a point (up to the specified radius),
        and returns all points within that diamond.
        """

        points = []

        orig_x = x
        orig_y = y

        # Origin
        points.append((x, y))

        for i in range(1, self.blur_radius + 1):
            # Top
            points.append((orig_x, orig_y - i))

            # NE side
            for x, y in zip(range(0, i), range(-i, 0)):
                points.append((orig_x + x, orig_y + y))

            # SE side
            for x, y in zip(range(i, 0, -1), range(0, i)):
                points.append((orig_x + x, orig_y + y))

            # SW side
            for x, y in zip(range(0, -i, -1), range(i, 0, -1)):
                points.append((orig_x + x, orig_y + y))

            # NW side
            for x, y in zip(range(-i, 0), range(0, -i, -1)):
                points.append((orig_x + x, orig_y + y))

        return points

    def sort(self):
        """Sorts a directory of images based on color

        Opens a directory, gets the file list, and determines the color at
        specific points in the images (using a simple blur), downsamples to
        a lower bitdepth and stores the filename in a dictionary, based on the
        color signature.  When completed, it will rename the files based on the
        dictionary entries, using the specified prefix.
        """

        img_files = os.listdir(self.path)

        img_list = {}

        for img_file in img_files:
            filename = os.path.join(self.path, img_file)

            try:
                img = Image.open(filename)
            except:
                continue

            print "Analyzing %s" % img_file

            points = self.points(img.size[0], img.size[1])
            key = ""
            for point in points:

                # Get the average color for each point
                ave_points = self.diamond_points(point[0], point[1])
                red = 0
                green = 0
                blue = 0
                for ave_point in ave_points:
                    try:
                        rgb = img.getpixel(ave_point)
                        red += rgb[0]
                        green += rgb[1]
                        blue += rgb[2]
                    except IndexError:
                        pass
                red /= len(ave_points)
                green /= len(ave_points)
                blue /= len(ave_points)

                # Bitdepths:
                # 12 bit - 4096 colors, range 0-F, divide by 16
                # 9 bit - 512 colors, range 0-7, divide by 32
                # 6 bit - 64 colors, range 0-3, divide by 64
                # 3 bit - 8 colors, range 0-1, divide by 128

                if self.num_colors == 8:
                    div = 128
                elif self.num_colors == 64:
                    div = 64
                elif self.num_colors == 512:
                    div = 32
                elif self.num_colors == 4096:
                    div = 16
                else:
                    self.usage()

                # Lower the bitdepth
                red = int(red / div)
                green = int(green / div)
                blue = int(blue / div)

                # Add to the key
                key += "%x%x%x" % (red, green, blue)

            # Add the key if needed
            if key not in img_list:
                img_list[key] = []

            # Add the file to the list
            img_list[key].append(img_file)

        # Go through and rename the files, based on the img_list dictionary
        # and the prefix
        num = 1
        for img in sorted(img_list.iterkeys()):
            for filename in sorted(img_list[img]):
                name, ext = os.path.splitext(filename)
                new_filename = "%s%04d%s" % (self.prefix, num, ext)
                full_filename = os.path.join(self.path, filename)
                full_new_filename = os.path.join(self.path, new_filename)
                if os.path.isfile(full_new_filename):
                    print "File %s exists - aborting!" % full_new_filename
                    return

                os.rename(full_filename, full_new_filename)
                print "Renamed %s to %s." % (filename, new_filename)
                num += 1

if __name__ == '__main__':

    description = "Sorts a directory of images"
    epilog = ("Note: Number of points must be a perfect square "
              "(4, 5, 9, etc.) (default is 9)")

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('path', help='directory of images to be sorted')
    parser.add_argument('prefix', help='prefix to use for new images')
    parser.add_argument('-c', dest='num_colors', type=int,
                        choices=[8, 64, 512, 4096], default=8,
                        help='number of colors to reduce to')
    parser.add_argument('-n', dest='num_points', type=int, default=9,
                        help='number of points to use')
    parser.add_argument('-r', dest='blur_radius', type=int, default=3,
                        help='blur radius')

    args = parser.parse_args()

    num_lines = int(math.sqrt(args.num_points))
    if num_lines ** 2 != args.num_points:
        print "Number of points must be a perfect square."
        parser.print_help()

    img = ImgSort(**vars(args))
    img.sort()
