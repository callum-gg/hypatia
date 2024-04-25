# Satellite networks' state

This directory shows how to generate the satellite network state. It makes use of the
`satgenpy` or `satgen` Python module, which is located at the root of Hypatia.

For each satellite network defined in here (Kuiper-630, Starlink-550, Telesat-1015),
it generates for a ranging set of scenarios the following static state:

* List of satellites which are encoded using TLEs (_tles.txt_)
* List of ISLs (_isls.txt_)
* List of ground stations (_ground_stations.txt_)
* Description of the maximum GSL and ISL length in meters (_description.txt_)
* Number of GSL interfaces each node (satellite and ground station) has,
  and their total bandwidth sum (_gsl_interfaces_info.txt_)

... and the following dynamic state in discrete time steps:

* Forwarding state (`fstate_<time in ns>.txt`)
* GSL interface bandwidth (`gsl_if_bandwidth_<time in ns>.txt`)

This state is all essential for perform analyses and packet-level simulations.

Each Python file here adds that folder to its Python path. If you want your
editor to highlight things, you need to add `satgenpy` to your editor's
Python path.

## Getting started

1. Make sure you have all dependencies installed as prescribed in
   `<hypatia>/satgenpy/README.md`
2. Run from the main folder for the satellite networks used in the paper:

   ```
   bash generate_all_local.sh
   # Or if you have remote machines to distribute the workloads:
   # python generate_all_remote.py
   ```
3. ... which will generate:

   ```
   gen_data
   |-- 25x25_algorithm_free_one_only_over_isls
   |-- kuiper_630_isls_none_ground_stations_paris_moscow_grid_algorithm_free_one_only_gs_relays
   |-- kuiper_630_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls
   |-- starlink_550_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls
   |-- telesat_1015_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls
   ```

Or, configure and run `main_live.py [constellation name] [duration (s)] [time step (ms)] [isls_plus_grid / isls_none] [ground_stations_{top_100, paris_moscow_grid}] [algorithm_{free_one_only_over_isls, free_one_only_gs_relays, paired_many_only_over_isls}] [num threads]`

Within this script, filters can be applied to the constellation obtained. Edit the `FILTERS` variable:

```
FILTERS = {
	"KEY": "VALUE"
}
```

Where `KEY` is the field to receive ([Space-Track.org list of fields](https://www.space-track.org/basicspacedata/modeldef/class/gp/format/html)) and `VALUE` is a logical operator for the value ([Space-Track.org list of operators](https://www.space-track.org/documentation#api-restOperators)). For no filters to be applied, this can be left as an empty dictionary.

## Get Satellites Data

The file `get_satellites_data.py` is a helper script which obtains the live positional and orbital data of a specified satellite constellation. This script is used by `main_live.py` for network analysis and `live_data/visualise_constellation.py` to visualise the live satellite network.
