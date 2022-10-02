# Assassin

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Assassin...")


import utils # Import the utils.py scripts.
debug_message = utils.debug_message # Load the function to print debugging information when the configuration says to do so.

debug_message("Starting loading")


import os # Required to interact with certain operating system functions
import json # Required to process JSON data


assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory, containing all the program's support files.. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json
debug_message("Loaded configuration")



import time # Required to add delays and handle dates/times
import subprocess # Required for starting some shell commands
import signal # Required to manage sub-proceses.
import sys
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings
import math # Required to run more complex math functions.
import random # Required to generate random numbers.

if (config["general"]["relay_alerts"]["enabled"] == True): # Only import the GPIO library if relay alerts are enabled.
    debug_message("Importing `GPIO` library")
    import RPi.GPIO as GPIO

if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only import the Bluetooth library if Bluetooth monitoring is enabled.
    debug_message("Importing `bluetooth` library")
    import bluetooth


# Load the rest of the utility functions from utils.py
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
get_distance = utils.get_distance # Load the function to get the distance between to global positions.
load_traffic_cameras = utils.load_traffic_cameras # Load the function used to load the database of speed and red-light cameras.
nearby_traffic_cameras = utils.nearby_traffic_cameras # Load the function used to check for nearby traffic cameras.
calculate_bearing = utils.calculate_bearing # Load the function used to calculate the bearing between two coordinate pairs.
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
get_arrow_direction = utils.get_arrow_direction # Load the function used to convert headings from degrees to arrow directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.
fetch_aircraft_data = utils.fetch_aircraft_data # Load the function used to fetch aircraft data from a Dump1090 CSV file.
debug_message("Imported `utils.py`")








