## Live Data

These scripts provide some functionality with integrating the live satellite input data.

## Scripts

### Generate JavaScript

This script generates JavaScript for the visualisations. It is intended to be run by the `visualise_constellation.py` script.

### Get Groundstations Data

Provides a function to obtain ground station data in a Python dictionary from the ground station CSV files found in `paper/satellite_networks_state/input_data/`. This is used within `visualise_constellation.py` to get the list of ground stations to display in the visualisation.

### Visualise Constellation

This script visualises a constellation from live data. To change the constellation to visualise, change the value passed with the function `GetSatellitesData`. To change the ground station file, pass the name of a ground station file in the `GetGroundStationsData` function. You can create a visualisation by running the script:

```
python visualise_constellation.py
```

The visualisation will be saved in `satviz/viz_output`.
