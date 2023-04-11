# Assassin

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This script contains several funtions and classes used in main.py




# Define some styling information
class style:
    # Define colors
    red = '\033[91m'
    yellow = '\033[93m'
    green = '\033[92m'
    blue = '\033[94m'
    cyan = '\033[96m'
    pink = '\033[95m'
    purple = '\033[1;35m'
    gray = '\033[1;37m'
    brown = '\033[0;33m'
    black = '\033[0;30m'

    # Define text decoration
    bold = '\033[1m'
    underline = '\033[4m'
    italic = '\033[3m'
    faint = '\033[2m'

    # Define styling end marker
    end = '\033[0m'


import time # Required to add delays and handle dates/times

# Define the function to print debugging information when the configuration specifies to do so.
debugging_time_record = time.time()
def debug_message(message):
    if (config["general"]["debugging_output"] == True): # Only print the message if the debugging output configuration value is set to true.
        global debugging_time_record
        time_since_last_message = (time.time()-debugging_time_record) # Calculate the time since the last debug message.
        print(f"{style.italic}{style.faint}{time.time():.10f} ({time_since_last_message:.10f}) - {message}{style.end}") # Print the message.
        debugging_time_record = time.time() # Record the current timestamp.




import os # Required to interact with certain operating system functions
import json # Required to process JSON data

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


def load_config():
    # Locate and load the configuration file.
    if (os.path.exists(str(assassin_root_directory + "/config.json")) == True): # Check to see if the configuration file exists in the default location.
        config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json
    elif (os.path.exists(str(assassin_root_directory + "/../config.json")) == True): # Check to see if the configuration file exists in the parent directory. This may occur if this script is being used in a subfolder of Assassin.
        config = json.load(open(assassin_root_directory + "/../config.json")) # Load the configuration database from the parent directory.
    else: # The configuration file couldn't be located. Assassin can't continue to load.
        config = {} # Set the configuration to a blank placeholder dictionary.
        print("Configuration couldn't be located.")
        exit()

    return config # Return the loaded configuration information.


config = load_config() # Execute the configuration loading.




debug_message("Loading utils.py libraries")

debug_message("Importing `subprocess` library")
import subprocess # Required for starting some shell commands
debug_message("Importing `sys` library")
import sys
debug_message("Importing `datetime` library")
import datetime # Required for converting between timestamps and human readable date/time information
debug_message("Importing `minidom` library")
from xml.dom import minidom # Required for processing GPX data
debug_message("Importing `lzma` library")
import lzma # Required to load ExCam database
debug_message("Importing `math` library")
import math # Required to run more complex math calculations
debug_message("Importing `numpy` library")
import numpy # Required to run more complex math calculations
debug_message("Importing `csv` library")
import csv # Required to process CSV information.

if (config["display"]["status_lighting"]["enabled"] == True): # Only import the libraries required by the status lighting system if the status lighting is enabled. These two libraries have loading times much higher than other libraries, so this step can improve loading times.
    debug_message("Importing `requests` library")
    import requests # Required to make network requests
    debug_message("Importing `validators` library")
    import validators # Required to validate URLs


gps_enabled = config["general"]["gps_enabled"] # This setting determines whether or not Assassin's GPS features are enabled.

if (gps_enabled == True): # Only import the GPS libraries of the GPS configuration is enabled.
    debug_message("Importing `gps` library")
    from gps import * # Required to access GPS information.
    debug_message("Importing `gpsd` library")
    import gpsd # Required to access GPS information.






