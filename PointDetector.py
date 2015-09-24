import http.server
import socketserver
from urllib.parse import parse_qs

from utils.Point import Point
from utils.StateSet import StateSet

with open('states.json') as states_file:
    state_set = StateSet(states_file)

class PointHandler(http.server.BaseHTTPRequestHandler):
    """
    Handle a request to find what state a point exists within
    """
    def do_POST(self):
        """
        Parse the query string for the post request and and see if a state matches the coordinate
        :return: Error message if the point is not in a state or the state name
        """
        encoding = "UTF-8"
        message_length = int(self.headers['content-length'])
        message = self.rfile.read(message_length)
        arguments = parse_qs(message)
        lng = float(arguments[b'longitude'][0])
        lat = float(arguments[b'latitude'][0])
        state = state_set.get_containing_state(Point(lng, lat))
        if state is None:
            self.wfile.write(bytes("Nothing found", encoding))
        else:
            self.wfile.write(bytes(state.name + "\n", encoding))

httpd = socketserver.TCPServer(("", 8080), PointHandler)
print("Serving on port 8080")
httpd.serve_forever()
