import exputil
import time
from get_gs_id import get_gs_id

satellite_network = "starlink_550_isls_none_ground_stations_top_100_algorithm_free_one_only_over_isls"
gen_data_path = "../../../paper/satellite_networks_state/gen_data/" + satellite_network + "/"
interval = 100 # interval times in ms
length = 10 # total time in seconds
max_num_processes = 4

end_gs = 27
start_gs = get_gs_id(gen_data_path)
if end_gs == start_gs:
    print("Warning: start and end locations are the same")
states_path = "dynamic_state" + str(interval) + "ms_for_" + str(length) + "s"

# Need to get number of satellites

# Generate config file from configuration in this script????

# STEP 1

run_dir = "./runs/" # only having 1 run

local_shell = exputil.LocalShell()

local_shell.remove_force_recursive(run_dir) # clear up any previous runs
local_shell.make_full_dir(run_dir) # create the run directory

# set configuration properties
local_shell.copy_file("templates/template_config_ns3.properties", run_dir + "/config_ns3.properties")

local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[SATELLITE-NETWORK]", satellite_network)
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[DYNAMIC-STATE]", states_path)
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[SIMULATION-END-TIME-NS]", str(length * 1_000_000_000))
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[DYNAMIC-STATE-UPDATE-INTERVAL-NS]", str(interval * 1_000_000))
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[ISL-DATA-RATE-MEGABIT-PER-S]", str(10.0))
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[GSL-DATA-RATE-MEGABIT-PER-S]", str(10.0))
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[ISL-MAX-QUEUE-SIZE-PKTS]", str(100))
local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties", "[GSL-MAX-QUEUE-SIZE-PKTS]", str(100))

# schedule.csv
# local_shell.copy_file("templates/template_tcp_a_b_schedule.csv", run_dir + "/schedule.csv")
# local_shell.sed_replace_in_file_plain(run_dir + "/schedule.csv", "[FROM]", str(run["from_id"]))
# local_shell.sed_replace_in_file_plain(run_dir + "/schedule.csv", "[TO]", str(run["to_id"]))

print("Successfully generated runs")

# STEP 2

commands_to_run = []
logs_ns3_dir = "runs/logs_ns3"
local_shell.remove_force_recursive(logs_ns3_dir)
local_shell.make_full_dir(logs_ns3_dir)
commands_to_run.append(
    "cd ../../../ns3-sat-sim/simulator; " 
    "./waf --run=\"main_satnet --run_dir='../../paper/ns3_experiments/real_traffic/runs/'\" "
    "2>&1 | tee '../../paper/ns3_experiments/real_traffic/" + logs_ns3_dir + "/console.txt'"
)
# generate commands to run

# Run the commands
print("Running commands (at most %d in parallel)..." % max_num_processes)
for i in range(len(commands_to_run)):
    print("Starting command %d out of %d: %s" % (i + 1, len(commands_to_run), commands_to_run[i]))
    local_shell.detached_exec(commands_to_run[i])
    while local_shell.count_screens() >= max_num_processes:
        time.sleep(2)

# Awaiting final completion before exiting
print("Waiting completion of the last %d..." % max_num_processes)
while local_shell.count_screens() > 0:
    time.sleep(2)
print("Finished.")

# STEP 3

# Set up directories
local_shell.remove_force_recursive("pdf")
local_shell.make_full_dir("pdf")
local_shell.remove_force_recursive("data")
local_shell.make_full_dir("data")

local_shell.perfect_exec(
    "cd ../../../ns3-sat-sim/simulator/contrib/basic-sim/tools/plotting/plot_tcp_flow; "
    "python plot_tcp_flow.py "
    "../../../../../../../paper/ns3_experiments/real_traffic/runs/logs_ns3 "
    "../../../../../../../paper/ns3_experiments/real_traffic/data "
    "../../../../../../../paper/ns3_experiments/real_traffic/pdf "
    "0 " + str(1 * 1000 * 1000 * 1000),  # Flow 0, 1 * 1000 * 1000 * 1000 ns = 1s interval
    output_redirect=exputil.OutputRedirect.CONSOLE
)
