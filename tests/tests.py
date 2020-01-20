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
import os
import unittest

from PIL import Image

import imgcompare

dir_path = os.path.dirname(os.path.realpath(__file__))

PNG_CAT = dir_path + "/testimages/cat.png"
PNG_BLACK = dir_path + "/testimages/black.png"
PNG_WHITE = dir_path + "/testimages/white.png"
PNG_HALF_BW = dir_path + "/testimages/half_black_white.png"
PNG_CAT_SLIGHT_DIFF = dir_path + "/testimages/cat_slight_diff.png"

JPG_CAT = dir_path + "/testimages/cat.jpg"
JPG_FOX = dir_path + "/testimages/fox.jpg"
JPG_CAT_BAD_SIZE = dir_path + "/testimages/cat_bad_size.jpg"
JPG_CAT_SLIGHT_DIFF = dir_path + "/testimages/cat_slight_diff.jpg"
JPG_CAT_DIFFERENT_RUN = dir_path + "/testimages/cat_jpg_different_run.jpg"
JPG_CAT_REENCODED = dir_path + "/testimages/cat_jpg_reencoded.jpg"
JPG_BLACK = dir_path + "/testimages/black.jpg"
JPG_WHITE = dir_path + "/testimages/white.jpg"
JPG_HALF_BW = dir_path + "/testimages/half_black_white.jpg"
JPG_RED_GREEN_BLUE = dir_path + "/testimages/red_green_blue.jpg"
JPG_RED_GREEN_GREEN = dir_path + "/testimages/red_green_green.jpg"

black_png = Image.open(PNG_BLACK)
PNG_BLACK_RGB = black_png.convert('RGB')

white_png = Image.open(PNG_WHITE)
PNG_WHITE_RGB = white_png.convert('RGB')

half_bw = Image.open(PNG_HALF_BW)
PNG_HALF_BW_RGB = half_bw.convert('RGB')


class ImageCompareTest(unittest.TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        PNG_BLACK_RGB.close()
        PNG_WHITE_RGB.close()
        PNG_HALF_BW_RGB.close()

    def test_version(self):
        self.assertEqual("2.0.1", imgcompare.__version__)

    def test_thresholds(self):
        self.assertEqual(0, imgcompare.image_diff_percent(JPG_BLACK, JPG_BLACK))
        self.assertEqual(100, imgcompare.image_diff_percent(JPG_BLACK, JPG_WHITE))
        self.assertEqual(50, imgcompare.image_diff_percent(JPG_BLACK, JPG_HALF_BW))

    def test_png_jpg_black_white(self):
        # to compare 'l' png with jpg, it has to be converted to RGB
        self.assertEqual(0, imgcompare.image_diff_percent(PNG_BLACK_RGB, JPG_BLACK))
        self.assertEqual(0, imgcompare.image_diff_percent(PNG_WHITE_RGB, JPG_WHITE))

    def test_bad_size(self):
        self.assertRaisesRegex(imgcompare.ImageCompareException, "different image sizes",
                                imgcompare.image_diff_percent, JPG_CAT, JPG_CAT_BAD_SIZE)

    def test_bad_mode(self):
        self.assertRaisesRegex(imgcompare.ImageCompareException, "different image mode", imgcompare.image_diff_percent,
                                JPG_BLACK, PNG_BLACK)

    def test_cat_fox(self):
        self.assertEqual(23.45, round(imgcompare.image_diff_percent(JPG_CAT, JPG_FOX), 2))
        self.assertEqual(23.45, round(imgcompare.image_diff_percent(JPG_FOX, JPG_CAT), 2))

    def test_red_green_blue(self):
        self.assertEqual(23.4, round(imgcompare.image_diff_percent(JPG_RED_GREEN_BLUE, JPG_RED_GREEN_GREEN), 2))

    def test_half_black(self):
        self.assertEqual(50, imgcompare.image_diff_percent(PNG_HALF_BW, PNG_BLACK))
        self.assertEqual(50, imgcompare.image_diff_percent(PNG_HALF_BW, PNG_WHITE))
        self.assertEqual(50, imgcompare.image_diff_percent(PNG_BLACK, PNG_HALF_BW))
        self.assertEqual(50, imgcompare.image_diff_percent(PNG_WHITE, PNG_HALF_BW))

        self.assertEqual(50, imgcompare.image_diff_percent(JPG_HALF_BW, JPG_BLACK))
        self.assertEqual(50, imgcompare.image_diff_percent(JPG_HALF_BW, JPG_WHITE))
        self.assertEqual(50, imgcompare.image_diff_percent(JPG_BLACK, JPG_HALF_BW))
        self.assertEqual(50, imgcompare.image_diff_percent(JPG_WHITE, JPG_HALF_BW))

    def test_jpg_reencode_diff(self):
        # when a png is converted two jpeg two times to a different file with the same encoder
        # diff is 0
        self.assertEqual(0, imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_DIFFERENT_RUN))

        # when reencoding the same jpg again, a minimal diff is found
        self.assertLess(imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_REENCODED), 0.024)

    def test_minimal_image_diff(self):
        # small changes on the image result in a bigger diff than jpg reencode
        self.assertEqual(0.35, round(imgcompare.image_diff_percent(JPG_CAT, JPG_CAT_SLIGHT_DIFF), 2))
        self.assertEqual(0.28, round(imgcompare.image_diff_percent(PNG_CAT, PNG_CAT_SLIGHT_DIFF), 2))

        # diffing jpg with png results in a lot different results
        self.assertEqual(16.13, round(imgcompare.image_diff_percent(JPG_CAT, PNG_CAT_SLIGHT_DIFF), 2))
        self.assertEqual(16.13, round(imgcompare.image_diff_percent(PNG_CAT_SLIGHT_DIFF, JPG_CAT), 2))

    def test_black_white_image_diff(self):
        self.assertEqual(27.75, round(imgcompare.image_diff_percent(JPG_CAT, JPG_BLACK), 2))
        self.assertEqual(72.25, round(imgcompare.image_diff_percent(JPG_CAT, JPG_WHITE), 2))
        self.assertEqual(55.32, round(imgcompare.image_diff_percent(JPG_CAT, JPG_HALF_BW), 2))

        self.assertEqual(11.79, round(imgcompare.image_diff_percent(PNG_CAT, PNG_BLACK_RGB), 2))
        self.assertEqual(88.21, round(imgcompare.image_diff_percent(PNG_CAT, PNG_WHITE_RGB), 2))
        self.assertEqual(53.62, round(imgcompare.image_diff_percent(PNG_CAT, PNG_HALF_BW_RGB), 2))

    def test_is_equal(self):
        self.assertTrue(imgcompare.is_equal(JPG_CAT, JPG_CAT_SLIGHT_DIFF, 0.5))
        self.assertFalse(imgcompare.is_equal(JPG_CAT, JPG_CAT_SLIGHT_DIFF, 0.2))
        self.assertTrue(imgcompare.is_equal(JPG_BLACK, JPG_BLACK))
        self.assertTrue(imgcompare.is_equal(JPG_BLACK, JPG_BLACK, 0.2))


if __name__ == "__main__":
    import unittest

    unittest.main()
