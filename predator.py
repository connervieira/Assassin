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
is_json = utils.is_json


# Locate and load the configuration file.
config = load_config()


import subprocess


def start_predator():
    if (config["general"]["predator_integration"]["enabled"] == True): # Check to see if Predator alerts are enabled.
        debug_message("Starting Predator")
        predator_path = config["general"]["predator_integration"]["instance_directory"]
        if (os.path.exists(predator_path) == True): # Check to see if an ADS-B message file has been set.
            start_command = ["python3",  predator_path + "/main.py", "2", "--headless", "2>/dev/null"] # This command is responsible for starting Predator.
            subprocess.Popen(start_command, stdout=subprocess.DEVNULL) # Execute the command to start Predator in the background.
        else:
            display_notice("Predator integration is enabled, but the configured instance directory does not exist. Predator could not be started.", 3)


def process_predator_alerts():
    debug_message("Processing Predator alerts")

    plate_log_file_path = config["general"]["predator_integration"]["plate_log_file"]

    if (os.path.exists(plate_log_file_path)): # Check to see if the plate log file exists.
        with open(plate_log_file_path) as plate_log_file: raw_plate_log_file_contents = plate_log_file.read() # Read the contents of the plate log file.

        if (is_json(raw_plate_log_file_contents)):
            raw_plate_history = json.loads(raw_plate_log_file_contents) # Load the plate log from the contents of the plate log file.
        else:
            raw_plate_history = {}

        pruned_plate_history = {} # This is a placeholder that will hold the recent entries in the plate history.
        for timestamp, entry in raw_plate_history.items(): # Iterate through each entry in the raw plate history.
            if (float(timestamp) > time.time() - config["general"]["predator_integration"]["latch_time"]): # Check to see if this entry in the plate log file is within the configured latch time.
                pruned_plate_history[timestamp] = entry # Add this entry to the pruned plate history.

        predator_alerts = {} # This is a placeholder that will hold the active alerts from the plate history.
        for timestamp in pruned_plate_history: # Iterate through each entry in the plate log.
            for plate in pruned_plate_history[timestamp]["plates"]: # Iterate through each plate in this entry.
                if (len(pruned_plate_history[timestamp]["plates"][plate]["alerts"]) > 0): # Check to see if this plate is associated with any alerts.
                    predator_alerts[plate] = {} # Initialize this plate in the Predator alerts.
                    for rule, rule_information in pruned_plate_history[timestamp]["plates"][plate]["alerts"].items(): # Iterate through each alert rule this plate is associated with.
                        predator_alerts[plate][rule] = rule_information # Add this alert rule and it's information to the Predator alert.
                
    else: # The plate log file does not exist.
        display_notice("Predator integration is enabled, but the configured plate log file does not exist.", 2)
        predator_alerts = {} # Set the dictionary of Predator alerts to a blank placeholder.
        

    return predator_alerts
