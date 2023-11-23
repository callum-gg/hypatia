import requests
import json
import os
from dotenv import load_dotenv
from skyfield.sgp4lib import EarthSatellite
from skyfield.api import load
from skyfield.toposlib import wgs84

# Load .env file
load_dotenv()

# API URLs
base_url = "https://www.space-track.org"
request_login = "/ajaxauth/login"

# Log into session using credentials
session = requests.Session()
resp = session.post(base_url + request_login, data = {
    "identity": os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD")
})
# Check session has successfully been logged into
logged_in = False
if resp.status_code != 200 or resp.text == "{\"Login\":\"Failed\"}":
    print("POST fail on login")
    session.close()
else:
    logged_in = True

def GetSatellitesData():
    if not logged_in:
        return
    # Could change to only return necessary data (speed up requests?)
    resp = session.get("https://www.space-track.org/basicspacedata/query/class/gp/OBJECT_NAME/STARLINK-%5E")
    # resp = session.get("https://www.space-track.org/basicspacedata/query/class/gp/OBJECT_NAME/STARLINK-%5E/limit/1")

    # Error handling
    satellites = json.loads(resp.text)

    # Generate positional information
    time_now = load.timescale().now()
    for i in range(0, len(satellites)):
        # Need to adjust for time data was taken from
        # And adjust current values as well
        satellite = EarthSatellite(satellites[i]["TLE_LINE1"], satellites[i]["TLE_LINE2"])#, ts=)
        geocentric = satellite.at(time_now)
        lat, lon = wgs84.latlon_of(geocentric)
        satellites[i]["LATITUDE"], satellites[i]["LONGITUDE"] = lat.degrees, lon.degrees

    # Debug information
    # print("Number of Starlink satellites:", len(satellites))
    # print("Example Satellite:")
    # print(json.dumps(satellites[0]))

    # Process data for correct output

    return satellites

if __name__ == "__main__":
    GetSatellitesData()

# Close session
# Might cause issues?
session.close()