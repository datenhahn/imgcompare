# MIT License
#
# Copyright (c) 2016 Jonas Hahn <jonas.hahn@datenhahn.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import os
import unittest

from PIL import Image, ImageChops
from PIL.Image import FLOYDSTEINBERG, NEAREST

import imgcompare

dir_path = os.path.dirname(os.path.realpath(__file__))

PNG_CAT = dir_path + "/testimages/cat.png"
PNG_BLACK = dir_path + "/testimages/black.png"
PNG_WHITE = dir_path + "/testimages/white.png"
PNG_HALF_BW = dir_path + "/testimages/half_black_white.png"
PNG_CAT_SLIGHT_DIFF = dir_path + "/testimages/cat_slight_diff.png"

JPG_CAT = dir_path + "/testimages/cat.jpg"
JPG_CAT_BAD_SIZE = dir_path + "/testimages/cat_bad_size.jpg"
JPG_CAT_SLIGHT_DIFF = dir_path + "/testimages/cat_slight_diff.jpg"
JPG_CAT_DIFFERENT_RUN = dir_path + "/testimages/cat_jpg_different_run.jpg"
JPG_CAT_REENCODED = dir_path + "/testimages/cat_jpg_reencoded.jpg"
JPG_BLACK = dir_path + "/testimages/black.jpg"
JPG_WHITE = dir_path + "/testimages/white.jpg"
JPG_HALF_BW = dir_path + "/testimages/half_black_white.jpg"

black_png = Image.open(PNG_BLACK)
PNG_BLACK_RGB = black_png.convert('RGB')

white_png = Image.open(PNG_WHITE)
PNG_WHITE_RGB = white_png.convert('RGB')

half_bw = Image.open(PNG_HALF_BW)
PNG_HALF_BW_RGB = half_bw.convert('RGB')

class ImageCompareTest(unittest.TestCase):

    def test_thresholds(self):
        self.assertEqual(imgcompare.image_diff_percent(JPG_BLACK, JPG_BLACK), 0)
        self.assertEqual(imgcompare.image_diff_percent(JPG_BLACK, JPG_WHITE), 100)
        self.assertEqual(imgcompare.image_diff_percent(JPG_BLACK, JPG_HALF_BW), 50)

    def test_png_jpg_black_white(self):
        # to compare 'l' png with jpg, it has to be converted to RGB
        self.assertEqual(imgcompare.image_diff_percent(PNG_BLACK_RGB, JPG_BLACK), 0)
        self.assertEqual(imgcompare.image_diff_percent(PNG_WHITE_RGB, JPG_WHITE), 0)

    def test_bad_size(self):
        self.assertRaisesRegexp(imgcompare.ImageCompareException, "different image sizes", imgcompare.image_diff_percent, JPG_CAT, JPG_CAT_BAD_SIZE)

    def test_bad_mode(self):
        self.assertRaisesRegexp(imgcompare.ImageCompareException, "different image mode", imgcompare.image_diff_percent, JPG_BLACK, PNG_BLACK)

    def test_half_black(self):
        self.assertEqual(imgcompare.image_diff_percent(PNG_HALF_BW, PNG_BLACK), 50)
        self.assertEqual(imgcompare.image_diff_percent(PNG_HALF_BW, PNG_WHITE), 50)
        self.assertEqual(imgcompare.image_diff_percent(PNG_BLACK, PNG_HALF_BW), 50)
        self.assertEqual(imgcompare.image_diff_percent(PNG_WHITE, PNG_HALF_BW), 50)

        self.assertEqual(imgcompare.image_diff_percent(JPG_HALF_BW, JPG_BLACK), 50)
        self.assertEqual(imgcompare.image_diff_percent(JPG_HALF_BW, JPG_WHITE), 50)
        self.assertEqual(imgcompare.image_diff_percent(JPG_BLACK, JPG_HALF_BW), 50)
        self.assertEqual(imgcompare.image_diff_percent(JPG_WHITE, JPG_HALF_BW), 50)

    def test_jpg_reencode_diff(self):
        # when a png is converted two jpeg two times to a different file with the same encoder
        # diff is 0
        self.assertEqual(imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_DIFFERENT_RUN), 0)

        # when reencoding the same jpg again, a minimal diff is found
        self.assertLess(imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_REENCODED), 0.015)


    def test_foo(self):
        r = 255
        g = 100
        b = 100



    def test_rgb(self):
        # small changes on the image result in a bigger diff than jpg reencode

        initial = Image.open("testimages/rgb.bmp")

        initial.convert('L').save("testimages/third.bmp")

        # diff = ImageChops.difference(Image.open("testimages/2x2_red.jpg"), Image.open("testimages/2x2_blue.jpg"))
        # #diff = ImageChops.difference(Image.open(JPG_CAT), Image.open(JPG_CAT_SLIGHT_DIFF))
        # diff_conv = diff.convert('L')
        # hist = diff_conv.histogram()
        #
        # total = imgcompare.imgcompare.total_histogram_diff(diff_conv)
        #
        # #raw_enc = diff.tobytes("raw").hex()
        # #raw_conv = diff_conv.tobytes("raw").hex()
        # # bmp_enc = diff.tobytes("hex").hex()
        #
        # #print("RAW: " + str(raw_enc))
        # #print("CONV: " + str(raw_conv))
        # # for index, e in enumerate(hist):
        # #     if e != 0:
        # #         print("HIST: index=" +str(index) + " val="+str(e))
        # #
        # print("TOTAL: " + str(total))

    def test_histogram(self):
        # small changes on the image result in a bigger diff than jpg reencode

        diff = ImageChops.difference(Image.open("testimages/2x2_red.jpg"), Image.open("testimages/2x2_blue.jpg"))
        #diff = ImageChops.difference(Image.open(JPG_CAT), Image.open(JPG_CAT_SLIGHT_DIFF))
        diff_conv = diff.convert('L')
        hist = diff_conv.histogram()

        total = imgcompare.imgcompare.total_histogram_diff(diff_conv)

        #raw_enc = diff.tobytes("raw").hex()
        #raw_conv = diff_conv.tobytes("raw").hex()
        # bmp_enc = diff.tobytes("hex").hex()

        #print("RAW: " + str(raw_enc))
        #print("CONV: " + str(raw_conv))
        # for index, e in enumerate(hist):
        #     if e != 0:
        #         print("HIST: index=" +str(index) + " val="+str(e))
        #
        print("TOTAL: " + str(total))

    def test_minimal_image_diff(self):
        # small changes on the image result in a bigger diff than jpg reencode
        self.assertEqual(round(imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_SLIGHT_DIFF), 2), 0.34)
