class Border:
    """
    A border of a State

    Consists of a start point and end point for the border, and a slope and x-intercept if the border was a full
    line instead of a segment.  The values are used for a take on a ray tracing algorithm.

    @ivar start_point: Starting point of the border
    @ivar end_point: Ending point of the border
    @ivar slope: Slope of the border line
    @ivar x_intercept: extrapolated x intercept of the border line
    """
    def __init__(self, start_point, end_point):
        """
        Initializes a border

        @param start_point: Point the border line starts on
        @param end_point: Point the border line ends on
        """
        self.start_point = start_point
        self.end_point = end_point
        self.slope = self._get_slope()
        self.x_intercept = self._get_x_intercept()

    def _get_slope(self):
        """
        Find the slope of the border line

        @return: The slope of a non vertical line or infinity for a vertical line
        """
        if self.end_point.x - self.start_point.x == 0:
            return float('Inf')
        else:
            return (self.end_point.y - self.start_point.y)/(self.end_point.x - self.start_point.x)

    def _get_x_intercept(self):
        """
        Find the x intercept of the border line

        @return: The x intercept of a non-horizontal line or 0 for a horizontal line
        """
        if self.slope == float('Inf'):
            return self.start_point.x
        elif self.slope == 0:
            return float("NaN")
        else:
            return self.start_point.y - (self.slope * self.start_point.x)
