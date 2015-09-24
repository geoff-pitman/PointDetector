#!/usr/bin/env bash
# Script to test results.  Didn't do a unit test suite because of how the server is run and overhead of python http requests
curl  -d "longitude=-77.036133&latitude=40.513799" http://localhost:8080/ # Pennsylvania
curl  -d "longitude=-77.036133" http://localhost:8080/ # Missing latitude Argument
curl  -d "latitude=40.513799" http://localhost:8080/ # Missing longitude Argument
curl  -d " " http://localhost:8080/ # Missing longitude and latitude
curl  -d "longitude=145.444&latitude=40.513799" http://localhost:8080/ # Coordinate not within state
curl  -d "longitude=-72&latitude=43" http://localhost:8080/ # New Hampshire
curl  -d "longitude=-120&latitude=40" http://localhost:8080/ # California