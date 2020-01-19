import unittest

RED_FACT = 19595
GREEN_FACT = 38470
BLUE_FACT = 7471
BITS=16

def convert_one(r, g, b):
    y = (RED_FACT*r + GREEN_FACT*g + BLUE_FACT*b) >> 16
    return y

def convert_two(r,g,b):
    y = (RED_FACT * r + GREEN_FACT * g + BLUE_FACT * b + 32768) >> 16
    return y

def convert_three(r,g,b):
    y = round((RED_FACT * r + GREEN_FACT * g + BLUE_FACT * b) / 2 ** 16)
    return y

class PilTest(unittest.TestCase):

    def test_converts(self):
        r = 0
        g = 1
        b = 0

        one = convert_one(r, g, b)
        print("ONE: " + str(one))

        two = convert_two(r, g, b)
        print("TWO: " + str(two))

        three = convert_three(r, g, b)
        print("THREE: " + str(three))

        self.assertEqual(one, two)

