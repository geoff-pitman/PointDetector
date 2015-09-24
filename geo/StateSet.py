import json

from .State import State


class StateSet:
    """
    A collection of all states

    @ivar states: a list of all states in the dataset
    """
    def __init__(self, state_file):
        """
        Sets up the states that belong to the set

        @param state_file: a file of Json rows which each define a state
        """
        self.states = self._create_states(state_file)

    @staticmethod
    def _create_states(state_file):
        """
        Reads each row from the state json file and casts each one to its own state

        @param state_file: a file of Json rows which each define a state
        @return: a list of state representation for each row in the file
        """
        states = []
        for state_string in state_file:
            state_data = json.loads(state_string)
            states.append(State(state_data['state'], state_data['border']))
        return states

    def _get_potential_states(self, point):
        """
        Finds which states may contain the point specified

        This uses the maximum points of a state in thefour cardinal directions to approximate a state as a square.
        This means the point can be easily checked against four data points instead of checking all borders of a state.
        There is an extra initial cost at startup time, but I feel this is outweighed by the performance gain when
        handling requests.

        @param point: A point to check against for potential state matches
        @return: A list of states the point may exist within
        """
        potential_states = []
        for state in self.states:
            if state.eastmost > point.x > state.westmost and state.northmost > point.y > state.southmost:
                potential_states.append(state)
        return potential_states

    def get_containing_state(self, point):
        """
        Check all potential state matches to see if any contain the supplied point

        @param point: A point to check against for potential state matches
        @return: The state that contains the point specified or None
        """
        for state in self._get_potential_states(point):
            if state.contains_point(point):
                return state
        return None
