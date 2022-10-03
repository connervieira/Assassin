import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.
import datetime # Required to interpret human-readable dates and times.
import signal # Required to manage sub-proceses.

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
add_to_file = utils.add_to_file
save_to_file = utils.save_to_file
display_notice = utils.display_notice

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.



def load_drone_alerts():
    if (config["general"]["drone_alerts"]["enabled"] == True):
        debug_message("Loading drone detection system")
        # Load the drone database.
        if (os.path.exists(config["general"]["alert_databases"]["drones"]) == True and config["general"]["alert_databases"]["drones"] != ""):
            drone_threat_database = json.load(open(config["general"]["alert_databases"]["drones"]))
        elif (config["general"]["alert_databases"]["drones"] == ""):
            drone_threat_database = {} # Load a blank placeholder database since the actual database couldn't be loaded.
            display_notice("Drone alerts are enabled in the configuration, but the drone alert database path is blank.", 2)
        elif (os.path.exists(config["general"]["alert_databases"]["drones"]) == False):
            drone_threat_database = {} # Load a blank placeholder database since the actual database couldn't be loaded.
            display_notice("Drone alerts are enabled in the configuration, but the specified drone alert database (" + str(config["general"]["alert_databases"]["drones"]) + ") doesn't exist.", 2)


        # Load the drone threat history file, if applicable.
        if (config["general"]["drone_alerts"]["save_detected_hazards"] == True): # Check to see if drone hazard recording is enabled.
            if (os.path.exists(assassin_root_directory + "/drone_threat_history.json")):
                drone_threat_history_file = open(assassin_root_directory + "/drone_threat_history.json") # Open the drone threat history file.
                drone_threat_history = json.load(drone_threat_history_file) # Load the drone threat history from the file.
            else:
                drone_threat_history = [] # Set the drone threat history to a blank placeholder list.

        # Load the detected devices history file, if applicable.
        if (config["general"]["drone_alerts"]["save_detected_devices"] == True): # Check to see if device recording is enabled.
            if (os.path.exists(assassin_root_directory + "/radio_device_history.json")):
                radio_device_history_file = open(assassin_root_directory + "/radio_device_history.json") # Open the device history file.
                radio_device_history = json.load(radio_device_history_file) # Load the detected device history from the file.
            else:
                radio_device_history = {} # Set the drone threat history to a blank placeholder list.
        else: # Device recording is disabled.
            radio_device_history = {} # Set the drone threat history to a blank placeholder list.


        # Run Airodump based on the Assassin configuration.
        airodump_command = "sudo airodump-ng " + str(config["general"]["drone_alerts"]["monitoring_device"]) + " -w airodump_data --output-format csv --background 1 --write-interval 1" # Set up the command to start airodump.
        if (config["general"]["drone_alerts"]["monitoring_mode"] == "automatic"):
            os.popen("rm -f " + assassin_root_directory + "/airodump_data*.csv") # Delete any previous airodump data.
            proc = subprocess.Popen(airodump_command.split()) # Execute the command to start airodump.
            time.sleep(1) # Wait for 1 second to give airodump time to start.
        elif (config["general"]["drone_alerts"]["monitoring_mode"] == "manual"):
            print("Please manually execute the following command in the Assassin root directory:")
            print(style.italic + airodump_command + style.end)
            input("Press enter to continue once the command is running.")


        debug_message("Loaded drone detection system")
        return drone_threat_history, radio_device_history, drone_threat_database

    else: # Drone alerts are disabled in the configuration.
        return [], {}, {} # Return blank placeholder information.





