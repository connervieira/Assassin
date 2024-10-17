# Assassin

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.


import json
import os
import time

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
display_notice = utils.display_notice


# Locate and load the configuration file.
config = load_config()


import subprocess


def load_predator_config(predator_instance_directory):
    config_file_path = os.path.join(predator_instance_directory, "config.json")
    if (os.path.exists(config_file_path)):
        with open(config_file_path) as configuration_file:
            raw_configuration_file_contents = configuration_file.read() # Read the contents of the configuration file.

        if (utils.is_json(raw_configuration_file_contents)):
            config = json.loads(raw_configuration_file_contents) # Load the configuration database from the contents of the config.json file.
        else:
            config = {} # Set the configuration to a blank placeholder dictionary.
            display_notice("The Predator configuration file appears to be invalid.", 3)
    else:
        config = {} # Set the configuration to a blank placeholder dictionary.
        display_notice("The Predator configuration file does not exist inside the configured Predator instance directory.", 3)
    return config

if (config["general"]["predator_integration"]["enabled"] == True): # Check to see if Predator integration is enabled.
    predator_config = load_predator_config(config["general"]["predator_integration"]["instance_directory"])


active_predator_hotlist = {}
def start_predator():
    global active_predator_hotlist
    global predator_config
    if (config["general"]["predator_integration"]["enabled"] == True): # Check to see if Predator alerts are enabled.
        debug_message("Initializing Predator")
        if (config["general"]["predator_integration"]["start_predator"] == True): # Check to see if Assassin is configured to start Predator.
            predator_path = config["general"]["predator_integration"]["instance_directory"]
            if (os.path.exists(predator_path) == True): # Check to see if an ADS-B message file has been set.
                start_command = ["python3",  predator_path + "/main.py", "2", "--headless", "2>/dev/null"] # This command is responsible for starting Predator.
                subprocess.Popen(start_command, stdout=subprocess.DEVNULL) # Execute the command to start Predator in the background.
            else:
                display_notice("Predator integration is enabled, but the configured instance directory does not exist. Predator could not be started.", 3)

    hotlist_filepath = os.path.join(predator_config["general"]["interface_directory"], "hotlist.json")
    if (os.path.exists(hotlist_filepath)):
        with open(hotlist_filepath) as file:
            file_contents = file.read() # Read the contents of the file.

        if (utils.is_json(file_contents)):
            active_predator_hotlist = json.loads(file_contents) # Load the active hotlist from the contents of the file.
        else:
            display_notice("The Predator hotlist interface file appears to be invalid.", 2)
    else:
        display_notice("The Predator hotlist interface file does not exist in the Predator interface directory.", 2)



def get_predator_plate_history():
    global predator_config
    plate_log_file_path = os.path.join(predator_config["general"]["working_directory"], predator_config["realtime"]["saving"]["license_plates"]["file"])

    if (predator_config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to make sure plate logging is enabled in Predator's configuration.
        if (os.path.exists(plate_log_file_path)): # Check to see if the plate log file exists.
            with open(plate_log_file_path) as plate_log_file: raw_plate_log_file_contents = plate_log_file.read() # Read the contents of the plate log file.

            if (utils.is_json(raw_plate_log_file_contents)):
                raw_plate_history = json.loads(raw_plate_log_file_contents) # Load the plate log from the contents of the plate log file.
            else:
                raw_plate_history = {}

            pruned_plate_history = {} # This is a placeholder that will hold the recent entries in the plate history.
            for timestamp in raw_plate_history: # Iterate through each entry in the raw plate history.
                if (float(timestamp) > time.time() - config["general"]["predator_integration"]["latch_time"]): # Check to see if this entry in the plate log file is within the configured latch time.
                    pruned_plate_history[timestamp] = raw_plate_history[timestamp] # Add this entry to the pruned plate history.
                    print(raw_plate_history[timestamp])
        else:
            display_notice("Predator integration is enabled, but the plate log file does not exist. Alerts could not be processed.", 2)
            pruned_plate_history = {}
    else:
        display_notice("Predator integration is enabled, but the plate log file is disabled. Alerts could not be processed.", 2)
        pruned_plate_history = {}

    return pruned_plate_history


# This function finds alerts from the pruned plate history.
def process_predator_alerts(pruned_plate_history):
    debug_message("Processing Predator alerts")
    global active_predator_hotlist

    predator_alerts = {} # This is a placeholder that will hold the active alerts from the plate history.
    for timestamp in pruned_plate_history: # Iterate through each entry in the plate log.
        for plate in pruned_plate_history[timestamp]["plates"]: # Iterate through each plate in this entry.
            if (len(pruned_plate_history[timestamp]["plates"][plate]["alerts"]) > 0): # Check to see if this plate is associated with any alerts.
                predator_alerts[plate] = {} # Initialize this plate in the Predator alerts.
                for rule in pruned_plate_history[timestamp]["plates"][plate]["alerts"]: # Iterate through each alert rule this plate is associated with.
                    predator_alerts[plate][rule] = active_predator_hotlist[rule] # Add this alert rule and it's information to the Predator alert.
            
    return predator_alerts
