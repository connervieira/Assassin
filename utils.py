# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
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
    purple = '\033[35m'
    gray = '\033[37m'
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
debugging_time_record = time.time() # This value holds the time that the previous debug message was displayed.
def debug_message(message):
    if (config["general"]["debugging_output"] == True): # Only print the message if the debugging output configuration value is set to true.
        global debugging_time_record
        time_since_last_message = (time.time()-debugging_time_record) # Calculate the time since the last debug message.
        print(f"{style.italic}{style.faint}{time.time():.10f} ({time_since_last_message:.10f}) - {message}{style.end}") # Print the message.
        debugging_time_record = time.time() # Record the current timestamp.




import os # Required to interact with certain operating system functions
import json # Required to process JSON data

def is_json(string):
    try:
        json_object = json.loads(string) # Try to load string as JSON information.
    except ValueError as error_message: # If the process fails, then the string is not valid JSON.
        return False # Return 'false' to indicate that the string is not JSON.

    return True # If the try statement is successful, then return 'true' to indicate that the string is valid JSON.


assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

import config
load_config = config.load_config

config = load_config() # Load the configuration.


import sys
if ("--headless" in sys.argv):
    headless_mode = True
else:
    headless_mode = False


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

if (config["audio"]["tts"]["enabled"] == True): # Only import the TTS libraries of text to speech functionality is enabled.
    debug_message("Importing `pyttxs3` library")
    import pyttsx3 # Import the text-to-speech library.
    tts = pyttsx3.init() # Initialize the text-to-speech engine.
    tts.setProperty('rate', config["audio"]["tts"]["speed"]) # Set the text-to-speech speed.

if (config["audio"]["provider"] == "playsound"): # Check to see if the configured audio provider is playsound.
    debug_message("Importing `playsound` library")
    from playsound import playsound # Import the playsound library.


if (config["display"]["status_lighting"]["enabled"] == True): # Only import the libraries required by the status lighting system if the status lighting is enabled. These two libraries have loading times much higher than other libraries, so this step can improve loading times.
    debug_message("Importing `requests` library")
    import requests # Required to make network requests
    debug_message("Importing `validators` library")
    import validators # Required to validate URLs


gps_enabled = config["general"]["gps"]["enabled"] # This setting determines whether or not Assassin's GPS features are enabled.


# Define the function that will be used to clear the screen.
debug_message("Creating `clear` function")
def clear():
    global headless_mode
    if (config["general"]["disable_console_clearing"] == False and headless_mode == False): # Only run the clearing function if the configuration value to disable clearing is set to false.
        if os.name == "nt": # Use 'cls' command if host is Windows
            os.system ("cls")
        else: # Use 'clear' command if host is Linux, BSD, MacOS, etc.
            os.system ("clear")





# Define the function that will be used to save files for exported data.
debug_message("Creating `save_to_file` function")
def save_to_file(file_name, contents, silence=True):
    file_name = file_name.replace("//","/")
    if (silence == False):
        debug_message("Saving file: " + str(file_name))
    file = None
    success = False
    try:
        file = open(file_name, 'w')
        file.write(contents)
        success = True   
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
            debug_message("Saved file")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            debug_message("Failed to save file")
    finally:
        try:
            if file:
                file.close()
        except:
            success = False
    return success



# Define the fuction that will be used to add to the end of a file.
debug_message("Creating `add_to_file` function")
def add_to_file(file_name, contents, silence=True):
    file_name = file_name.replace("//","/")
    if (silence == False):
        debug_message("Adding to file: " + str(file_name))
    file = None
    success = False
    try:
        file = open(file_name, 'a')
        file.write(contents)
        success = True
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
            debug_message("File saved")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            debug_message("Failed to save file")
    finally:
        try:
            if file:
                file.close()
        except:
            success = False
    return success




debug_message("Creating `display_notice` function")
if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
    status_file_location = config["external"]["local"]["interface_directory"] + "/status.json"
    if (os.path.exists(status_file_location) == False): # If the error log file doesn't exist, create it.
        save_to_file(status_file_location, "{}", True) # Save a blank placeholder dictionary to the error log file.

    error_file = open(status_file_location, "r") # Open the error log file for reading.
    error_file_contents = error_file.read() # Read the raw contents of the error file as a string.
    error_file.close() # Close the error log file.

    if (is_json(error_file_contents) == True): # If the error file contains valid JSON data, then load it.
        status_log = json.loads(error_file_contents) # Read and load the error log from the file.
    else: # If the error file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        status_log = json.loads("{}") # Load a blank placeholder dictionary.
else: # Interfacing with local services is disabled.
    status_log = {} # Set the error log to a blank placeholder.