def drone_alert_processing(radio_device_history, drone_threat_database, detected_drone_hazards):
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
        debug_message("Processing drone alerts")

        grab_output_command = "cat " + assassin_root_directory + "/airodump_data-01.csv" # Set up the command to grab the contents of airodump's CSV output file.
        command_output = str(os.popen(grab_output_command).read()) # Execute the output file grab command.

        line_split_output = command_output.split("\n") # Split the raw command output into a list, line by line.
        detected_devices = [] # Create a placeholder list for all of the detected devices and their data.
        for device in line_split_output: # Iterate through each detected device, and separate it's information into a sub-list.
            detected_devices.append(device.split(",")) # Add the information from each detected device to the access point list.

        # Remove invalid entries from the listed of detected devices.
        for device in detected_devices: # Iterate through each entry in the list of devices.
            if (len(device) <= 3): # Check to see if this entry is shorter than expected.
                detected_devices.remove(device) # Remove this entry from the list.

        for device in detected_devices: # Iterate through each entry in the list of devices.
            if (device[0] == "BSSID"): # Check to see if this entry is of the first header of the airodump output.
                detected_devices.remove(device) # Remove this entry from the list.
            elif (device[0] == "Station MAC"): # Check to see if this entry is of the second header of the airodump output.
                detected_devices.remove(device) # Remove this entry from the list.

        for device in detected_devices: # Iterate through each entry in the list of devices.
            if (len(device) <= 3): # Check to see if this entry is shorter than expected.
                detected_devices.remove(device) # Remove this entry from the list.

        for device_key, device in enumerate(detected_devices): # Iterate through each entry in the list of devices.
            for entry_key, entry in enumerate(device): # Iterate through each data entry for this device.
                detected_devices[device_key][entry_key] = entry.strip() # Remove leading whitespace before any data in this entry.


        active_radio_devices = {} # Set a placeholder dictionary to store the active radio devices. Information stored in this dictionary is volatile and are not saved to disk.

        for device in detected_devices: # Iterate through each device detected in the previous step.

            device_information = {} # Create a blank placeholder that will be used to store this device's information.

            if (len(device) == 15): # This hazard is an access point.
                device_information["mac"] = device[0] # Add the device's MAC address to the device information.
                device_information["name"] = device[13] # Add the device's name to the device information.
                device_information["lastseen"] = device[2] # Add the device's last-seen timestamp to the device information.
                device_information["firstseen"] = device[1] # Add the device's first-seen timestamp to the device information.
                device_information["channel"] = device[3] # Add the device's channel to the device information.
                device_information["packets"] = device[9] # Add the device's packet count to the device information.
                device_information["strength"] = str(100 + (int(device[8]))) # Convert the relative strength to a percentage, then save it to the device information.
                device_information["type"] = "Access Point" # Add the device's device type to the device information.
                device_information["threat"] = False # Add the device's threat status to the device information.
                device_information["company"] = "" # Add a placeholder for this device's associated company. This will be updated if the device is found to be a threat.
                device_information["threattype"] = "" # Add a placeholder for this device's threat type. This will be updated if the device is found to be a threat.
            elif (len(device) == 7): # This hazard is a device.
                device_information["mac"] = device[0] # Add the device's MAC address to the device information.
                device_information["name"] = device[6] # Add the device's name to the device information.
                device_information["lastseen"] = device[2] # Add the device's last-seen timestamp to the device information.
                device_information["firstseen"] = device[1] # Add the device's first-seen timestamp to the device information.
                device_information["channel"] = "Unknown" # Add the device's channel to the device information.
                device_information["packets"] = device[4] # Add the device's packet count to the device information.
                device_information["strength"] = str(100 + (int(device[3]))) # Convert the relative strength to a percentage, then save it to the device information.
                device_information["type"] = "Device" # Add the device's device type to the device information.
                device_information["threat"] = False # Add the device's threat status to the device information.
                device_information["company"] = "" # Add a placeholder for this device's associated company. This will be updated if the device is found to be a threat.
                device_information["threattype"] = "" # Add a placeholder for this device's threat type. This will be updated if the device is found to be a threat.
            else: # This hazard doesn't match the expected formatting rules.
                pass


            if (device_information != {}): # Check to see if the device_information has been populated by data.

                # Handle historical device recording.
                if (config["general"]["drone_alerts"]["save_detected_devices"] == True): # Check to see if device recording is enabled.
                    current_timestamp = str(round(time.time())) # Get the current timestamp. This value is saved to variable because it's theoretically possible for the time to change between the time the database entry is changed and the time information is added to it.
                    if (time.time() - time.mktime(datetime.datetime.strptime(device_information["lastseen"], "%Y-%m-%d %H:%M:%S").timetuple()) < float(3)): # Check to see if this threat was seen within the last 3 seconds. If not, ignore it and don't log it.

                        if (current_timestamp not in radio_device_history): # Check to see if the current timestamp already exists in the radio device history.
                            radio_device_history[current_timestamp] = [] # If this timestamp doesn't exist in the database, then create it with a blank placeholder dictionary.

                        radio_device_history[current_timestamp].append(device_information) # Add the current device to the list of detected radio devices.

                # Handle active device recording.
                active_radio_devices[device_information["mac"]] = device_information # Add this device to the device information




        if (config["general"]["drone_alerts"]["save_detected_devices"] == True): # Check to see if device recording is enabled.
            save_to_file(assassin_root_directory + "/" + "/radio_device_history.json", json.dumps(radio_device_history), True) # Save the radio device history to the log file.


        for company in drone_threat_database: # Iterate through each manufacturer in the threat database.
            for mac in drone_threat_database[company]["MAC"]: # Iterate through each MAC address prefix for this manufacturer in the threat database.
                for device in active_radio_devices: # Iterate through each active radio device.
                    device_information = active_radio_devices[device] # Get the information for the current device in the iteration.
                    if (''.join(c for c in device_information["mac"] if c.isalnum())[:6].lower() == mac.lower()): # Check to see if the first 6 characters of this device matches the MAC address of this company.
                        if (drone_threat_database[company]["type"] in config["general"]["drone_alerts"]["alert_types"]): # Check to see if the company associated with the device matches one of the device types in the list of device types Assassin is configured to alert to.
                            device_information["threat"] = True # Change this device's threat status to positive.
                            device_information["company"] = company # Add this device's associated company to this device's data.
                            device_information["threattype"] = drone_threat_database[company]["type"] # Add this device's type from the database to it's data.



        # Check to see which threats are still within the latch time, then add them to the active hazards list.
        for device in active_radio_devices: # Iterate through each active radio device.
            if (active_radio_devices[device]["threat"] == True):
                if (time.time() - time.mktime(datetime.datetime.strptime(active_radio_devices[device]["lastseen"], "%Y-%m-%d %H:%M:%S").timetuple()) < float(config["general"]["drone_alerts"]["hazard_latch_time"])): # Check to see if this threat was recently seen. If not, don't consider it an active threat.

                    # Check to see if this hazard already exists in the active drone hazards list.
                    for hazard in detected_drone_hazards: # Iterate through all active hazards.
                        if hazard["mac"] == active_radio_devices[device]["mac"]: # Check to see if the hazard already exists in the list of active hazards.
                            detected_drone_hazards.remove(hazard) # Remove the older hazard information.
                    detected_drone_hazards.append(active_radio_devices[device]) # Add the current device to the list of active hazards detected.


        # Iterate through all active hazards, and remove any that have expired.
        for hazard in detected_drone_hazards: # Iterate through each active hazard.
            if (time.time() - time.mktime(datetime.datetime.strptime(hazard["lastseen"], "%Y-%m-%d %H:%M:%S").timetuple()) > float(config["general"]["drone_alerts"]["hazard_latch_time"])): # Check to see if this threat was recently seen. If not, don't consider it an active threat.
                detected_drone_hazards.remove(hazard) # Remove the hazard from the active detected hazards database.


        return detected_drone_hazards
        debug_message("Processed drone alerts")
    else:
        return []
