import simplejson as json

def GenerateSatelliteJavascript(satellites):
    satellites_string = ""
    for j in range(len(satellites)):
        if str(satellites[j]["LONGITUDE"]) != "nan" and str(satellites[j]["LATITUDE"]) != "nan":
            satellites_string += "var satelliteSphere = viewer.entities.add({name : '" + satellites[j]["OBJECT_NAME"] + "', position: Cesium.Cartesian3.fromDegrees(" \
                            + str(satellites[j]["LONGITUDE"]) + ", " \
                            + str(satellites[j]["LATITUDE"]) + ", " + str(
                (float(satellites[j]["APOAPSIS"]) + float(satellites[j]["PERIAPSIS"])) * 500) + "), " \
                            + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                            + "material : Cesium.Color.BLACK.withAlpha(1),}});\n"
            
    # Show orbital rings

    # for key in orbit_links:
    #     sat1 = orbit_links[key]["sat1"]
    #     sat2 = orbit_links[key]["sat2"]
    #     satellites_string += "viewer.entities.add({name : '', polyline: { positions: Cesium.Cartesian3.fromDegreesArrayHeights([" \
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
    satellites_string += "document.getElementById('general-info').children[1].children[0].innerText = '" + str(len(satellites)) + "';\n"
    # Pass satellite data to JavaScript so can be shown in satellite info box

    satellites_string += "const satellite_data = JSON.parse('" + json.dumps(satellites, ignore_nan=True) + "');\n"

    return satellites_string

def GenerateGroundStationJavascript(groundstations):
    groundstations_string = ""
    for i in range(0, len(groundstations)):
        groundstations_string += "var groundstationSphere = viewer.entities.add({name : 'GROUNDSTATION', position: Cesium.Cartesian3.fromDegrees(" \
                        + str(groundstations[i]["LONGITUDE"]) + ", " \
                        + str(groundstations[i]["LATITUDE"]) + ", 0), " \
                        + "ellipsoid : {radii : new Cesium.Cartesian3(30000.0, 30000.0, 30000.0), " \
                        + "material : Cesium.Color.RED.withAlpha(1),}});\n"

    groundstations_string += "document.getElementById('general-info').children[1].children[1].innerText = '" + str(len(groundstations)) + "';\n"
    
    return groundstations_string
