import math

from .Border import Border
from .Point import Point


class State:
    """
    A state's geographical mapping

    @ivar westmost: furthest west longitude of the state
    @ivar eastmost: furthest east longitude of the state
    @ivar northmost: furthest north longitude of the state
    @ivar southmost: furthest south longitude of the state
    @ivar name: State name
    @ivar borders: list of state borders
    """
    def __init__(self, name, points):
        """
        Sets up the basic data to define a State

        @param name: Name of the state
        @param points: Points that compose the border
        """
        self.name = name
        self.westmost = points[0][0]
        self.eastmost = points[0][0]
        self.northmost = points[0][1]
        self.southmost = points[0][1]
        self.borders = self._resolve_borders_and_extremes(points)

    def _resolve_borders_and_extremes(self, points):
        """
        Sets up the borders for a state and all of the compass direction extremes

        @param points: All points that comprise the state
        @return: A list of all border lines that outline the state
        """
        borders = []
        for current_index in range(0, len(points)-1):
            current_point = points[current_index]
            next_point = points[current_index+1]
            borders.append(
                Border(
                    Point(current_point[0], current_point[1]),
                    Point(next_point[0], next_point[1])))
            if next_point[0] < self.westmost:
                self.westmost = next_point[0]
            elif next_point[0] > self.eastmost:
                self.eastmost = next_point[0]
            if next_point[1] > self.northmost:
                self.northmost = next_point[1]
            elif next_point[1] < self.southmost:
                self.southmost = next_point[1]
        return borders

    def contains_point(self, point):
        """
        Checks if a point is inside or outside of the state using a take on a ray tracing algorithm

        Does this by checking every border and seeing where a horizontal ray would intersect the border if
        the border was a full blown line instead of a line segment. It then verifies if the intersection point actually
        exists on the real border. It increments if the intersection is west or east of the border.  An odd number on
        both sides means that the point is inside of the state, otherwise it is not.

        There are also checks to make sure that the point is not on a border/vertex itself

        @param point: Point to check
        @return: True if the point is inside of the state, False otherwise
        """
        west_intersects = 0
        east_intersects = 0
        for border in self.borders:
            border_start_lat = border.start_point.y
            border_start_lng = border.start_point.x
            border_end_lat = border.end_point.y
            border_end_lng = border.end_point.x
            if border.slope == 0:
                border_intersect = None
            elif math.isinf(border.slope):
                border_intersect = point.y
            else:
                border_intersect = (point.y - border.x_intercept)/border.slope
            if border_intersect is not None and \
                    ((border_start_lat >= border_end_lat and border_start_lat >= point.y >= border_end_lat) or
                     (border_end_lat >= border_start_lat and border_end_lat >= point.y >= border_start_lat)):
                # point is on border so cannot be in a specific state, weird math to account for float point rounding
                if .000000005 >= (abs(border_intersect) - abs(point.x)) >= -.000000005:
                    return False
                elif border_intersect > point.x:
                    east_intersects += 1
                elif border_intersect < point.x:
                    west_intersects += 1
            # point is on horizontal border so cannot be in a specific state
            elif border_intersect is None and border_start_lat == point.y and \
                ((border_start_lng >= border_end_lng and border_start_lng >= point.x >= border_end_lng) or
                 (border_end_lng >= border_start_lng and border_end_lng >= point.x >= border_start_lng)):
                return False
        if (west_intersects % 2 == 1) and (east_intersects % 2 == 1):
            return True
        else:
            return False