def display_notice(message, level=1):
    global headless_mode
    level = int(round(float(level))) # Convert the message level to an integer.
    message = str(message) # Convert the message to a string.

    if (level == 1): # The level is set to 1, indicating a standard notice.
        if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
            status_log[time.time()] = [1, message] # Add this warning message to the log file, using the current time as the key.
            save_to_file(status_file_location, json.dumps(status_log), True) # Save the modified error log to the disk as JSON data.
        if (config["display"]["display_status_messages"] == True and headless_mode == False): # Check to see if the configuration indicates that status messages should be displayed.
            print(message)
            if (config["display"]["notices"]["1"]["wait_for_input"] == True): # Check to see if the configuration indicates to wait for user input before continuing.
                input("Press enter to continue...") # Wait for the user to press enter before continuning.
            else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
                time.sleep(float(config["display"]["notices"]["1"]["delay"])) # Wait for the delay specified in the configuration.

    elif (level == 2): # The level is set to 2, indicating a warning.
        if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
            status_log[time.time()] = [2, message] # Add this warning message to the log file, using the current time as the key.
            save_to_file(status_file_location, json.dumps(status_log), True) # Save the modified error log to the disk as JSON data.
        print(style.yellow + "Warning: " + message + style.end)
        if (headless_mode == False):
            if (config["display"]["notices"]["2"]["wait_for_input"] == True): # Check to see if the configuration indicates to wait for user input before continuing.
                input("Press enter to continue...") # Wait for the user to press enter before continuning.
            else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
                time.sleep(float(config["display"]["notices"]["2"]["delay"])) # Wait for the delay specified in the configuration.

    elif (level == 3): # The level is set to 3, indicating an error.
        if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
            status_log[time.time()] = [3, message] # Add this error message to the log file, using the current time as the key.
            save_to_file(status_file_location, json.dumps(status_log), True) # Save the modified error log to the disk as JSON data.
        print(style.red + "Error: " + message + style.end)
        if (headless_mode == False):
            if (config["display"]["notices"]["3"]["wait_for_input"] == True and headless_mode == False): # Check to see if the configuration indicates to wait for user input before continuing.
                input("Press enter to continue...") # Wait for the user to press enter before continuning.
            else: # If the configuration doesn't indicate to wait for user input, then wait for a delay specified in the configuration for this notice level.
                time.sleep(float(config["display"]["notices"]["3"]["delay"])) # Wait for the delay specified in the configuration.





process_timers = {}
def process_timing(identifier, action):
    global process_timers

    if (identifier not in process_timers and action != "dump"): # Check to see if the specified identifier doesn't exist in the process_timer dictionary.
        process_timers[identifier] = {"total": 0, "start": 0} # Initialize the timer for this process.

    if (action == "dump"):
        return process_timers
    elif (action == "start"):
        process_timers[identifier]["start"] = time.time()
    elif (action == "end"):
        if (process_timers[identifier]["start"] != 0):
            process_timers[identifier]["total"] = process_timers[identifier]["total"] + (time.time() - process_timers[identifier]["start"])
            process_timers[identifier]["start"] = 0
        else:
            display_notice("The `processing_timing` function was called setting the end of the timer (" + identifier + "), but the timer wasn't started. This is likely a bug.", 2)
    else:
        display_notice("The `processing_timing` function was called with an unknown action. This likely a bug.", 2)






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





# This is a simple function used to display large ASCII shapes.
debug_message("Creating `display_shape` function")
def display_shape(shape):
    if (config["display"]["shape_alerts"] == True): # Check to see if shape alerts are enabled in the configuration.
        if (shape == "square"):
            print(style.bold)
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print("######################")
            print(style.end)

        elif (shape == "circle"):
            print(style.bold)
            print("        ######")
            print("     ############")
            print("   ################")
            print("  ##################")
            print(" ####################")
            print("######################")
            print("######################")
            print("######################")
            print(" ####################")
            print("  ##################")
            print("   ################")
            print("     ############")
            print("        ######")
            print(style.end)

        elif (shape == "triangle"):
            print(style.bold)
            print("           #")
            print("          ###")
            print("         #####")
            print("        #######")
            print("       #########")
            print("      ###########")
            print("     #############")
            print("    ###############")
            print("   #################")
            print("  ###################")
            print(" #####################")
            print("#######################")
            print(style.end)

        elif (shape == "diamond"):
            print(style.bold)
            print("           #")
            print("          ###")
            print("         #####")
            print("        #######")
            print("       #########")
            print("      ###########")
            print("     #############")
            print("      ###########")
            print("       #########")
            print("        #######")
            print("         #####")
            print("          ###")
            print("           #")
            print(style.end)

        elif (shape == "cross"):
            print(style.bold)
            print("########              ########")
            print("  ########          ########")
            print("    ########      ########")
            print("      ########  ########")
            print("        ##############")
            print("          ##########")
            print("        ##############")
            print("      ########  ########")
            print("    ########      ########")
            print("  ########          ########")
            print("########              ########")
            print(style.end)

        elif (shape == "horizontal"):
            print(style.bold)
            print("############################")
            print("############################")
            print("############################")
            print("############################")
            print(style.end)

        elif (shape == "vertical"):
            print(style.bold)
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print("           ######")
            print(style.end)