#        self.assertEqual(round(imgcompare.image_diff_percent(PNG_CAT, PNG_CAT_SLIGHT_DIFF), 2), 0.28)

        # diffing jpg with png results in a lot different results
#        self.assertEqual(round(imgcompare.image_diff_percent(JPG_CAT, PNG_CAT_SLIGHT_DIFF), 2), 15.96)
#        self.assertEqual(round(imgcompare.image_diff_percent(PNG_CAT_SLIGHT_DIFF, JPG_CAT), 2), 15.96)

    def test_black_white_image_diff(self):
        self.assertEqual(round(imgcompare.image_diff_percent(JPG_CAT, JPG_BLACK), 2), 27.58)
        self.assertEqual(round(imgcompare.image_diff_percent(JPG_CAT, JPG_WHITE), 2), 72.07)
        self.assertEqual(round(imgcompare.image_diff_percent(JPG_CAT, JPG_HALF_BW), 2), 55.15)

        self.assertEqual(round(imgcompare.image_diff_percent(PNG_CAT, PNG_BLACK_RGB), 2), 11.63)
        self.assertEqual(round(imgcompare.image_diff_percent(PNG_CAT, PNG_WHITE_RGB), 2), 88.04)
        self.assertEqual(round(imgcompare.image_diff_percent(PNG_CAT, PNG_HALF_BW_RGB), 2), 53.46)

    def test_is_equal(self):
        self.assertTrue(imgcompare.is_equal(JPG_CAT, JPG_CAT_SLIGHT_DIFF, 0.5))
        self.assertFalse(imgcompare.is_equal(JPG_CAT, JPG_CAT_SLIGHT_DIFF, 0.2))
        self.assertTrue(imgcompare.is_equal(JPG_BLACK, JPG_BLACK))
        self.assertTrue(imgcompare.is_equal(JPG_BLACK, JPG_BLACK, 0.2))

if __name__ == "__main__":
    import unittest

    unittest.main()
