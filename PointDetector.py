import http.server
import socketserver
from urllib.parse import parse_qs

from geo.Point import Point
from geo.StateSet import StateSet

with open('states.json') as states_file:
    state_set = StateSet(states_file)


class PointHandler(http.server.BaseHTTPRequestHandler):
    """
    Handle a request to find which state a point exists within
    """
    def do_POST(self):
        """
        Parse the query string for the post request and and see if a state matches the coordinate
        :return: Error message if there arent the proper arguments or if the point is not in a state. State name otherwise
        """
        encoding = "UTF-8"
        message_length = int(self.headers['content-length'])
        message = self.rfile.read(message_length)
        arguments = parse_qs(message, keep_blank_values=True)
        if b'longitude' in arguments and b'latitude' in arguments:
            lng = float(arguments[b'longitude'][0])
            lat = float(arguments[b'latitude'][0])
            state = state_set.get_containing_state(Point(lng, lat))
            if state is None:
                self.wfile.write(bytes("Coordinate not within state\n", encoding))
            else:
                self.wfile.write(bytes(state.name + "\n", encoding))
        elif b'longitude' in arguments:
            self.wfile.write(bytes("Missing latitude Argument\n", encoding))
        elif b'latitude' in arguments:
            self.wfile.write(bytes("Missing longitude Argument\n", encoding))
        else:
            self.wfile.write(bytes("Missing longitude and latitude Arguments\n", encoding))

port = 8080
httpd = socketserver.TCPServer(("", port), PointHandler)
print("Serving on port " + str(port))
httpd.serve_forever()
