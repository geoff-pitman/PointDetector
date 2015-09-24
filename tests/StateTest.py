import unittest

from geo.Point import Point
from geo.State import State


class StateTest(unittest.TestCase):
    """
    Tests of methods of the State class
    """
    def setUp(self):
        """
        Create a basic 5 sided state for other tests
        """
        self.border_points = [[-142.67, 77.34], [-10.323, 95.55], [10.67, 85.56],
                              [44.22, 76.88], [-20.99, 55.59], [-142.67, 77.34]]
        self.test_state = State("Test State", self.border_points)

        self.border_points = [[30, 30], [45, 15], [15, 15], [30, 30]]
        self.triangle_state = State("Triangle Test State", self.border_points)

    def test_border_extremes(self):
        """
        Tests that the compass direction extremes of the state are properly computed
        """
        self.assertEqual(-142.67, self.test_state.westmost, "Westmost border boundary not computed properly")
        self.assertEqual(95.55, self.test_state.northmost, "Northmost border boundary not computed properly")
        self.assertEqual(44.22, self.test_state.eastmost, "Eastmost border boundary not computed properly")
        self.assertEqual(55.59, self.test_state.southmost, "Southmost border boundary not computed properly")

    def test_border_count(self):
        """
        Tests that the number of borders that are calculated matches what is expected
        """
        self.assertEqual(5, len(self.test_state.borders), "Number of borders not generated correctly")

    def test_doesnt_contain_point(self):
        """
        Tests that a point outside of the state is registered as such
        """
        self.assertFalse(self.test_state.contains_point(Point(-75, 93)), "Point incorrectly considered in state")

    def test_contains_point(self):
        """
        Tests that a point inside of the state is registered as such
        """
        self.assertTrue(self.test_state.contains_point(Point(5, 88)), "Point incorrectly considered out of state")

    def test_vertex_point(self):
        """
        Tests that a point on the vertex of a border point is not within a state
        """
        self.assertFalse(self.test_state.contains_point(Point(-20.99, 55.59)), "Point on vertex considered in state")

    def test_horizontal_point(self):
        """
        Tests that a point on a horizontal border is not within a state
        """
        self.assertFalse(self.triangle_state.contains_point(Point(30, 15)),
                         "Point on horizontal border considered in state")

    def test_border_point(self):
        """
        Tests that a point on a border is not within a state
        """
        self.assertFalse(self.triangle_state.contains_point(Point(25, 15)),
                         "Point on non-horizontal border considered in state")

