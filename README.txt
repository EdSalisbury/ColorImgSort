============
ColorImgSort
============

ColorImgSort will sort a directory of images based on colors at different
points in the image, based on the image size.  This is useful when there are
multiple images in a directory, which are similar in content, but not
necessarily identical.  It will rename the files in such a way so that the
images that are close to each other in content will appear next to each
other in an image viewer, and can then be processed manually.  It is good for
images that have been color corrected, resized, rescanned, etc.

Typical usage:
==============

python colorimgsort.py <directory of images> <prefix>

Other options that can be specified:
====================================

-n <number of points to compare>
In order to compare images, ColorImgSort will pick specific points in an image,
distributed evenly.  This number must be a perfect square.  Defaults to 9.

-c <number of colors to reduce to>
Exact colors are not helpful, as the program is looking for images that are
approximate in content.  Possible values are 8, 64, 512, 4096.  Defaults to 8.

-r <blur radius>
In order to get colors that are reasonable to compare, the program will get
the pixel colors around a specific point (depending on the radius) and average
them.  Defaults to 3.

Written 2013/12/25 by Ed Salisbury <ed@edsalisbury.net>