# Define a simple function to calculate the approximate distance between two points in miles.
debug_message("Creating `get_distance` function")
def get_distance(lat1, lon1, lat2, lon2, efficient_mode = True):
    try:
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
    except:
        return 0.0







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





# Define the function that gets the difference between two bearings.
debug_message("Creating `bearing_difference` function")
def bearing_difference(bearing1, bearing2):
    # Convert the bearings received.
    bearing1 = float(bearing1)
    bearing2 = float(bearing2)

    # Make sure both of the bearings are positive.
    while bearing1 < 0:
        bearing1 = bearing1 + 360
    while bearing2 < 0:
        bearing2 = bearing2 + 360

    # Make sure both of the bearings are less than 360 degrees.
    while bearing1 > 0:
        bearing1 = bearing1 - 360
    while bearing2 > 0:
        bearing2 = bearing2 - 360


    method1 = abs(bearing1 - bearing2)
    method2 = abs(method1 - 360)

    if (method1 < method2):
        return method1
    elif (method2 <= method1):
        return method2




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

        if (entry["facing"] != ""): # Check to see if this POI has direction information.
            entry["relativefacing"] = entry["facing"] - current_location[4] # Calculate the direction of this POI relative to the current direction of motion.
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

    if (config["display"]["diagonal_arrows"] == True): # Check to see if diagonal arrows are enabled in the configuration.
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

    else: # Diagonal arrows are disabled in the configuration, so round to the nearest 90 degrees instead.
        direction = round(heading / 90) # Divide the current heading in degrees into 8 segments, each representing a cardinal direction or sub-cardinal direction.
        if (direction == 0 or direction == 4):
            return "↑"
        elif (direction == 1):
            return "→"
        elif (direction == 2):
            return "↓"
        elif (direction == 3):
            return "←"
        else: # This case should never occur.
            return "ERROR" # Return an error indicating that the information supplied to the function was invalid.




debug_message("Creating `update_status_lighting` function")
def update_status_lighting(url_id): # Define the function used to update status lighting. This function is primarily designed to interface with WLED RGB LED controllers, but it should work for other systems that use network requests to update lighting.
    process_timing("Status Lighting", "start")
    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        debug_message("Updating status lighting")
        status_lighting_update_url = str(config["display"]["status_lighting"]["status_lighting_values"][url_id]).replace("[U]", str(config["display"]["status_lighting"]["base_url"]))# Prepare the URL where a request will be sent in order to update the status lighting.
        if (validators.url(status_lighting_update_url)): # Check to make sure the URL ID supplied actually resolves to a valid URL in the configuration database.
            debug_message("Sending status lighting network request")
            try:
                response = requests.get(status_lighting_update_url)
                debug_message("Updated status lighting")
            except:
                debug_message("Failed to update status lighting")
                display_notice("Unable to update status lighting. No network response.", 2) # Display a warning that the URL was invalid, and no network request was sent.
        else:
            display_notice("Unable to update status lighting. Invalid URL configured for " + str(url_id) + ".", 2) # Display a warning that the URL was invalid, and no network request was sent.
    process_timing("Status Lighting", "end")






