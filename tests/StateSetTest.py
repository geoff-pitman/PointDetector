import unittest

from geo.Point import Point
from geo.StateSet import StateSet


class StateSetTest(unittest.TestCase):
    """
    Tests of methods of the StateSet class
    """
    def setUp(self):
        """
        Creates a four state grid of pentagonal states for verifiying potential and actual states patches
        """
        with open('state_set_test.json') as states_file:
            self.state_set = StateSet(states_file)

    def test_state_and_state_border_count(self):
        """
        Tests that the correct number of states have been created and that each has the correct number of borders
        """
        self.assertEquals(len(self.state_set.states), 4, "Incorrect number of states loaded")
        for state in self.state_set.states:
            self.assertEqual(len(state.borders), 5, "Incorrect number of borders on " + state.name)

    def test_no_potential_matches(self):
        """
        Tests that points outside of all heuristic state squares don't return a potential match
        """
        states = self.state_set._get_potential_states(Point(-25.55, 120))
        self.assertEqual([], states, "False positive potential match when too far north")
        states = self.state_set._get_potential_states(Point(-180, 53))
        self.assertEqual([], states, "False positive potential match when too far west")
        states = self.state_set._get_potential_states(Point(80, 53))
        self.assertEqual([], states, "False positive potential match when too far east")
        states = self.state_set._get_potential_states(Point(-25.55, 2))
        self.assertEqual([], states, "False positive potential match when too far south")

    def test_potential_matches_single(self):
        """
        Tests for the correct individual matches for each quadrant
        """
        state = self.state_set._get_potential_states(Point(-148, 33))
        self.assertEqual("West State", state[0].name, "Potential state not being detected properly in west quadrant")
        state = self.state_set._get_potential_states(Point(-10, 80))
        self.assertEqual("North State", state[0].name, "Potential state not being detected properly in north quadrant")
        state = self.state_set._get_potential_states(Point(-18, 20))
        self.assertEqual("South State", state[0].name, "Potential state not being detected properly in south quadrant")
        state = self.state_set._get_potential_states(Point(42, 53))
        self.assertEqual("East State", state[0].name, "Potential state not being detected properly in east quadrant")

    def test_potential_matches_multiple(self):
        """
        Tests for the correct pairs of potential matches in all combination of quadrant matches
        """
        states = self.state_set._get_potential_states(Point(-25.55, 53))
        self.assertEqual("West State", states[0].name,
                         "Potential states not being detected properly in west quadrant for west-south test")
        self.assertEqual("South State", states[1].name,
                         "Potential states not being detected properly in south quadrant for west-south test")
        states = self.state_set._get_potential_states(Point(-120, 60))
        self.assertEqual("North State", states[0].name,
                         "Potential states not being detected properly in north quadrant for north-west test")
        self.assertEqual("West State", states[1].name,
                         "Potential states not being detected properly in west quadrant for north-west test")
        states = self.state_set._get_potential_states(Point(42, 58))
        self.assertEqual("North State", states[0].name,
                         "Potential states not being detected properly in north quadrant for north-east test")
        self.assertEqual("East State", states[1].name,
                         "Potential states not being detected properly in west quadrant for north-east test")
        states = self.state_set._get_potential_states(Point(2, 23))
        self.assertEqual("South State", states[0].name,
                         "Potential states not being detected properly in south quadrant for south-east test")
        self.assertEqual("East State", states[1].name,
                         "Potential states not being detected properly in east quadrant for south-east test")

    def test_point_not_contained(self):
        """
        Tests that points outside of quandrants do not return a false positive containment match
        """
        state = self.state_set.get_containing_state(Point(-25.55, 120))
        self.assertIsNone(state, "False positive contained match when too far north")
        state = self.state_set.get_containing_state(Point(-180, 53))
        self.assertIsNone(state, "False positive contained match when too far west")
        state = self.state_set.get_containing_state(Point(80, 53))
        self.assertIsNone(state, "False positive contained match when too far east")
        state = self.state_set.get_containing_state(Point(-25.55, 2))
        self.assertIsNone(state, "False positive countained match when too far south")

    def test_point_contained(self):
        """
        Tests for the correct containing state identification for each quadrant
        """
        state = self.state_set.get_containing_state(Point(-25.55, 53))
        self.assertEqual("West State", state.name, "Point location not being detected properly in west quadrant")
        state = self.state_set.get_containing_state(Point(-21, 62))
        self.assertEqual("North State", state.name, "Point location not being detected properly in west quadrant")
        state = self.state_set.get_containing_state(Point(42, 58))
        self.assertEqual("East State", state.name, "Point location not being detected properly in east quadrant")
        state = self.state_set.get_containing_state(Point(2, 23))
        self.assertEqual("South State", state.name, "Point Location not being detected properly in south quadrant")