debug_message("Creating `display_notice` function")
def display_notice(message, level=1):
    level = int(level) # Convert the message level to an integer.
    message = str(message) # Convert the message to a string.

    if (level == 1): # The level is set to 1, indicating a standard notice.
        print(message)
        if (config["display"]["notices"]["1"]["wait_for_input"] == True): # Check to see if the configuration indicates to wait for user input before continuing.
            input("Press enter to continue...") # Wait for the user to press enter before continuning.
        else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
            time.sleep(float(config["display"]["notices"]["1"]["delay"])) # Wait for the delay specified in the configuration.

    elif (level == 2): # The level is set to 2, indicating a warning.
        print(style.yellow + "Warning: " + message + style.end)
        if (config["display"]["notices"]["2"]["wait_for_input"] == True): # Check to see if the configuration indicates to wait for user input before continuing.
            input("Press enter to continue...") # Wait for the user to press enter before continuning.
        else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
            time.sleep(float(config["display"]["notices"]["2"]["delay"])) # Wait for the delay specified in the configuration.

    elif (level == 3): # The level is set to 3, indicating an error.
        print(style.red + "Error: " + message + style.end)
        if (config["display"]["notices"]["3"]["wait_for_input"] == True): # Check to see if the configuration indicates to wait for user input before continuing.
            input("Press enter to continue...") # Wait for the user to press enter before continuning.
        else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
            time.sleep(float(config["display"]["notices"]["3"]["delay"])) # Wait for the delay specified in the configuration.







