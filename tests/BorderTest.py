import math
import unittest

from utils.Border import Border
from utils.Point import Point


class BorderTest(unittest.TestCase):
    """
    Tests of methods of the Border class
    """
    def test_slope_regular(self):
        """
        Tests computing slope of a non vertical and non horizontal line
        """
        start = Point(-79.2, 40)
        end = Point(-86.2, 33)
        border = Border(start, end)
        self.assertEqual(1.0, border._get_slope(), "Regular slope calculation not working")

    def test_slope_horizontal(self):
        """
        Tests computing slope of a horizontal line
        """
        start = Point(-79.2, 40)
        end = Point(-86.2, 40)
        border = Border(start, end)
        self.assertEqual(0, border._get_slope(), "Horizontal slope calculation not working")

    def test_slope_vertical(self):
        """
        Tests computing slope of a vertical line
        """
        start = Point(-79.2, 40)
        end = Point(-79.2, 33)
        border = Border(start, end)
        self.assertTrue(math.isinf(border._get_slope()), "Vertical slope calculation not working")

    def test_y_intercept_regular(self):
        """
        Tests computing y-intercept of a non vertical and non horizontal line
        """
        start = Point(-79.2, 40)
        end = Point(-86.2, 33)
        border = Border(start, end)
        self.assertEqual(119.2, border._get_x_intercept(), "Regular y-intercept calculation not working")

    def test_y_intercept_horizontal(self):
        """
        Tests computing y-intercept of a horizontal line
        """
        start = Point(-79.2, 40)
        end = Point(-86.2, 40)
        border = Border(start, end)
        self.assertTrue(math.isnan(border._get_x_intercept()), "Horizontal y-intercept calculation not working")

    def test_y_intercept_vertical(self):
        """
        Tests computing y-intercept of a vertical line
        """
        start = Point(-79.2, 40)
        end = Point(-79.2, 33)
        border = Border(start, end)
        self.assertEqual(-79.2, border._get_x_intercept(), "Vertical y-intercept calculation not working")