# This function is used to play a given sound as defined in the configuration.
debug_message("Creating `play_sound` function")
def play_sound(sound_id):
    process_timing("Audio/Sound Effects", "start")
    if (str(sound_id) in config["audio"]["sounds"]): # Check to see that a sound with the specified sound ID exists in the configuration.
        if (int(config["audio"]["sounds"][str(sound_id)]["repeat"]) > 0): # Check to see if this sound effect is enabled.
            if (os.path.exists(str(config["audio"]["sounds"][str(sound_id)]["path"])) == True and str(config["audio"]["sounds"][str(sound_id)]["path"]) != ""): # Check to see if the sound file associated with the specified sound ID actually exists.
                debug_message("Playing sound " + str(sound_id))
                for i in range(0, int(config["audio"]["sounds"][str(sound_id)]["repeat"])): # Repeat the sound several times, if the configuration says to do so.
                    if (config["audio"]["provider"] == "mpg321"): # Check to see if the configured audio provider is MPG321.
                        os.system("mpg321 " + config["audio"]["sounds"][str(sound_id)]["path"] + " > /dev/null 2>&1 &") # Play the sound file associated with this sound ID in the configuration.
                        time.sleep(float(config["audio"]["sounds"][str(sound_id)]["delay"])) # Wait before playing the sound again.
                    elif (config["audio"]["provider"] == "playsound"): # Check to see if the configured audio provider is playsound.
                        playsound(config["audio"]["sounds"][str(sound_id)]["path"], False) # Play the sound file associated with this sound ID in the configuration.
                        time.sleep(float(config["audio"]["sounds"][str(sound_id)]["delay"])) # Wait before playing the sound again.
                    else:
                        display_notice("The audio provider is configured incorrectly.", 2)
            elif (str(config["audio"]["sounds"][str(sound_id)]["path"]) == ""): # The file path associated with this sound ID is left blank, and therefore the sound can't be played.
                display_notice("The sound file path associated with sound ID (" + str(sound_id) + ") is blank.", 2)
            elif (os.path.exists(str(config["audio"]["sounds"][str(sound_id)]["path"])) == False): # The file path associated with this sound ID does not exist, and therefore the sound can't be played.
                display_notice("The sound file path associated with sound ID (" + str(sound_id) + ") does not exist.", 2)
    else: # No sound with this ID exists in the configuration database, and therefore the sound can't be played.
        display_notice("No sound with the ID (" + str(sound_id) + ") exists in the configuration.", 2)
    process_timing("Audio/Sound Effects", "end")







# This function is used to convert a text sample into audible speech and play it.
debug_message("Creating `speak` function")
def speak(full_text, brief_text):
    if (config["audio"]["tts"]["enabled"] == True): # Only play text-to-speech if it is enabled in the configuration.
        debug_message("Playing text-to-speech")
        if (config["audio"]["tts"]["brief"] == True): # Check to see if brief mode is enabled in the configuration.
            tts.say(brief_text)
            tts.runAndWait()
        else:
            tts.say(full_text)
            tts.runAndWait()



# This function converts a human-readable UTC timestamp into a Unix epoch timestamp.
debug_message("Creating `utc_datetime` function")
def utc_datetime(timestamp):
    timestamp = float(timestamp)
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


# This function takes the location history and exports it into a GPX file.
debug_message("Creating `save_gpx` function")
def save_gpx(location_history):
    if (type(location_history) == list): # Check to make sure the location_history provided is a list.
        if (os.path.isdir(config["general"]["telemetry"]["directory"]) == True): # Check to make sure the save directory specified in the configuration exists and is actually a directory.
            debug_message("Generating GPX location track")

            file_contents = '<?xml version="1.0" encoding="UTF-8" ?>\n<gpx version="1.0" creator="V0LT Assassin">\n    <time>' + utc_datetime(location_history[0]["time"]) + '</time>\n    <trk>\n        <trkseg>\n' # Set-up the start of the file.

            for point in location_history: # Iterate through each point in the location history .
                file_contents = file_contents + '            ' # Add indents to the beginning of each point line to make the file human-readable.
                file_contents = file_contents + '<trkpt lat="' + str(point["lat"]) + '" lon="' + str(point["lon"]) + '">' # Add the latitude and longitude to this point.
                file_contents = file_contents + '<time>' + str(utc_datetime(point["time"])) + '</time>' # Add the time to this point.
                file_contents = file_contents + '<ele>' + str(point["alt"]) + '</ele>' # Add the elevation to this point.
                file_contents = file_contents + '<sat>' + str(point["sat"]) + '</sat>' # Add the number of satellites to this point.
                file_contents = file_contents + '<speed>' + str(point["spd"]) + '</speed>' # Add the speed to this point.
                file_contents = file_contents + '<src>' + str(point["src"]) + '</src>' # Add the location source to this point.
                file_contents = file_contents + '</trkpt>\n' # Close this point.

            file_contents = file_contents + "        </trkseg>\n    </trk>\n</gpx>" # Set-up the end of the file.

            file_name = config["general"]["telemetry"]["file"].replace("{T}", str(round(location_history[0]["time"]))) # Set up the file name that the telemetry information will be saved to.
            file_path = config["general"]["working_directory"] + "/" + file_name # Set up the complete file path that the telemetry information will be saved to.

            save_to_file(file_path, file_contents, True) # Save the telemetry data to a file.

    else:
        display_notice("The location history supplied to save_gpx() isn't a valid list. This is most likely a bug. Telemetry logging could not be recorded.", 2)