debug_message("Creating `processing_gpx` function")
# This function will be used to process GPX files into a Python dictionary.
def process_gpx(gpx_file):
    if (os.path.exists(gpx_file) == True): # Check to see if the GPX file exists.
        gpx_file = open(gpx_file, 'r') # Open the GPX document.

        xmldoc = minidom.parse(gpx_file) # Load the full XML GPX document.

        track = xmldoc.getElementsByTagName('trkpt') # Get all of the location information from the GPX document.
        timing = xmldoc.getElementsByTagName('time') # Get all of the timing information from the GPX document.

        gpx_data = {}  # Set the GPX data to a blank placeholder.

        for i in range(0, len(timing)): # Iterate through each point in the GPX file.
            point_lat = track[i].getAttribute('lat') # Get the latitude for this point.
            point_lon = track[i].getAttribute('lon') # Get the longitude for this point.
            point_time = str(timing[i].toxml().replace("<time>", "").replace("</time>", "").replace("Z", "").replace("T", " ")) # Get the time for this point in human readable text format.

            point_time = round(time.mktime(datetime.datetime.strptime(point_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the human readable timestamp into a Unix timestamp.

            gpx_data[point_time] = {"lat":point_lat, "lon":point_lon} # Add this point to the decoded GPX data.

    else: # The GPX file doesn't exist.
        display_notice("The GPX file doesn't exist.", 2)
        gpx_data = {}  # Set the GPX data to a blank placeholder.

    return gpx_data





# Define the function that will be used to clear the screen.
debug_message("Creating `clear` function")
def clear():
    if config["general"]["disable_console_clearing"] == False: # Only run the clearing function if the configuration value to disable clearing is set to false.
        if os.name == "nt": # Use 'cls' command if host is Windows
            os.system ("cls")
        else: # Use 'clear' command if host is Linux, BSD, MacOS, etc.
            os.system ("clear")



# Define the function that will be used to save files for exported data.
debug_message("Creating `save_to_file` function")
def save_to_file(file_name, contents, silence = False):
    debug_message("Saving file: " + str(file_name))
    fh = None
    success = False
    try:
        fh = open(file_name, 'w')
        fh.write(contents)
        success = True   
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
            debug_message("Saved file")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            display_notice("Failed to save!", 2)
            debug_message("Failed to save file")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success



# Define the fuction that will be used to add to the end of a file.
debug_message("Creating `add_to_file` function")
def add_to_file(file_name, contents, silence=False):
    debug_message("Adding to file: " + str(file_name))
    fh = None
    success = False
    try:
        fh = open(file_name, 'a')
        fh.write(contents)
        success = True
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
            debug_message("File saved")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            display_warning("Failed to save!", 2)
            debug_message("Failed to save file")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success






# Define a function for running a countdown timer.
debug_message("Creating `countdown` function")
def countdown(timer):
    timer = int(timer) # Make sure the timer is an integer number.

    if (timer > 0): # Make sure the timer is greater than 0 seconds.
        debug_message("Starting " + str(timer) + " second timer")
        for iteration in range(1, timer + 1): # Loop however many times specified by the `timer` variable.
            print(str(timer - iteration + 1)) # Display the current countdown number for this iteration, but subtracting the current iteration count from the total timer length.
            time.sleep(1) # Wait for 1 second.
    else:
        display_notice("The timer was less than 0 seconds, so it was skipped.", 2)






# Define the function that will be used to get the current GPS coordinates.
debug_message("Creating `get_gps_location` function")
def get_gps_location(): # Placeholder that should be updated at a later date.
    debug_message("Getting GPS location")
    if (gps_enabled == True): # Check to see if GPS is enabled.
        if (config["general"]["gps_demo_mode"]["enabled"] == True): # Check to see if GPS demo mode is enabled in the configuration.
            debug_message("Returning demo GPS information")
            return float(config["general"]["gps_demo_mode"]["longitude"]), float(config["general"]["gps_demo_mode"]["latitude"]), float(config["general"]["gps_demo_mode"]["speed"]), float(config["general"]["gps_demo_mode"]["altitude"]), float(config["general"]["gps_demo_mode"]["heading"]), int(config["general"]["gps_demo_mode"]["satellites"]) # Return the sample GPS information defined in the configuration.
        else: # GPS demo mode is disabled, so attempt to get the actual GPS data from GPSD.
            try: # Don't terminate the entire script if the GPS location fails to be aquired.
                debug_message("Connecting to GPSD")
                gpsd.connect() # Connect to the GPS daemon.
                debug_message("Fetching GPS information")
                gps_data_packet = gpsd.get_current() # Get the current information.
                debug_message("Received GPS information")
                return gps_data_packet.position()[0], gps_data_packet.position()[1], gps_data_packet.speed(), gps_data_packet.altitude(), gps_data_packet.movement()["track"], gps_data_packet.sats # Return GPS information.
            except: # If the current location can't be established, then return placeholder location data.
                return 0.0000, -0.0000, 0.0, 0.0, 0.0, 0 # Return a default placeholder location.
                debug_message("GPS fetch failed")
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        return 0.0000, 0.0000, 0.0, 0.0, 0.0, 0 # Return a default placeholder location.
        debug_message("GPS is disabled")




# Define a simple function to calculate the approximate distance between two points in miles.
debug_message("Creating `get_distance` function")
def get_distance(lat1, lon1, lat2, lon2, efficient_mode = True):

    # Convert the coordinates received.
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    # Verify the coordinates received, if efficient mode is disabled.
    if (efficient_mode == False):
        if (lat1 > 180 or lat1 < -180):
            display_notice("Latitude value 1 is out of bounds, and is invalid.", 2)
            lat1 = 0 # Default to a safe value.
        if (lon1 > 90 or lon1 < -90):
            display_notice("Longitude value 1 is out of bounds, and is invalid.", 2)
            lon1 = 0 # Default to a safe value.
        if (lat2 > 180 or lat2 < -180):
            display_notice("Latitude value 2 is out of bounds, and is invalid.", 2)
            lat2 = 0 # Default to a safe value.
        if (lon2 > 90 or lon2 < -90):
            display_notice("Longitude value 2 is out of bounds, and is invalid.", 2)
            lon2 = 0 # Default to a safe value.

    if (lon1 == lon2 and lat1 == lat2): # Check to see if the coordinates are the same.
        distance = 0 # The points are the same, so they are 0 miles apart.

    else: # The points are different, so calculate the distance between them
        # Convert the coordinates into radians.
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Calculate the distance.
        distance = 6371.01 * math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon1 - lon2))

        # Convert the distance from kilometers to miles.
        distance = distance * 0.6213712

    # Return the calculated distance.
    return distance







# Define the function that will be used to fetch all traffic cameras within a certain radius and load them to memory.
debug_message("Creating `load_traffic_cameras` function")
def load_traffic_cameras(current_lat, current_lon, database_file, radius):
    if (os.path.exists(database_file) == True): # Check to make sure the database specified in the configuration actually exists.
        debug_message("Opening traffic enforcement camera database")
        with lzma.open(database_file, "rt", encoding="utf-8") as f: # Open the database file.
            database_lines = list(map(json.loads, f)) # Load the camera database
            loaded_database_information = [] # Load an empty placeholder database so we can write data to it later.
            
            debug_message("Loading traffic enforcement cameras from database")
            for camera in database_lines: # Iterate through each camera in the database.
                if ("lat" in camera and "lon" in camera): # Only check this camera if it has a latitude and longitude defined in the database.
                    if (get_distance(current_lat, current_lon, camera['lat'], camera['lon']) < float(radius)): # Check to see if this camera is inside the initial loading radius.
                        loaded_database_information.append(camera)
    else: # The database file specified does not exist.
        loaded_database_information = [] # Return a blank database if the file specified doesn't exist.

    return loaded_database_information # Return the newly edited database information.




# Define the function that will be used to get nearby speed, red light, and traffic cameras from a loaded database.
debug_message("Creating `nearby_traffic_cameras` function")
def nearby_traffic_cameras(current_lat, current_lon, database_information, radius=1.0): # This function is used to get a list of all traffic enforcement cameras within a certain range of a given location.
    nearby_speed_cameras, nearby_redlight_cameras, nearby_misc_cameras = [], [], [] # Create empty placeholder lists for each camera type.

    if (len(database_information) > 0): # Check to see if the supplied database information has data in it.
        camera_id = 0 # This will be incremented up by 1 for each camera iterated through in the database.
        for camera in database_information: # Iterate through each camera in the loaded database.
            camera_id = camera_id + 1
            camera["id"] = camera_id
            current_distance = get_distance(current_lat, current_lon, camera['lat'], camera['lon'])
            if (current_distance < float(radius)): # Only show the camera if it's within a certain radius of the current location.
                camera["dst"] = current_distance # Save the current distance from this camera to it's data before adding it to the list of nearby speed cameras.
                if (camera["flg"] == 0 or camera["flg"] == 2 or camera["flg"] == 3): # Check to see if this particular camera is speed related.
                    nearby_speed_cameras.append(camera) # Add this camera to the "nearby speed camera" list.
                elif (camera["flg"] == 1): # Check to see if this particular camera is red-light related.
                    nearby_redlight_cameras.append(camera) # Add this camera to the "nearby red light camera" list.
                else:
                    nearby_misc_cameras.append(camera) # Add this camera to the "nearby general traffic camera" list.

    else: # The supplied database information was empty.
        pass

    return nearby_speed_cameras, nearby_redlight_cameras, nearby_misc_cameras # Return the list of nearby cameras for all types.







# Define the function that calculates the bearing between two coordinate pairs.
debug_message("Creating `calculate_bearing` function")
def calculate_bearing (lat1, lon1, lat2, lon2):
    # Convert the coordinates received.
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)

    # Verify the coordinates received.
    if (lat1 > 180 or lat1 < -180):
        display_notice("Latitude value 1 is out of bounds, and is invalid.", 2)
        lat1 = 0 # Default to a safe value.
    if (lon1 > 90 or lon1 < -90):
        display_notice("Longitude value 1 is out of bounds, and is invalid.", 2)
        lon1 = 0 # Default to a safe value.
    if (lat2 > 180 or lat2 < -180):
        display_notice("Latitude value 2 is out of bounds, and is invalid.", 2)
        lat2 = 0 # Default to a safe value.
    if (lon2 > 90 or lon2 < -90):
        display_notice("Longitude value 2 is out of bounds, and is invalid.", 2)
        lon2 = 0 # Default to a safe value.


    # Calculate the bearing.
    longitude_difference = (lon2 - lon1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(longitude_difference))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(longitude_difference))
    bearing = numpy.arctan2(x,y) # Calculate the bearing, in radians.
    bearing = numpy.degrees(bearing) # Convert the bearing to degrees.

    # Return the bearing.
    return bearing




