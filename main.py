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
import sys
import urllib.request # Required to make network requests
import re # Required to use Regex
import validators # Required to validate URLs
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings
import psutil # Required to get disk usage information
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




if (float(config["general"]["alert_range"]["traffic_cameras"]) > 0): # Check to see if traffic camera alerts are enabled.
    if (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == True): # Check to see that the traffic camera database exists at the path specified in the configuration.
        loaded_traffic_camera_database = load_traffic_cameras(get_gps_location()[0], get_gps_location()[1], config["general"]["alert_databases"]["traffic_cameras"], float(config["general"]["traffic_camera_loaded_radius"])) # Load all traffic cameras within the configured loading radius.




# Load the ALPR camera database, if enabled.
if (float(config["general"]["alert_range"]["alpr_cameras"]) > 0): # Check to see if ALPR camera alerts are enabled.
    if (str(config["general"]["alert_databases"]["alpr_cameras"]) != "" and os.path.exists(str(config["general"]["alert_databases"]["alpr_cameras"]))): # Check to see if the ALPR camera database exists.
        loaded_alpr_camera_database = json.load(open(str(config["general"]["alert_databases"]["alpr_cameras"]))) # Load the ALPR database.






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



if (int(config["audio"]["sounds"]["startup"]["repeat"]) > 0): # Check to see if the user has the start up audio alert enabled.
    for i in range(0, int(config["audio"]["sounds"]["startup"]["repeat"])): # Repeat the sound several times, if the configuration says to.
        os.system("mpg321 " + config["audio"]["sounds"]["startup"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
        time.sleep(float(config["audio"]["sounds"]["startup"]["delay"])) # Wait before playing the sound again.





active_alarm = "none" # Set the active alert placeholder before starting the main loop.



while True: # Run forever in a loop until terminated.


    # Process all information that needs to be handled at the beginning of each cycle.

    if (config["general"]["gps_enabled"] == True): # If GPS is enabled, then get the current location at the beginning of the cycle.
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






    clear() # Clear the console output at the beginning of every cycle.

    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.





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



    # Traffic enforcement camera alert display
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
                display_shape("circle") # Display an ASCII cross in the output.

            # Play audio alerts, as necessary.
            if (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.1)): # Check to see if the nearest camera is within 10% of the traffic camera alert radius.
                if (nearest_enforcement_camera["spd"] != None and config["general"]["traffic_camera_speed_check"] == True): # Check to see if speed limit data exists for this speed camera, and if the traffic camera speed check setting is enabled in the configuration.
                    if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then play a heightened alarm sound.
                        if (int(config["audio"]["sounds"]["alarm"]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
                            for i in range(0, int(config["audio"]["sounds"]["alarm"]["repeat"])): # Repeat the sound several times, if the configuration says to.
                                os.system("mpg321 " + config["audio"]["sounds"]["alarm"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                if (int(config["audio"]["sounds"]["camera3"]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
                    for i in range(0, int(config["audio"]["sounds"]["camera3"]["repeat"])): # Repeat the sound several times, if the configuration says to.
                        os.system("mpg321 " + config["audio"]["sounds"]["camera3"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                        time.sleep(float(config["audio"]["sounds"]["camera3"]["delay"])) # Wait before playing the sound again.
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.25)): # Check to see if the nearest camera is within 25% of the traffic camera alert radius.
                if (int(config["audio"]["sounds"]["camera2"]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
                    for i in range(0, int(config["audio"]["sounds"]["camera2"]["repeat"])): # Repeat the sound several times, if the configuration says to.
                        os.system("mpg321 " + config["audio"]["sounds"]["camera2"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                        time.sleep(float(config["audio"]["sounds"]["camera2"]["delay"])) # Wait before playing the sound again.
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]))): # Check to see if the nearest camera is within the traffic camera alert radius.
                if (int(config["audio"]["sounds"]["camera1"]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
                    for i in range(0, int(config["audio"]["sounds"]["camera1"]["repeat"])): # Repeat the sound several times, if the configuration says to.
                        os.system("mpg321 " + config["audio"]["sounds"]["camera1"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                        time.sleep(float(config["audio"]["sounds"]["camera1"]["delay"])) # Wait before playing the sound again.


    # ALPR camera alert display
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

        if (int(config["audio"]["sounds"]["alpr"]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
            for i in range(0, int(config["audio"]["sounds"]["alpr"]["repeat"])): # Repeat the sound several times, if the configuration says to.
                os.system("mpg321 " + config["audio"]["sounds"]["alpr"]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                time.sleep(float(config["audio"]["sounds"]["alpr"]["delay"])) # Wait before playing the sound again.



    # Telemetry recording
    if (config["general"]["record_telemetry"] == True): # Check to see if Assassin is configured to record telemetry data.
        if (config["general"]["gps_enabled"] == True): # Check to see if GPS features are enabled.
            export_data = str(round(time.time())) + "," + str(current_speed) + "," + str(current_location[0]) + "," + str(current_location[1]) + "," + str(current_location[3]) + "," + str(current_location[4]) + "," + str(current_location[5]) + "\n" # Add all necessary information to the export data.
        else:
            export_data = str(round(time.time())) + "," + str("0") + "," + str("0.000") + "," + str("0.000") + "," + str("0") + "," + str("0") + "," + str("0") + "\n" # Add all necessary information to the export data, using placeholders for information that depends on GPS.

        add_to_file(assassin_root_directory + "/information_recording.csv", export_data, True) # Add the export data to the end of the file and write it to disk.



    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
