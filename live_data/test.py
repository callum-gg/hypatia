# - Show basic data in div
# - Get groundstation locations
# - Enhance Literature Review
# - Start writing methodology chapter

# Setting home directory for running
import os
os.chdir("T:/ahhh/L3/Project/hypatia")

import sys
sys.path.append("satviz/scripts")

from get_satellites_data import GetSatellitesData

def GenerateSatelliteJavascript(satellites):
    viz_string = ""
    for j in range(len(satellites)):
        if str(satellites[j]["LONGITUDE"]) != "nan" and str(satellites[j]["LATITUDE"]) != "nan":
            viz_string += "var redSphere = viewer.entities.add({name : '', position: Cesium.Cartesian3.fromDegrees(" \
                            + str(satellites[j]["LONGITUDE"]) + ", " \
                            + str(satellites[j]["LATITUDE"]) + ", " + str(
                (float(satellites[j]["APOAPSIS"]) + float(satellites[j]["APOAPSIS"])) * 500) + "), " \
                            + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                            + "material : Cesium.Color.BLACK.withAlpha(1),}});\n"

    # for key in orbit_links:
    #     sat1 = orbit_links[key]["sat1"]
    #     sat2 = orbit_links[key]["sat2"]
    #     viz_string += "viewer.entities.add({name : '', polyline: { positions: Cesium.Cartesian3.fromDegreesArrayHeights([" \
    #                     + str(math.degrees(sat_objs[sat1]["sat_obj"].sublong)) + "," \
    #                     + str(math.degrees(sat_objs[sat1]["sat_obj"].sublat)) + "," \
    #                     + str(sat_objs[sat1]["alt_km"] * 1000) + "," \
    #                     + str(math.degrees(sat_objs[sat2]["sat_obj"].sublong)) + "," \
    #                     + str(math.degrees(sat_objs[sat2]["sat_obj"].sublat)) + "," \
    #                     + str(sat_objs[sat2]["alt_km"] * 1000) + "]), " \
    #                     + "width: 0.5, arcType: Cesium.ArcType.NONE, " \
    #                     + "material: new Cesium.PolylineOutlineMaterialProperty({ " \
    #                     + "color: Cesium.Color."+COLOR[i]+".withAlpha(0.4), outlineWidth: 0, outlineColor: Cesium.Color.BLACK})}});"

    # Code for displaying additional data
    viz_string += "document.getElementById('satellite-data').innerText = 'Number of Satellites: " + str(len(satellites)) + "'"

    return viz_string

# Get satellites data
satellites = GetSatellitesData()

# HTML output file writer
output_file = open("satviz/viz_output/output.html", "w")
with open("satviz/static_html/top.html", "r") as top_html:
    output_file.write(top_html.read())

# Write extra script code for satellites
output_file.write(GenerateSatelliteJavascript(satellites))

with open("satviz/static_html/bottom.html", "r") as bottom_html:
    output_file.write(bottom_html.read())