debug_message("Creating `nearby_database_poi` function")
def nearby_database_poi(current_location, database_information, radius=1.0): # This function is used to get a list of all points of interest from a particular database within a certain range of a given location.
    current_lat = current_location[0]
    current_lon = current_location[1]
    current_heading = current_location[2]
    nearby_database_information = [] # Create a placeholder list to add the nearby POIs to in the next steps.
    for entry in database_information["entries"]: # Iterate through each entry in the loaded database information.
        current_distance = get_distance(current_lat, current_lon, entry['lat'], entry['lon']) # Get the current distance to the POI in question.
        entry["distance"] = current_distance # Append the current POI's distance to it's database information.
        entry["bearing"] = calculate_bearing(current_lat, current_lon, entry["lat"], entry["lon"]) # Calculate the bearing to the POI.
        if (entry["bearing"] < 0): # If the bearing to the POI is negative, then convert it to a positive bearing.
            entry["bearing"] = 360 + entry["bearing"] # Convert the bearing to a positive number.

        if (entry["direction"] != ""): # Check to see if this POI has direction information.
            entry["relativefacing"] = entry["direction"] - current_location[4] # Calculate the direction of this POI relative to the current direction of motion.
            if (entry["relativefacing"] < 0): # If the relative facing direction of the POI is negative, then convert it to a positive direction.
                entry["relativefacing"] = 360 + entry["relativefacing"] # Convert the relative facing direction to a positive value.

        if (current_distance < float(radius)): # Check to see if the current POI is within range of the user.
            nearby_database_information.append(entry) # Add this entry to the list of POIs within range.

    return nearby_database_information # Return the new database with the newly added distance information.







