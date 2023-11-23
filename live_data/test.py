# - Show basic data in div - kinda done
# - Get groundstation locations - kinda done
# - Enhance Literature Review
# - Start writing methodology chapter

# Setting home directory for running
import os
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv("DIRECTORY"))

import sys
sys.path.append("satviz/scripts")

from get_satellites_data import GetSatellitesData
from get_groundstations_data import GetGroundStationsData
from generate_javascript import GenerateSatelliteJavascript, GenerateGroundStationJavascript

# Get satellites data
satellites = GetSatellitesData()
groundstations = GetGroundStationsData()

# HTML output file writer
output_file = open("satviz/viz_output/output.html", "w")
with open("satviz/static_html/top.html", "r") as top_html:
    output_file.write(top_html.read())

# Write extra script code for satellites
output_file.write(GenerateSatelliteJavascript(satellites))
output_file.write(GenerateGroundStationJavascript(groundstations))

with open("satviz/static_html/bottom.html", "r") as bottom_html:
    output_file.write(bottom_html.read())