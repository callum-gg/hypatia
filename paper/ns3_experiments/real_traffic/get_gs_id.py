import socket
import geocoder
import requests
import math

def get_gs_id(website="www.barcoo.qld.gov.au"):
    response = requests.get("https://" + website)
    size = len(response.content) # in bytes
    ip_address = socket.gethostbyname(website)
    latitude, longitude = geocoder.ip(ip_address).latlng    

    # Get closest groundstation
    closest_gs = None
    closest_dist = 0
    # Simulate sending this data from the closest groundstation to a different groundstation

    # Import GS file
    # Need to ensure the file path is correct
    gs_file = "./paper/satellite_networks_state/gen_data/starlink_550_isls_none_ground_stations_top_100_algorithm_free_one_only_over_isls/ground_stations.txt"
    with open(gs_file, "r") as file:
        gs_lines = file.read().splitlines()
        for i in range(1, len(gs_lines)):
            latitude_gs, longitude_gs = map(float, gs_lines[i].split(",")[2:4])
            dist = math.acos((math.sin(math.radians(latitude_gs)) * \
                        math.sin(math.radians(latitude))) + \
                        (math.cos(math.radians(latitude_gs)) * \
                        math.cos(math.radians(latitude)) * \
                        math.cos(math.radians(longitude) - \
                        math.radians(longitude_gs)))) * 6378135
            if closest_gs is None or dist < closest_dist:
                closest_gs = gs_lines[i]
                closest_dist = dist
    
    return closest_gs.split(",")[0]