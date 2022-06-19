# Assassin

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Assassin...")


import os # Required to interact with certain operating system functions
import json # Required to process JSON data


assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory, containing all the program's support files.. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json



import time # Required to add delays and handle dates/times
import subprocess # Required for starting some shell commands
import signal # Required to manage sub-proceses.
import sys
import urllib.request # Required to make network requests
import re # Required to use Regex
import validators # Required to validate URLs
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings
import lzma # Required to open and manipulate ExCam database.
import math # Required to run more complex math functions.
from geopy.distance import great_circle # Required to calculate distance between locations.
import random # Required to generate random numbers.



import utils # Import the utils.py scripts.
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
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.






if (float(config["general"]["alert_range"]["traffic_cameras"]) > 0): # Check to see if traffic camera alerts are enabled.
    if (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == True): # Check to see that the traffic camera database exists at the path specified in the configuration.
        loaded_traffic_camera_database = load_traffic_cameras(get_gps_location()[0], get_gps_location()[1], config["general"]["alert_databases"]["traffic_cameras"], float(config["general"]["traffic_camera_loaded_radius"])) # Load all traffic cameras within the configured loading radius.
    else: # Traffic enforcement camera alerts are enabled, but the traffic enforcement camera database doesn't exist, so print a warning message.
        if (str(config["general"]["alert_databases"]["traffic_cameras"]) == ""): # The traffic enforcement camera alert database specified in the configuration is blank.
            display_notice("Traffic enforcement camera alerts are enabled in the configuration, but no traffic camera database was specified.", 2)
        elif (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == False): # The traffic camera alert database specified in the configuration does not exist.
            display_notice("Traffic enforcement camera alerts are enabled in the configuration, but the traffic camera database specified (" + str(config["general"]["alert_databases"]["traffic_cameras"]) + ") does not exist.", 2)
        else:
            display_notice("An unexpected error occurred while processing the traffic enforcement camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 2)




# Load the ALPR camera database, if enabled.
if (float(config["general"]["alert_range"]["alpr_cameras"]) > 0): # Check to see if ALPR camera alerts are enabled.
    if (str(config["general"]["alert_databases"]["alpr_cameras"]) != "" and os.path.exists(str(config["general"]["alert_databases"]["alpr_cameras"]))): # Check to see if the ALPR camera database exists.
        loaded_alpr_camera_database = json.load(open(str(config["general"]["alert_databases"]["alpr_cameras"]))) # Load the ALPR database.
    else:
        if (str(config["general"]["alert_databases"]["alpr_cameras"]) == ""): # The ALPR alert database specified in the configuration is blank.
            display_notice("ALPR camera alerts are enabled in the configuration, but no ALPR alert database was specified.", 2)
        elif (os.path.exists(str(config["general"]["alert_databases"]["alpr_cameras"])) == False): # The ALPR alert database specified in the configuration does not exist.
            display_notice("ALPR camera alerts are enabled in the configuration, but the ALPR database specified (" + str(config["general"]["alert_databases"]["alpr_cameras"]) + ") does not exist.", 2)
        else:
            display_notice("An unexpected error occurred while processing the ALPR camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 2)



# Load drone alert information, if enabled.
if (config["general"]["drone_alerts"]["enabled"] == True):
    if (os.path.exists(config["general"]["alert_databases"]["drones"]) == True and config["general"]["alert_databases"]["drones"] != ""):
        drone_threat_database = json.load(open(config["general"]["alert_databases"]["drones"]))
    elif (config["general"]["alert_databases"]["drones"] == ""):
        display_notice("Drone alerts are enabled in the configuration, but the drone alert database path is blank.", 2)
    elif (os.path.exists(config["general"]["alert_databases"]["drones"]) == False):
        display_notice("Drone alerts are enabled in the configuration, but the specified drone alert database (" + str(config["general"]["alert_databases"]["drones"]) + ") doesn't exist.", 2)


    if (config["general"]["drone_alerts"]["save_detected_hazards"] == True): # Check to see if drone hazard recording is enabled.
        if (os.path.exists(assassin_root_directory + "/drone_threat_history.json")):
            drone_threat_history_file = open(assassin_root_directory + "/drone_threat_history.json") # Open the drone threat history file.
            drone_threat_history = json.load(drone_threat_history_file) # Load the drone threat history from the file.
        else:
            drone_threat_history = [] # Set the drone threat history to a blank placeholder list.

    os.popen("rm -f " + assassin_root_directory + "/airodump_data*.csv") # Delete any previous airodump data.

    airodump_command = "sudo airodump-ng " + str(config["general"]["drone_alerts"]["monitoring_device"]) + " -w airodump_data --output-format csv --background 1 --write-interval 1" # Set up the command to start airodump.
    if (config["general"]["drone_alerts"]["monitoring_mode"] == "automatic"):
        proc = subprocess.Popen(airodump_command.split()) # Execute the command to start airodump.
        time.sleep(1) # Wait for 1 second to give airodump time to start.
    elif (config["general"]["drone_alerts"]["monitoring_mode"] == "manual"):
        print("Please manually execute the following command in the Assassin root directory:")
        print(style.italic + airodump_command + style.end)
        input("Press enter to continue once the command is running.")






# Display the start-up intro header.
clear() # Clear the screen.
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


time.sleep(2) # Wait two seconds to allow the start-up logo to remain on-screen for a moment.





play_sound("startup")





active_alarm = "none" # Set the active alert indicator variable to a placeholder before starting the main loop.
current_location = [] # Set the current location variable to a placeholder before starting the main loop.


while True: # Run forever in a loop until terminated.

    # Process all information that needs to be handled at the beginning of each cycle to prevent delays in the middle of the displaying process.

    if (config["general"]["gps_enabled"] == True): # If GPS is enabled, then get the current location at the beginning of the cycle.
        last_location = current_location # Set the last location to the current location immediately before we update the current location for the next cycle.
        current_location = get_gps_location() # Get the current location.



    # Traffic camera alert processing
    if (config["general"]["gps_enabled"] == True and float(config["general"]["alert_range"]["traffic_cameras"]) > 0): # Check to see if the speed camera display is enabled in the configuration.
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





    # ALPR camera alert processing
    if (os.path.exists(config["general"]["alert_databases"]["alpr_cameras"]) == True and config["general"]["alert_databases"]["alpr_cameras"] != "" and config["general"]["gps_enabled"] == True): # Check to see if a valid ALPR database has been configured.
        nearby_alpr_cameras = nearby_database_poi(current_location[0], current_location[1], loaded_alpr_camera_database, float(config["general"]["alert_range"]["alpr_cameras"])) # Get nearby entries from this POI database.
        nearest_alpr_camera = {"distance": 1000000000.0}

        for entry in nearby_alpr_cameras: # Iterate through all nearby ALPR cameras.
            if (entry["distance"] < nearest_alpr_camera["distance"]): # Check to see if the distance to this camera is lower than the current closest camera.
                nearest_alpr_camera = entry # Make the current camera the new closest camera.




    # Drone alert processing
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
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

        detected_drone_hazards = [] # This is a placeholder list of detected hazards that will be append to in the next step.
        for company in drone_threat_database: # Iterate through each manufacturer in the threat database.
            for mac in drone_threat_database[company]["MAC"]: # Iterate through each MAC address prefix for this manufacturer in the threat database.
                for device in detected_devices: # Iterate through each access point detected in the previous step.
                    if (''.join(c for c in device[0] if c.isalnum())[:6].lower() == mac.lower()): # Check to see if the first 6 characters of this AP matches the MAC address of this company.
                        device.append(company) # Add this device's associated company to this device's data.
                        device.append(round(time.time())) # Add the current time to this device's data.
                        detected_drone_hazards.append(device) # Add the current device to the list of hazards detected.








    clear() # Clear the console output at the beginning of every cycle.



    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.



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

    if (config["display"]["displays"]["speed"]["large_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the large speed display is enabled in the configuration.
        current_speed = convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
        current_speed = round(current_speed * 10**int(config["display"]["displays"]["speed"]["decimal_places"]))/10**int(config["display"]["displays"]["speed"]["decimal_places"]) # Round off the current speed to a certain number of decimal places as specific in the configuration.
        display_number(current_speed) # Display the current speed in a large ASCII font.

    if (config["display"]["displays"]["time"] == True): # Check to see the time display is enabled in the configuration.
        print("Time: " + str(time.strftime('%H:%M:%S'))) # Print the current time to the console.

    if (config["display"]["displays"]["date"]  == True): # Check to see the date display is enabled in the configuration.
        print("Date: " + str(time.strftime('%A, %B %d, %Y'))) # Print the current date to the console.

    if (config["display"]["displays"]["speed"]["small_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the small speed display is enabled in the configuration.
        current_speed = round(convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"])*10**int(config["display"]["displays"]["speed"]["decimal_places"]))/(10**int(config["display"]["displays"]["speed"]["decimal_places"])) # Convert the speed data from the GPS into the units specified by the configuration.
        print("Speed: " + str(current_speed) + " " + str(config["display"]["displays"]["speed"]["unit"])) # Print the current speed to the console.

    if (config["display"]["displays"]["location"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current location display is enabled in the configuration.
        print("Position: " + str(current_location[0]) + " " + str(current_location[1])) # Print the current location as coordinates to the console.

    if (config["display"]["displays"]["altitude"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
        print("Altitude: " + str(current_location[3]) + " meters") # Print the current altitude to the console.

    if ((config["display"]["displays"]["heading"]["degrees"] == True or config["display"]["displays"]["heading"]["direction"] == True) and config["general"]["gps_enabled"] == True): # Check to see if the current heading display is enabled in the configuration.
        if (config["display"]["displays"]["heading"]["direction"] == True and config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees are both enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4])) + " (" + str(current_location[4]) + ")") # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["direction"] == True): # Check to see if the configuration value to display the current heading in cardinal directions is enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4]))) # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in degrees is enabled.
            print("Heading: " + str(current_location[4])) # Print the current heading to the console in degrees.

    if (config["display"]["displays"]["satellites"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
        print("Satellites: " + str(current_location[5])) # Print the current altitude satellite count to the console.





    # Display traffic camera alerts.
    if (config["general"]["gps_enabled"] == True and float(config["general"]["alert_range"]["traffic_cameras"]) > 0 and "nearest_enforcement_camera" in locals()): # Check to see if the speed camera display is enabled in the configuration.
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

        if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
            update_status_lighting("alprcamera") # Run the function to update the status lighting.

        print(style.purple + style.bold)
        print("Nearest " + loaded_alpr_camera_database["name"] + ":")
        print("    Distance: " + str(round(nearest_alpr_camera["distance"]*1000)/1000) + " miles")
        print("    Street: " + str(nearest_alpr_camera["road"]))
        print(style.end + style.end)

        if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
            display_shape("horizontal") # Display an ASCII horizontal bar in the console output.

        play_sound("alpr")




    # Display drone alerts.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
        if (len(detected_drone_hazards) > 0): # Check to see if any hazards were detected this cycle.
            print(style.cyan + "Detected drone hazards:")
            for hazard in detected_drone_hazards: # Iterate through each detected hazard.
                if (len(hazard) == 17): # This hazards is an access point.
                    print("    " + hazard[0] + "") # Show this hazard's MAC address.
                    print("        Type: Access Point") # Show this hazard's type.
                    print("        Name: " + hazard[13]) # Show this hazard's name.
                    print("        Last Seen: " + str(hazard[2])) # Show the timestamp that this hazard was last seen.
                    print("        First Seen: " + str(hazard[1])) # Show the timestamp that this hazard was first seen.
                    print("        Channel: " + hazard[3]) # Show this hazard's wireless channel.
                    print("        Strength: " + str(100 + (int(hazard[8]))) + "%") # Show this hazards relative signal strength.
                    print("        Company: " + hazard[15]) # Show company or brand that this hazard is associated with.
                elif (len(hazard) == 9): # This hazard is a device. TODO
                    print("    " + hazard[0] + "") # Show this hazard's MAC address.
                    print("        Type: Device") # Show this hazard's type.
                    print("        Name: " + hazard[7]) # Show this hazard's name.
                    print("        Last Seen: " + str(hazard[2])) # Show the timestamp that this hazard was last seen.
                    print("        First Seen: " + str(hazard[1])) # Show the timestamp that this hazard was first seen.
                    print("        Channel: " + str(hazard[4])) # Show this hazard's wireless channel.
                    print("        Strength: " + str(100 + (int(hazard[3]))) + "%") # Show this hazards relative signal strength.
                    print("        Company: " + str(hazard[7])) # Show company or brand that this hazard is associated with.
                else:
                    print("    " + hazard[0] + "") # Show this hazard's MAC address.

                drone_threat_history.append(hazard) # Add this threat to the treat history.

            print(style.end) # End the font styling from the drone threat display.

            with open(assassin_root_directory + "/drone_threat_history.json", 'w') as drone_hazard_history_file: # Open the drone threat history file for editing.
                drone_hazard_history_file.write(str(json.dumps(drone_threat_history, indent = 4))) # Write the current drone threat history to the file.

            if (config["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                display_shape("cross") # Display an ASCII cross in the console output to represent a drone.

            play_sound("drone") # Play the sound effect associated with a potential drone threat being detected.




    # Record telemetry data according to the configuration.
    if (config["general"]["record_telemetry"] == True): # Check to see if Assassin is configured to record telemetry data.
        if (config["general"]["gps_enabled"] == True): # Check to see if GPS features are enabled.
            export_data = str(round(time.time())) + "," + str(current_speed) + "," + str(current_location[0]) + "," + str(current_location[1]) + "," + str(current_location[3]) + "," + str(current_location[4]) + "," + str(current_location[5]) + "\n" # Add all necessary information to the export data.
        else:
            export_data = str(round(time.time())) + "," + str("0") + "," + str("0.000") + "," + str("0.000") + "," + str("0") + "," + str("0") + "," + str("0") + "\n" # Add all necessary information to the export data, using placeholders for information that depends on GPS.

        add_to_file(assassin_root_directory + "/information_recording.csv", export_data, True) # Add the export data to the end of the file and write it to disk.




    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
