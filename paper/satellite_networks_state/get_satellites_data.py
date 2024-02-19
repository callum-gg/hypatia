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

def GetSatellitesData(object_name):
    print("Fetching live satellite positional data")
    if not logged_in:
        print("Session not valid")
        return
    # Could change to only return necessary data (speed up requests?)
    resp = session.get("https://www.space-track.org/basicspacedata/query/class/gp/OBJECT_NAME/" + object_name + "-%5E")
    # resp = session.get("https://www.space-track.org/basicspacedata/query/class/gp/OBJECT_NAME/" + object_name + "-%5E/limit/100")

    # Error handling
    satellites = json.loads(resp.text)

    # Generate positional information
    time_now = load.timescale().now()
    for i in range(0, len(satellites)):
        # Need to adjust for time data was taken from
        # And adjust current values as well
        satellite = EarthSatellite(satellites[i]["TLE_LINE1"], satellites[i]["TLE_LINE2"])
        geocentric = satellite.at(time_now)
        s_elapsed = (int(time_now.utc_strftime("%H")) * 60 + int(time_now.utc_strftime("%M"))) * 60 + int(time_now.utc_strftime("%S"))
        new_time = "{:.8f}".format(round(float(time_now.utc_strftime("%y%j")) + float(s_elapsed / 86400)), 8) # hours + mins + seconds / seconds in a day
        tle_line = satellites[i]["TLE_LINE1"][0:18] + new_time + satellites[i]["TLE_LINE1"][32:-1]
        check_sum = 0
        for j in range(0, len(tle_line)):
            if tle_line[j] == "-":
                check_sum += 1
            elif tle_line[j].isnumeric():
                check_sum += int(tle_line[j])
        satellites[i]["TLE_LINE1"] = tle_line + str(check_sum % 10)
        lat, lon = wgs84.latlon_of(geocentric)
        satellites[i]["LATITUDE"], satellites[i]["LONGITUDE"] = lat.degrees, lon.degrees
        satellites[i]["ALTITUDE"] = (float(satellites[i]["APOAPSIS"]) + float(satellites[i]["PERIAPSIS"])) * 500
        satellites[i]["ID"] = i

    # Debug information
    # print("Number of Starlink satellites:", len(satellites))
    # print("Example Satellite:")
    # print(json.dumps(satellites[0]))

    # Process data for correct output

    return satellites

if __name__ == "__main__":
    GetSatellitesData("STARLINK")

# Close session
session.close()