# Load the traffic enforcement camera, if enabled.
if (float(config["general"]["alert_range"]["traffic_cameras"]) > 0 and config["general"]["gps_enabled"]): # Check to see if traffic camera alerts are enabled, and the GPS is enabled.
    debug_message("Loading traffic enforcement camera database")
    current_location = [0, 0] # Set the "current location" to a placeholder.
    while (current_location[0] == 0 and current_location[1] == 0): # Repeatedly attempt to get a GPS location until one is received.
        current_location = get_gps_location() # Attempt to get the current GPS location.
        time.sleep(2) # Wait 2 seconds to give the GPS time to get a lock.

    if (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == True): # Check to see that the traffic camera database exists at the path specified in the configuration.
        loaded_traffic_camera_database = load_traffic_cameras(get_gps_location()[0], get_gps_location()[1], config["general"]["alert_databases"]["traffic_cameras"], float(config["general"]["traffic_camera_loaded_radius"])) # Load all traffic cameras within the configured loading radius.
    else: # Traffic enforcement camera alerts are enabled, but the traffic enforcement camera database doesn't exist, so print a warning message.
        if (str(config["general"]["alert_databases"]["traffic_cameras"]) == ""): # The traffic enforcement camera alert database specified in the configuration is blank.
            display_notice("Traffic enforcement camera alerts are enabled in the configuration, but no traffic camera database was specified.", 2)
        elif (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == False): # The traffic camera alert database specified in the configuration does not exist.
            display_notice("Traffic enforcement camera alerts are enabled in the configuration, but the traffic camera database specified (" + str(config["general"]["alert_databases"]["traffic_cameras"]) + ") does not exist.", 2)
        else:
            display_notice("An unexpected error occurred while processing the traffic enforcement camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 2)
    debug_message("Loaded traffic enforcement camera database")




# Load the ALPR camera database, if enabled.
if (float(config["general"]["alert_range"]["alpr_cameras"]) > 0): # Check to see if ALPR camera alerts are enabled.
    debug_message("Loading ALPR camera database")
    if (str(config["general"]["alert_databases"]["alpr_cameras"]) != "" and os.path.exists(str(config["general"]["alert_databases"]["alpr_cameras"]))): # Check to see if the ALPR camera database exists.
        loaded_alpr_camera_database = json.load(open(str(config["general"]["alert_databases"]["alpr_cameras"]))) # Load the ALPR database.
    else:
        if (str(config["general"]["alert_databases"]["alpr_cameras"]) == ""): # The ALPR alert database specified in the configuration is blank.
            display_notice("ALPR camera alerts are enabled in the configuration, but no ALPR alert database was specified.", 2)
        elif (os.path.exists(str(config["general"]["alert_databases"]["alpr_cameras"])) == False): # The ALPR alert database specified in the configuration does not exist.
            display_notice("ALPR camera alerts are enabled in the configuration, but the ALPR database specified (" + str(config["general"]["alert_databases"]["alpr_cameras"]) + ") does not exist.", 2)
        else:
            display_notice("An unexpected error occurred while processing the ALPR camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 2)
    debug_message("Loaded ALPR camera database")



# Load drone alert information, if enabled.
if (config["general"]["drone_alerts"]["enabled"] == True):
    debug_message("Loading drone detection system")
    # Load the drone database.
    if (os.path.exists(config["general"]["alert_databases"]["drones"]) == True and config["general"]["alert_databases"]["drones"] != ""):
        drone_threat_database = json.load(open(config["general"]["alert_databases"]["drones"]))
    elif (config["general"]["alert_databases"]["drones"] == ""):
        display_notice("Drone alerts are enabled in the configuration, but the drone alert database path is blank.", 2)
    elif (os.path.exists(config["general"]["alert_databases"]["drones"]) == False):
        display_notice("Drone alerts are enabled in the configuration, but the specified drone alert database (" + str(config["general"]["alert_databases"]["drones"]) + ") doesn't exist.", 2)


    detected_drone_hazards = [] # Set the active drone hazards list to a blank placeholder.

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





# Load the Bluetooth device log file, if applicable.
if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["bluetooth_monitoring"]["log_devices"]["enabled"] == True): # Check to see if Bluetooth device logging is enabled.
    debug_message("Loading Bluetooth log file")
    if (os.path.exists(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"])):
        detected_bluetooth_devices = json.load(open(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"])) # Load the data from the Bluetooth device log file.
    else:
        detected_bluetooth_devices = {} # Set the Bluetooth device log to a blank placeholder list.

    debug_message("Loaded Bluetooth log file")






# Display the start-up intro header.
clear() # Clear the screen.
debug_message("Completed loading")
if (config["display"]["ascii_art_header"] == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
    print(style.red + style.bold)
    print("    _   ___ ___   _   ___ ___ ___ _  _ ")
    print("   /_\ / __/ __| /_\ / __/ __|_ _| \| |")
    print("  / _ \\\\__ \__ \/ _ \\\\__ \__ \| || .` |")
    print(" /_/ \_\___/___/_/ \_\___/___/___|_|\_|")
    print(style.end)

else: # If the user his disabled the large ASCII art header, then show a simple title header with minimal styling.
    print(style.red + style.bold + "ASSASSIN" + style.end)


if (config["display"]["custom_startup_message"] != ""): # Only display the line for the custom message if the user has defined one.
    print(config["display"]["custom_startup_message"]) # Show the user's custom defined start-up message.


time.sleep(1) # Wait two seconds to allow the start-up logo to remain on-screen for a moment.





play_sound("startup")





active_alarm = "none" # Set the active alert indicator variable to a placeholder before starting the main loop.
current_location = [] # Set the current location variable to a placeholder before starting the main loop.


debug_message("Starting main loop")

while True: # Run forever in a loop until terminated.
    debug_message("Cycle started")
    if (config["general"]["active_config_refresh"] == True): # Check to see if the configuration indicates to actively refresh the configuration during runtime.
        config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json
        debug_message("Reloaded configuration")




    # Process all information that needs to be handled at the beginning of each cycle to prevent delays in the middle of the displaying process.

    if (config["general"]["gps_enabled"] == True): # If GPS is enabled, then get the current location at the beginning of the cycle.
        debug_message("Grabbing GPS information")
        last_location = current_location # Set the last location to the current location immediately before we update the current location for the next cycle.
        current_location = get_gps_location() # Get the current location.
        current_speed = round(convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"])*10**int(config["display"]["displays"]["speed"]["decimal_places"]))/(10**int(config["display"]["displays"]["speed"]["decimal_places"])) # Convert the speed data from the GPS into the units specified by the configuration.
        debug_message("Grabbed GPS information")



    # Run traffic enforcement camera alert processing
    if (config["general"]["gps_enabled"] == True and float(config["general"]["alert_range"]["traffic_cameras"]) > 0): # Check to see if the speed camera display is enabled in the configuration.
        debug_message("Processing traffic enforcement camera alerts")
        # Create placeholders for each camera type so we can add the closet camera for each category in the next step .
        nearest_speed_camera, nearest_redlight_camera, nearest_misc_camera, nearest_traffic_camera = {"dst": 10000000.0}, {"dst": 10000000.0}, {"dst": 10000000.0}, {"dst": 10000000.0}

        nearby_speed_cameras, nearby_redlight_cameras, nearby_misc_cameras = nearby_traffic_cameras(current_location[0], current_location[1], loaded_traffic_camera_database, float(config["general"]["alert_range"]["traffic_cameras"])) # Get all traffic cameras within the configured radius.

        if (config["general"]["camera_alert_types"]["speed"] == True): # Only process alerts for speed cameras if enabled in the configuration.
            for camera in nearby_speed_cameras: # Iterate through all nearby speed cameras.
                if (camera["dst"] < nearest_speed_camera["dst"]): # Check to see if the distance to this camera is lower than the current closest camera.
                    nearest_speed_camera = camera # Make the current camera the new closest camera.
        if (config["general"]["camera_alert_types"]["redlight"] == True): # Only process alerts for red light cameras if enabled in the configuration.
            for camera in nearby_redlight_cameras: # Iterate through all nearby redlight cameras.
                if (camera["dst"] < nearest_redlight_camera["dst"]): # Check to see if the distance to this camera is lower than the current closest camera.
                    nearest_redlight_camera = camera # Make the current camera the new closest camera.
        if (config["general"]["camera_alert_types"]["misc"] == True): # Only process alerts for general traffic cameras if enabled in the configuration.
            for camera in nearby_misc_cameras: # Iterate through all nearby miscellaneous cameras.
                if (camera["dst"] < nearest_misc_camera["dst"]): # Check to see if the distance to this camera is lower than the current closest camera.
                    nearest_misc_camera = camera # Make the current camera the new closest camera.


        if (nearest_speed_camera["dst"] < nearest_redlight_camera["dst"] and nearest_speed_camera["dst"] < nearest_misc_camera["dst"]): # Check to see if the nearest speed camera is closer than nearest of the other camera types
            nearest_enforcement_camera = nearest_speed_camera # Set the overall nearest camera to the nearest speed camera.
        elif (nearest_redlight_camera["dst"] < nearest_speed_camera["dst"] and nearest_redlight_camera["dst"] < nearest_misc_camera["dst"]): # Check to see if the nearest red-light camera is closer than nearest of the other camera types
            nearest_enforcement_camera = nearest_redlight_camera # Set the overall nearest camera to the nearest red-light camera.
        elif (nearest_misc_camera["dst"] < nearest_speed_camera["dst"] and nearest_misc_camera["dst"] < nearest_redlight_camera["dst"]): # Check to see if the nearest miscellaneous camera is closer than nearest of the other camera types
            nearest_enforcement_camera = nearest_redlight_camera # Set the overall nearest camera to the nearest miscellaneous camera.

        if (config["general"]["traffic_camera_speed_check"] == True and "nearest_enforcement_camera" in locals()): # Check to see if the traffic camera speed check setting is enabled in the configuration, and that a speed camera is actually within the alert radius at all.
            if (nearest_enforcement_camera["spd"] != None): # Check to see if the nearest speed camera has speed limit data associated with it.
                if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then enable a heightend alert.
                    active_alarm = "speedcameralimitexceeded" # Set an active alarm indicating that the speed camera speed limit has been exceeded.

        debug_message("Processed traffic enforcement camera alerts")





    # Run ALPR camera alert processing
    if (os.path.exists(config["general"]["alert_databases"]["alpr_cameras"]) == True and config["general"]["alert_databases"]["alpr_cameras"] != "" and config["general"]["gps_enabled"] == True): # Check to see if a valid ALPR database has been configured.
        debug_message("Processing ALPR camera alerts")
        nearby_alpr_cameras = nearby_database_poi(current_location[0], current_location[1], loaded_alpr_camera_database, float(config["general"]["alert_range"]["alpr_cameras"])) # Get nearby entries from this POI database.
        nearest_alpr_camera = {"distance": 1000000000.0}

        for entry in nearby_alpr_cameras: # Iterate through all nearby ALPR cameras.
            if (entry["distance"] < nearest_alpr_camera["distance"]): # Check to see if the distance to this camera is lower than the current closest camera.
                nearest_alpr_camera = entry # Make the current camera the new closest camera.

        debug_message("Processed ALPR camera alerts")




    # Run drone alert processing
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


        active_radio_devices = {} # Set a placeholder dictionary to store the active radio devices. Information stored in this dictionary is voltile and are not saved to disk.

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


        debug_message("Processed drone alerts")





    # Run relay-based alert processing.
    if (config["general"]["relay_alerts"]["enabled"] == True): # Only check for relay-based alerts if relay alerts are enabled in the configuration.
        debug_message("Processing relay alerts")
        active_relay_alerts = [] # Set the active relay alerts to a blank placeholder so all of the active alerts this cycle can be added to it in the next step.
        for alert in config["general"]["relay_alerts"]["alerts"]:
            if (GPIO.input(config["general"]["relay_alerts"]["alerts"][alert]["gpio_pin"]) == config["general"]["relay_alerts"]["alerts"][alert]["alert_on_closed"]):
                if (config["general"]["gps_enabled"] == True):
                    if (float(current_speed) >= config["general"]["relay_alerts"]["alerts"][alert]["minimum_speed"] and float(current_speed) <= config["general"]["relay_alerts"]["alerts"][alert]["maximum_speed"]): # Check to see if the current speed falls within the range specified for this alert.
                        active_relay_alerts.append(config["general"]["relay_alerts"]["alerts"][alert]) # Add this alert to the list of active alerts for this cycle.
                else: # GPS features are disabled, so show the alert regardless of the current speed.
                    active_relay_alerts.append(config["general"]["relay_alerts"]["alerts"][alert]) # Add this alert to the list of active alerts for this cycle.

        debug_message("Processed relay alerts")




    # Run Bluetooth alert processing.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only conduct Bluetooth alert processing if bluetooth alerts and GPS features are enabled in the configuration.
        debug_message("Processing Bluetooth alerts")
        try:
            nearby_bluetooth_devices = bluetooth.discover_devices(int(config["general"]["bluetooth_monitoring"]["scan_time"]), lookup_names = True) # Scan for nearby Bluetooth devices for the amount of time specified in the configuration.
        except:
            display_notice("Couldn't detect nearby Bluetooth devices.", 2) # Display a warning that Bluetooth devices could not be detected.
            nearby_bluetooth_devices = {}  # Set the nearby Bluetooth device list to an empty placeholder, since Bluetooth devices could not be detected.

        for address, name in nearby_bluetooth_devices:
            if (address in detected_bluetooth_devices): # This device has been seen before, so update it's existing dictionary entry.
                detected_bluetooth_devices[address]["lastseenlocation"] = current_location
                detected_bluetooth_devices[address]["lastseentime"] = round(time.time())
            else: # This device has not been seen before, so add it to the dictionary.
                detected_bluetooth_devices[address] = {
                    "name": str(name),
                    "firstseenlocation": current_location, # This is the first GPS location that this device was detected at. This will not be updated upon subsequent detections.
                    "lastseenlocation": current_location, # This is the most recent GPS location that this device was detected at. This will be updated upon subsequent detections.
                    "firstseentime": round(time.time()), # This is the first time that this device was detected at. This will not be updated upon subsequent detections.
                    "lastseentime": round(time.time()), # This is the most recent time that this device was detected at. This will be updated upon subsequent detections.
                    "whitelist": address in config["general"]["bluetooth_monitoring"]["whitelist"]["devices"], # Check to see if this device address is in the whitelist specified in the configuration.
                    "blacklist": address in config["general"]["bluetooth_monitoring"]["blacklist"]["devices"] # Check to see if this device address is in the blacklist specified in the configuration.
                }

            if (config["general"]["bluetooth_monitoring"]["log_devices"]["enabled"] == True): # Check to see if Bluetooth device logging is enabled.
                save_to_file(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"], json.dumps(detected_bluetooth_devices), True) # Save the Bluetooth device history to disk.

        debug_message("Processed Bluetooth alerts")







    # Run aircraft ADS-B alert processing.
    if (config["general"]["adsb_alerts"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Processing ADS-B alerts")
        aircraft_data = fetch_aircraft_data("/home/pi/Downloads/ADSB-Data.csv") # Fetch the most recent aircraft data. TODO - Replace with live data stream.
        aircraft_threats = [] # Set the list of active aircraft threats to an empty placeholder database.

        for key in aircraft_data.keys(): # Iterate through all detected aircraft
            aircraft_location = [aircraft_data[key]["latitude"], aircraft_data[key]["longitude"], aircraft_data[key]["altitude"]] # Grab the location information for the aircraft.

            if (aircraft_location[0] != "" and aircraft_location[1] != ""): # Check to make sure this aircraft has location information. Otherwise, skip it.
                # Calculate the distance to the aircraft.
                aircraft_distance = get_distance(current_location[0], current_location[1], aircraft_location[0], aircraft_location[1]) # Calculate the distance to the aircraft.
                aircraft_data[key]["distance"] = aircraft_distance # Add the distance to the aircraft to its data.

                # Calculate the heading of the aircraft relative to the current direction of motion.
                relative_heading = int(aircraft_data[key]["heading"]) - current_location[4] # Calculate the heading direction of this aircraft relative to the current direction of movement
                if (relative_heading < 0): # Check to see if the relative heading is a negative number.
                    relative_heading = 360 + relative_heading # Convert the relative heading to a positive number.
                aircraft_data[key]["relativeheading"] = relative_heading # Add the relative heading of the aircraft to its data.

                # Calculate the direction to the aircraft relative to the current position.
                relative_direction = calculate_bearing(current_location[0], current_location[1], aircraft_data[key]["latitude"], aircraft_data[key]["longitude"])
                if (relative_direction < 0): # Check to see if the direction to the aircraft is negative.
                    relative_direction = 360 + relative_direction
                aircraft_data[key]["direction"] = relative_direction # Add the direction to the aircraft to its data.

                precise_alert_threshold = (int(aircraft_location[2]) / config["general"]["adsb_alerts"]["base_altitude_threshold"]) * config["general"]["adsb_alerts"]["distance_threshold"] # Calculate the precise alerting distance based on the aircraft altitude, base altitude threshold, and alert distance configured by the user. Higher altitude will cause planes to alert from farther away.

                if (aircraft_distance < precise_alert_threshold):
                    aircraft_threats.append(aircraft_data[key]) # Add this aircraft to the list of active threats.

        debug_message("Processed ADS-B alerts")




    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.








    debug_message("Alert processing completed")
    clear() # Clear the console output at the beginning of every cycle.






    # Display any critical alarm messages that the user should know about as soon as possible.
    if (active_alarm == "speedcameralimitexceeded"):
        if (config["display"]["large_critical_display"] == True):
            print(style.red + style.bold)
            print(" $$$$$$\\  $$\\       $$$$$$\\  $$\\      $$\\       $$$$$$$\\   $$$$$$\\  $$\\      $$\\ $$\\   $$\\ ")
            print("$$  __$$\\ $$ |     $$  __$$\\ $$ | $\\  $$ |      $$  __$$\\ $$  __$$\\ $$ | $\\  $$ |$$$\\  $$ |")
            print("$$ /  \\__|$$ |     $$ /  $$ |$$ |$$$\\ $$ |      $$ |  $$ |$$ /  $$ |$$ |$$$\\ $$ |$$$$\\ $$ |")
            print("\\$$$$$$\\  $$ |     $$ |  $$ |$$ $$ $$\\$$ |      $$ |  $$ |$$ |  $$ |$$ $$ $$\\$$ |$$ $$\\$$ |")
            print(" \\____$$\\ $$ |     $$ |  $$ |$$$$  _$$$$ |      $$ |  $$ |$$ |  $$ |$$$$  _$$$$ |$$ \\$$$$ |")
            print("$$\\   $$ |$$ |     $$ |  $$ |$$$  / \\$$$ |      $$ |  $$ |$$ |  $$ |$$$  / \\$$$ |$$ |\\$$$ |")
            print("\\$$$$$$  |$$$$$$$$\ $$$$$$  |$$  /   \\$$ |      $$$$$$$  | $$$$$$  |$$  /   \\$$ |$$ | \$$ |")
            print(" \\______/ \________|\\______/ \\__/     \\__|      \\_______/  \\______/ \\__/     \\__|\\__|  \\__|")
            print(style.red + "SPEED CAMERA LIMIT EXCEEDED" + style.end)
            print(style.end)
        else:
            print(style.red + style.bold + "SLOW DOWN" + style.end)
            print(style.red + "SPEED CAMERA LIMIT EXCEEDED" + style.end)




    active_alarm = "none" # Reset the active alert to none at the beginning of each session.






    # Show all configured basic information displays.

    debug_message("Displaying basic dashboard")

    if (config["display"]["displays"]["speed"]["large_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the large speed display is enabled in the configuration.
        current_speed = convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
        current_speed = round(current_speed * 10**int(config["display"]["displays"]["speed"]["decimal_places"]))/10**int(config["display"]["displays"]["speed"]["decimal_places"]) # Round off the current speed to a certain number of decimal places as specific in the configuration.
        display_number(current_speed) # Display the current speed in a large ASCII font.

    if (config["display"]["displays"]["time"] == True): # Check to see the time display is enabled in the configuration.
        print("Time: " + str(time.strftime('%H:%M:%S'))) # Print the current time to the console.

    if (config["display"]["displays"]["date"]  == True): # Check to see the date display is enabled in the configuration.
        print("Date: " + str(time.strftime('%A, %B %d, %Y'))) # Print the current date to the console.

    if (config["display"]["displays"]["speed"]["small_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the small speed display is enabled in the configuration.
        print("Speed: " + str(current_speed) + " " + str(config["display"]["displays"]["speed"]["unit"])) # Print the current speed to the console.

    if (config["display"]["displays"]["location"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current location display is enabled in the configuration.
        print("Position: " + str(current_location[0]) + " " + str(current_location[1])) # Print the current location as coordinates to the console.

    if (config["display"]["displays"]["altitude"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
        print("Altitude: " + str(current_location[3]) + " meters") # Print the current altitude to the console.

    if ((config["display"]["displays"]["heading"]["degrees"] == True or config["display"]["displays"]["heading"]["direction"] == True) and config["general"]["gps_enabled"] == True): # Check to see if the current heading display is enabled in the configuration.
        if (config["display"]["displays"]["heading"]["direction"] == True and config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees are both enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4])) + " (" + str(current_location[4]) + "°)") # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["direction"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees is enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4]))) # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in degrees is enabled.
            print("Heading: " + str(current_location[4]) + "°") # Print the current heading to the console in degrees.

    if (config["display"]["displays"]["satellites"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
        print("Satellites: " + str(current_location[5])) # Print the current altitude satellite count to the console.




    # Display relay-based alerts.
    if (config["general"]["relay_alerts"]["enabled"] == True): # Only display relay-based alerts if relay alerts are enabled in the configuration.
        debug_message("Displaying relay alerts")
        for alert in active_relay_alerts: # Iterate through each active alert, and print it to the screen.
            print(style.green + alert["title"])
            print("    " + alert["message"] + style.end)




    # Display Bluetooth monitoring alerts.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only conduct Bluetooth alert processing if bluetooth alerts and GPS features are enabled in the configuration.
        debug_message("Displaying Bluetooth alerts")
        active_bluetooth_alert = False # Reset the alert status to false. This will be changed to true if an active alert is found.
        for address in detected_bluetooth_devices:
            device = detected_bluetooth_devices[address] # Grab the data for the device of this iteration cycle.
            distance_followed = get_distance(device["firstseenlocation"][0], device["firstseenlocation"][1], device["lastseenlocation"][0], device["lastseenlocation"][1]) # Calculate the distance that this device has been following Assassin by determining the distance between the first detected location and the last detected location.
            if ((distance_followed >= float(config["general"]["bluetooth_monitoring"]["minimum_following_distance"]) and address not in config["general"]["bluetooth_monitoring"]["whitelist"]["devices"]) or address in config["general"]["bluetooth_monitoring"]["blacklist"]["devices"]): # Check to see if the distance this device has followed Assassin is greater than or equal to the threshold set in the configuration for alerting. Also check to make sure this device is not in the whitelist. If this device is in the blacklist, the alert regardless of other conditions.
                active_bluetooth_alert = True # Change the current alert status to 'active'.
                print(style.pink + address + " (" + device["name"] + ") has been following for " + str(distance_followed) + " miles over the past " + str(int(device["lastseentime"]) - int(device["firstseentime"])) + " seconds." + style.end) # Print a notice containing the device that is following, as well has how far and how long the device has been detected.

        if (active_bluetooth_alert == True): # If an active alert was determined this round, then run relevant alerts.
            if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                display_shape("square") # Display an ASCII square in the console output to represent a device.

            play_sound("bluetooth") # Play the alert sound associated with Bluetooth alerts, if one is configured to run.
            



    # Display traffic camera alerts.
    if (config["general"]["gps_enabled"] == True and float(config["general"]["alert_range"]["traffic_cameras"]) > 0 and "nearest_enforcement_camera" in locals()): # Check to see if the speed camera display is enabled in the configuration.
        debug_message("Displaying traffic enforcement camera alerts")
        # Display the nearest traffic camera, if applicable.
        if (nearest_enforcement_camera["dst"] < float(config["general"]["alert_range"]["traffic_cameras"])): # Only display the nearest camera if it's within the maximum range specified in the configuration.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("enforcementcamera") # Run the function to update the status lighting.


            print(style.blue + style.bold)
            print("Nearest Enforcement Camera:")
            if (nearest_enforcement_camera == nearest_speed_camera): # Check to see if the overall nearest camera is the nearest speed camera.
                print("    Type: Speed Camera")
            elif (nearest_enforcement_camera == nearest_redlight_camera): # Check to see if the overall nearest camera is the nearest red light camera.
                print("    Type: Red Light Camera")
            elif (nearest_enforcement_camera == nearest_misc_camera): # Check to see if the overall nearest camera is the nearest general traffic camera.
                print("    Type: General Traffic Camera")
            else:
                print("    Type: Unknown")
            print("    Distance: " + str(round(nearest_enforcement_camera["dst"]*1000)/1000) + " miles") # Display the current distance to the traffic camera.
            if (nearest_enforcement_camera["str"] != None): # Check to see if street data exists for this camera.
                print("    Street: " + str(nearest_enforcement_camera["str"])) # Display the street that the traffic camera is on.
            if (nearest_enforcement_camera["spd"] != None): # Check to see if speed limit data exists for this camera.
                print("    Speed: " + str(nearest_enforcement_camera["spd"])) # Display the speed limit of the traffic camera.
            print(style.end + style.end)


            if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                display_shape("circle") # Display an ASCII circle in the console output.

            # Play audio alerts, as necessary.
            if (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.1)): # Check to see if the nearest camera is within 10% of the traffic camera alert radius.
                if (nearest_enforcement_camera["spd"] != None and config["general"]["traffic_camera_speed_check"] == True): # Check to see if speed limit data exists for this speed camera, and if the traffic camera speed check setting is enabled in the configuration.
                    if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then play a heightened alarm sound.
                        play_sound("alarm")

                play_sound("camera3")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.25)): # Check to see if the nearest camera is within 25% of the traffic camera alert radius.
                play_sound("camera2")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]))): # Check to see if the nearest camera is within the traffic camera alert radius.
                play_sound("camera1")




    # Display ALPR camera alerts.
    if (len(nearby_alpr_cameras) > 0): # Only iterate through the nearby cameras if there are any nearby cameras to begin with.
        debug_message("Displaying ALPR camera alerts")

        if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
            update_status_lighting("alprcamera") # Run the function to update the status lighting.

        print(style.purple + style.bold)
        print("Nearest " + loaded_alpr_camera_database["name"] + ":")
        print("    Distance: " + str(round(nearest_alpr_camera["distance"]*1000)/1000) + " miles") # Display the distance to this POI.
        print("    Street: " + str(nearest_alpr_camera["road"])) # Display the road that this POI is associated with.
        print("    Direction: " + str(get_arrow_direction(nearest_alpr_camera["bearing"] - current_location[4])) + " " + str(round(nearest_alpr_camera["bearing"] - current_location[4])) + "°") # Display the direct to this POI relative to the current direction of movement.
        print("    Bearing: " + str(get_cardinal_direction(nearest_alpr_camera["bearing"])) + " " + str(round(nearest_alpr_camera["bearing"])) + "°") # Display the absolute bearing to this POI.
        print(style.end + style.end)

        if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
            display_shape("horizontal") # Display an ASCII horizontal bar in the console output.

        play_sound("alpr")




    # Display drone alerts.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
        debug_message("Displaying drone alerts")
        if (len(detected_drone_hazards) > 0): # Check to see if any hazards were detected this cycle.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("autonomousthreat") # Update the status lighting to indicate that at least one autonomous threat was detected.

            print(style.cyan + "Detected autonomous hazards:")
            for hazard in detected_drone_hazards: # Iterate through each detected hazard.
                print("    " + hazard["mac"] + "") # Show this hazard's MAC address.
                print("        Threat Type: " + hazard["threattype"]) # Show what kind of threat this device is.
                print("        Company: " + hazard["company"]) # Show company or brand that this hazard is associated with.
                print("        Name: " + hazard["name"]) # Show this hazard's name.
                print("        Last Seen: " + str(hazard["lastseen"])) # Show the timestamp that this hazard was last seen.
                print("        First Seen: " + str(hazard["firstseen"])) # Show the timestamp that this hazard was first seen.
                print("        Channel: " + hazard["channel"]) # Show this hazard's wireless channel.
                print("        Channel: " + hazard["packets"]) # Show this hazard's packet count.
                print("        Strength: " + str(hazard["strength"]) + "%") # Show this hazards relative signal strength.
                print("        Wireless Type: " + hazard["type"]) # Show this hazard's type.

                drone_threat_history.append(hazard) # Add this threat to the threat history.

            print(style.end) # End the font styling from the drone threat display.

            save_to_file(assassin_root_directory + "/drone_threat_history.json", str(json.dumps(drone_threat_history, indent = 4)), True) # Save the current drone threat history to disk.

            if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                display_shape("cross") # Display an ASCII cross in the console output to represent a drone.

            play_sound("drone") # Play the sound effect associated with a potential drone threat being detected.




    # Display ADS-B aircraft alerts
    if (config["general"]["adsb_alerts"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Displaying ADS-B alerts")
        if (len(aircraft_threats) > 0): # Check to see if any threats were detected this cycle.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("adsbthreat") # Update the status lighting to indicate that at least one ADS-B aircraft threat was detected.

            print(style.yellow + "Detected aircraft ADS-B threats:")
            for threat in aircraft_threats: # Iterate through each detected hazard.
                print("    " + threat["id"] + ":") # Show this hazard's MAC address.
                print("        Location: " + str(threat["latitude"]) + ", " + str(threat["longitude"]) + " (" + get_arrow_direction(threat["direction"]) + " " + str(round(threat["direction"])) + ")") # Show the coordinates of this aircraft.
                print("        Distance: " + str(round(threat["distance"]*1000)/1000) + " miles") # Show the distance to this aircraft.
                print("        Speed: " + str(threat["speed"]) + " knots") # Show the speed of this aircraft.
                print("        Absolute Heading: " + get_cardinal_direction(threat["heading"]) + " (" + str(threat["heading"]) + "°)") # Show the absolute heading of this aircraft.
                print("        Relative Heading: " + get_arrow_direction(threat["relativeheading"]) + " (" + str(threat["relativeheading"]) + "°)") # Show the direction of this aircraft relative to the current direction of movement.

            print(style.end) # End the font styling from the aircraft ADS-B threat display.

            if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                display_shape("triangle") # Display an ASCII triangle in the console output to represent a plane.

            play_sound("adsb") # Play the sound effect associated with a potential ADS-B aircraft threat being detected.








    # Record telemetry data according to the configuration.
    if (config["general"]["record_telemetry"] == True): # Check to see if Assassin is configured to record telemetry data.
        debug_message("Recording telemetry data")
        if (config["general"]["gps_enabled"] == True): # Check to see if GPS features are enabled.
            export_data = str(round(time.time())) + "," + str(current_speed) + "," + str(current_location[0]) + "," + str(current_location[1]) + "," + str(current_location[3]) + "," + str(current_location[4]) + "," + str(current_location[5]) + "\n" # Add all necessary information to the export data.
        else:
            export_data = str(round(time.time())) + "," + str("0") + "," + str("0.000") + "," + str("0.000") + "," + str("0") + "," + str("0") + "," + str("0") + "\n" # Add all necessary information to the export data, using placeholders for information that depends on GPS.

        add_to_file(assassin_root_directory + "/information_recording.csv", export_data, True) # Add the export data to the end of the file and write it to disk.
        debug_message("Telemetry recorded")




    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
