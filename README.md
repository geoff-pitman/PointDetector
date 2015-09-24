# PointDetector
Detects what state a given point is located in  

It loads in border and name data about states from a separate JSON file.  

When supplied a point  it first uses rectangulized versions of all state borders to see what states may be potential matches. 
Then it looks at all of the borders using ray-tracing for the potential matches.  
If there is a match it returns a plain text string representation in an HTTP response.
Otherwise it returns a plain text error message.  
A point on any borders is considered not be within a state.  

Server can be run with  

python3 PointDetector.py  

Main server file is PointDetector.py, all other relevant classes are in the geo module, and unit tests are in the tests module  

Documentation has been generated using epydoc and can be perused by opening docs/index.html in a browser  


