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

if (config["general"]["tts"]["enabled"] == True): # Only import the TTS libraries of text to speech functionality is enabled.
    import pyttsx3 # Import the text-to-speech library.
    tts = pyttsx3.init() # Initialize the text-to-speech engine.
    tts.setProperty('rate', config["general"]["tts"]["speed"]) # Set the text-to-speech speed.


if (config["display"]["status_lighting"]["enabled"] == True): # Only import the libraries required by the status lighting system if the status lighting is enabled. These two libraries have loading times much higher than other libraries, so this step can improve loading times.
    debug_message("Importing `requests` library")
    import requests # Required to make network requests
    debug_message("Importing `validators` library")
    import validators # Required to validate URLs


gps_enabled = config["general"]["gps_enabled"] # This setting determines whether or not Assassin's GPS features are enabled.

if (gps_enabled == True and config["general"]["gps_provider"] == "gpsd"): # Only import the GPS libraries if GPS is enabled in the configuration, and the GPSD provider is selected.
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
            return float(config["general"]["gps_demo_mode"]["longitude"]), float(config["general"]["gps_demo_mode"]["latitude"]), float(config["general"]["gps_demo_mode"]["speed"]), float(config["general"]["gps_demo_mode"]["altitude"]), float(config["general"]["gps_demo_mode"]["heading"]), int(config["general"]["gps_demo_mode"]["satellites"]), "V0LT Assassin - GPS demo mode" # Return the sample GPS information defined in the configuration.
        else: # GPS demo mode is disabled, so attempt to get the actual GPS data from GPSD.
            if (config["general"]["gps_provider"] == "gpsd"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Connecting to GPSD")
                    gpsd.connect() # Connect to the GPS daemon.
                    debug_message("Fetching GPSD information")
                    gps_data_packet = gpsd.get_current() # Get the current information.
                    debug_message("Received GPSD information")
                    return gps_data_packet.position()[0], gps_data_packet.position()[1], gps_data_packet.speed(), gps_data_packet.altitude(), gps_data_packet.movement()["track"], gps_data_packet.sats, "V0LT Assassin - GPSD Device" # Return GPS information.
                except: # If the current location can't be established, then return placeholder location data.
                    return [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            elif (config["general"]["gps_provider"] == "termux"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Fetching termux-location information")
                    raw_termux_response = str(os.popen("termux-location").read()) # Execute the Termux location command.
                    termux_response = json.loads(raw_termux_response) # Load the location information from the Termux response.
                    debug_message("Received termux-location information")
                    return termux_response["latitude"], termux_response["longitude"], termux_response["speed"], termux_response["altitude"], termux_response["bearing"], 0, "V0LT Assassin - Termux-API" # Return the fetched GPS information.
                except:
                    return [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            elif (config["general"]["gps_provider"] == "locateme"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Fetching LocateMe information")
                    raw_locateme_response = str(os.popen("locateme -f {LAT},{LON},{SPD},{ALT},{DIR},0").read()) # Execute the LocateMe location command.
                    locateme_response = raw_locateme_response.split(",") # Load the location information from the LocateMe response.
                    locateme_respose.append("V0LT Assassin - MacOS Location Services via LocateMe") # Append the location provider to the information.
                    debug_message("Received LocateMe information")
                    return float(locateme_response[0]), float(locateme_response[1]), float(locateme_response[2]), float(locateme_response[3]), float(locateme_response[4]), 0 # Return the fetched GPS information.
                except:
                    return [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            else:
                return [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                debug_message("Invalid location provider")
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        return [0.0000, 0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
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
                camera["bearing"] = calculate_bearing(camera["lat"], camera["lon"], current_lat, current_lon)
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
        current_distance = get_distance(current_lat, current_lon, entry['latitude'], entry['longitude']) # Get the current distance to the POI in question.
        entry["distance"] = current_distance # Append the current POI's distance to it's database information.
        entry["bearing"] = calculate_bearing(current_lat, current_lon, entry["latitude"], entry["longitude"]) # Calculate the bearing to the POI.
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






debug_message("Creating `play_sound` function")
def play_sound(sound_id):
    if (str(sound_id) in config["audio"]["sounds"]): # Check to see that a sound with the specified sound ID exists in the configuration.
        if (int(config["audio"]["sounds"][str(sound_id)]["repeat"]) > 0): # Check to see if this sound effect is enabled.
            if (os.path.exists(str(config["audio"]["sounds"][str(sound_id)]["path"])) == True and str(config["audio"]["sounds"][str(sound_id)]["path"]) != ""): # Check to see if the sound file associated with the specified sound ID actually exists.
                debug_message("Playing sound " + str(sound_id))
                for i in range(0, int(config["audio"]["sounds"][str(sound_id)]["repeat"])): # Repeat the sound several times, if the configuration says to do so.
                    os.system("mpg321 " + config["audio"]["sounds"][str(sound_id)]["path"] + " > /dev/null 2>&1 &") # Play the sound file associated with this sound ID in the configuration.
                    time.sleep(float(config["audio"]["sounds"][str(sound_id)]["delay"])) # Wait before playing the sound again.
            elif (str(config["audio"]["sounds"][str(sound_id)]["path"]) == ""): # The file path associated with this sound ID is left blank, and therefore the sound can't be played.
                display_notice("The sound file path associated with sound ID (" + str(sound_id) + ") is blank.", 2)
            elif (os.path.exists(str(config["audio"]["sounds"][str(sound_id)]["path"])) == False): # The file path associated with this sound ID does not exist, and therefore the sound can't be played.
                display_notice("The sound file path associated with sound ID (" + str(sound_id) + ") does not exist.", 2)
    else: # No sound with this ID exists in the configuration database, and therefore the sound can't be played.
        display_notice("No sound with the ID (" + str(sound_id) + ") exists in the configuration.", 2)











# Define the function used to fetch aircraft data from the Dump1090 ADS-B message output. This function is also responsible for managing the raw message data itself.
debug_message("Creating `fetch_aircraft_data` function")
def fetch_aircraft_data(file):
    debug_message("Fetching aircraft data")

    if (os.path.exists(str(file)) == True): # Check to see if the filepath supplied exists before attempting to load it.
        debug_message("Reading raw ADS-B messages")

        with open(file, 'r') as read_file: # Open the ADS-B message file.
            raw_output = list(csv.reader(read_file)) # Dump the contents of the CSV file as a nested Python list.

        save_to_file(file, "", True) # After loading the file, erase its contents. This allows new messages to be saved while the data processing takes place.


        # Iterate through all received messages, and delete any that have exceeded the time-to-live threshold set in the configuration.
        debug_message("Removing expired messages")
        messages_pruned_count = 0 # This is a placeholder variable that will be incremented by 1 for each message removed. This is used for debugging purposes.
        for message in reversed(raw_output): # Iterate through each message (line) in the file, in reverse order to prevent list entries from being shuffled around during the pruning process.
            message_timestamp = round(time.mktime(datetime.datetime.strptime(message[6] + " " + message[7], "%Y/%m/%d %H:%M:%S.%f").timetuple())) # Get the timestamp of this message.
            message_age = time.time() - message_timestamp # Calculate the age of this message.
            if (message_age > config["general"]["adsb_alerts"]["message_time_to_live"]): # Check to see if this message's age is older than the time-to-live threshold set in the configuration.
                raw_output.remove(message) # Remove this message from the raw data.
                messages_pruned_count = messages_pruned_count + 1 # Increment the pruned message counter by 1.

        if (messages_pruned_count > 0): # Check to see if any messages were pruned.
            debug_message("Pruned " + str(messages_pruned_count) + " messages")

        debug_message("Generating pruned CSV data")
        new_raw_csv_string = "" # This is a placeholder string that will be appended to in the next steps.
        for line in raw_output: # Iterate through each line of the pruned CSV data.
            for entry in line: # Iterate through each field in this line.
                new_raw_csv_string = new_raw_csv_string + str(entry) + "," # Add this entry to the line.
            new_raw_csv_string = new_raw_csv_string[:-1] # Remove the last comma in the line.
            new_raw_csv_string = new_raw_csv_string + "\n" # Add a line break at the end of the last line.

        debug_message("Saving pruned CSV data")
        add_to_file(file, new_raw_csv_string, True) # Save the pruned CSV data back to the original file. The `add_to_file` function is used so that messages received during the data handling process are not overwritten and lost.



        debug_message("Collecting aircraft data")
        aircraft_data = {} # Set the aircraft data as a placeholder dictionary so information can be added to it in later steps.
        for entry in raw_output: # Iterate through each entry in the CSV list data.
            if (entry[4] in aircraft_data): # Check to see if the aircraft associated with this message already exists in the database.
                individual_data = aircraft_data[entry[4]] # If so, fetch the existing aircraft data.
            else:
                individual_data = {"latitude":"0", "longitude":"0", "altitude":"0", "speed":"0", "heading":0, "climb":"0", "callsign":"", "time":""} # Set the data for this aircraft to a fresh placeholder.

            if (entry[4] != ""): # Only fetch the identification if the message data for it isn't blank.
                individual_data["id"] = entry[4] # Get the aircraft's identification.
            if (entry[14] != ""): # Only update the latitude information if the message data for it isn't blank.
                individual_data["latitude"] = entry[14] # Get the aircraft's latitude.
            if (entry[15] != ""): # Only update the longitude information if the message data for it isn't blank.
                individual_data["longitude"] = entry[15] # Get the aircraft's longitude.
            if (entry[11] != ""): # Only update the altitude information if the message data for it isn't blank.
                individual_data["altitude"] = entry[11] # Get the aircraft's altitude.
            if (entry[12] != ""): # Only update the speed information if the message data for it isn't blank.
                individual_data["speed"] = entry[12] # Get the aircraft's ground speed.
            if (entry[13] != ""): # Only update the heading information if the message data for it isn't blank.
                try:
                    individual_data["heading"] = int(entry[13]) # Get the aircraft's compass heading.
                except:
                    individual_data["heading"] = 0 # Use a placeholder for the aircraft's heading.
            if (entry[16] != ""): # Only update the climb rate information if the message data for it isn't blank.
                individual_data["climb"] = entry[16] # Get the aircraft's vertical climb rate.
            if (entry[10] != ""): # Only update the callsign information if the message data for it isn't blank.
                individual_data["callsign"] = entry[10].strip() # Get the aircraft's callsign, removing any trailing or leading spaces.
            if (entry[6] != "" and entry[7] != ""): # Ensure the message date and time are set.
                individual_data["time"] = str(round(time.mktime(datetime.datetime.strptime(entry[6] + " " + entry[7], "%Y/%m/%d %H:%M:%S.%f").timetuple()))) # Convert the human readable timestamp into a Unix timestamp.
            else:
                display_notice("An ADS-B message didn't have an associated date and time. This should never happen.", 3)

            aircraft_data[entry[4]] = individual_data # Add the updated aircraft information back to the main database.
            
        return aircraft_data # Return the processed aircraft data.

    else: # The file supplied to load ADS-B messages from does not exist.
        display_notice("The ADS-B message file specified in the configuration does not exist. ADS-B messages can't be loaded.", 2)
        return {} # Return blank aircraft data.




debug_message("Creating `speak` function")
def speak(full_text, brief_text):
    if (config["general"]["tts"]["enabled"] == True): # Only play text-to-speech if it is enabled in the configuration.
        debug_message("Playing text-to-speech")
        if (config["general"]["tts"]["brief"] == True): # Check to see if brief mode is enabled in the configuration.
            tts.say(brief_text)
            tts.runAndWait()
        else:
            tts.say(full_text)
            tts.runAndWait()


debug_message("Creating `utc_datetime` function")
def utc_datetime(timestamp):
    timestamp = float(timestamp)
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%fZ')



debug_message("Creating `save_gpx` function")
def save_gpx(location_history, file_path):
    if (type(location_history) == list): # Check to make sure the location_history provided is a list.
        if (os.path.isdir(config["general"]["telemetry"]["directory"]) == True): # Check to make sure the save directory specified in the configuration exists and is actually a directory.
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
            file_path = config["general"]["telemetry"]["directory"] + "/" + file_name # Set up the complete file path that the telemetry information will be saved to.
            save_to_file(file_path, file_contents, True) # Save the telemetry data to a file.

    else:
        display_notice("The location history supplied to save_gpx() isn't a valid list. This is most likely a bug. Telemetry logging could not be recorded.", 2)