debug_message("Creating `convert_speed` function")
def convert_speed(speed, unit="mph"): # This function is used to convert speeds from meters per second, to other units.
    unit = unit.lower() # Convert the unit to all lowercase in order to make it easier to work with and remove inconsistencies in configuration setups.
    unit = unit.strip() # Remove any trailing or leading whitespaces in the unit in an attempt to recover from malformatted units.

    if (unit == "kph"): # Convert the speed to kilometers per hour.
        speed = speed * 3.6 # The speed is already measured in kilometers per hour, so there is no reason to convert it.
    elif (unit == "mph"): # Convert the speed to miles per hour.
        speed = speed * 2.236936
    elif (unit == "mps"): # Convert the speed to meters per second.
        speed = speed # The speed is already measured in meters per second, so there is no reason to convert it.
    elif (unit == "knot"): # Convert the speed to knots.
        speed = speed * 1.943844
    elif (unit == "fps"): # Convert the speed to feet per second.
        speed = speed * 3.28084
    else: # If an invalid unit was supplied, then simply return a speed of zero.
        display_notice("Invalid speed unit supplied.", 2) # Display a warning.
        speed = 0

    return speed # Return the converted speed.





debug_message("Creating `display_number` function")
def display_number(display_number="0"): # This function is used to display a number as a large ASCII character.
    numbers = {} # Create a placeholder dictionary for all numbers.
    numbers["."] = ["    ", "    ", "    ", "    ", "    ", "    ", " ## ", " ## "] # Define each line in the ASCII art for zero.
    numbers["0"] = [" $$$$$$\\  ", "$$$ __$$\\ ", "$$$$\\ $$ |", "$$\\$$\\$$ |", "$$ \\$$$$ |", "$$ |\\$$$ |", "\\$$$$$$  /", " \\______/ "] # Define each line in the ASCII art for zero.
    numbers["1"] = ["  $$\\   ", "$$$$ |  ", "\\_$$ |  ", "  $$ |  ", "  $$ |  ", "  $$ |  ", "$$$$$$\ ", "\\______|"] # Define each line in the ASCII art for one.
    numbers["2"] = [" $$$$$$\\  ", "$$  __$$\\ ", "\\__/  $$ |", " $$$$$$  |", "$$  ____/ ", "$$ |      ", "$$$$$$$$\\ ", "\\________|"] # Define each line in the ASCII art for two.
    numbers["3"] = [" $$$$$$\\  ", "$$ ___$$\\ ", "\\_/   $$ |", "  $$$$$ / ", "  \\___$$\\ ", "$$\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for three.
    numbers["4"] = ["$$\\   $$\\ ", "$$ |  $$ |", "$$ |  $$ |", "$$$$$$$$ |", "\\_____$$ |", "      $$ |", "      $$ |", "      \\__|"] # Define each line in the ASCII art for four.
    numbers["5"] = ["$$$$$$$\\  ", "$$  ____| ", "$$ |      ", "$$$$$$$\\  ", "\_____$$\\ ", "$$\\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for five.
    numbers["6"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  \\__|", "$$$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", " $$$$$$  |", " \\______/ "] # Define each line in the ASCII art for six.
    numbers["7"] = ["$$$$$$$$\\ ", "\\____$$  |", "    $$  / ", "   $$  /  ", "  $$  /   ", " $$  /    ", "$$  /     ", "\\__/      "] # Define each line in the ASCII art for seven.
    numbers["8"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", " $$$$$$  |", "$$  __$$< ", "$$ /  $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for eight.
    numbers["9"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", "\\$$$$$$$ |", " \\____$$ |", "$$\\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for nine.

    display_lines = {} # Create a placeholder for each line that will be printed to the console.

    for line_count in range(0, 8): # Iterate through each of the 8 lines that the output will have.
        display_lines[line_count] = "" # Set each line to an empty placeholder string.

    for display_character in str(display_number): # Iterate through each character that needs to be displayed.
        for individual_display_line in range(0, 8): # Iterate through each line that will be displayed to the console output.
            display_lines[individual_display_line] = str(display_lines[individual_display_line]) + numbers[str(display_character)][individual_display_line] # Add each number to each line of the output.

    for line_index in display_lines: # Iterate through each line that needs to displayed.
        print(display_lines[line_index]) # Print each individual line.





debug_message("Creating `get_cardinal_direction` function")
def get_cardinal_direction(heading=0): # Define the function used to convert degrees into cardinal directions.
    heading = int(heading) # Convert the heading to an integer.

    if (heading < 0): # Check to see if the heading is a negative number.
         heading = 360 + heading # Convert the heading to a positive number. 

    while heading > 360: # Check to see if the heading exceeds 360 degrees
        heading = heading - 360 # Reduce the heading by 360 degrees until it falls under the 360 degree threshold.

    direction = round(heading / 45) # Divide the current heading in degrees into 8 segments, each representing a cardinal direction or sub-cardinal direction.
    if (direction == 0 or direction == 8):
        return "N"
    elif (direction == 1):
        return "NE"
    elif (direction == 2):
        return "E"
    elif (direction == 3):
        return "SE"
    elif (direction == 4):
        return "S"
    elif (direction == 5):
        return "SW"
    elif (direction == 6):
        return "W"
    elif (direction == 7):
        return "NW"
    else: # This case should never occur.
        return "ERROR" # Return an error indicating that the information supplied to the function was invalid.


debug_message("Creating `get_arrow_direction` function")
def get_arrow_direction(heading=0): # Define the function used to convert degrees into an arrow pointing in a particular direction.
    heading = int(heading) # Convert the heading to an integer.

    if (heading < 0): # Check to see if the heading is a negative number.
         heading = 360 + heading # Convert the heading to a positive number. 

    while heading > 360: # Check to see if the heading exceeds 360 degrees
        heading = heading - 360 # Reduce the heading by 360 degrees until it falls under the 360 degree threshold.

    direction = round(heading / 45) # Divide the current heading in degrees into 8 segments, each representing a cardinal direction or sub-cardinal direction.
    if (direction == 0 or direction == 8):
        return "↑"
    elif (direction == 1):
        return "⬈"
    elif (direction == 2):
        return "→"
    elif (direction == 3):
        return "⬊"
    elif (direction == 4):
        return "↓"
    elif (direction == 5):
        return "⬋"
    elif (direction == 6):
        return "←"
    elif (direction == 7):
        return "⬉"
    else: # This case should never occur.
        return "ERROR" # Return an error indicating that the information supplied to the function was invalid.
