# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




import os # Required to interact with certain operating system functions
import json # Required to process JSON data

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

import config
load_config = config.load_config

import utils
style = utils.style
debug_message = utils.debug_message
display_notice = utils.display_notice
get_distance = utils.get_distance
process_timing = utils.process_timing # Load the function used to track how much time is spent doing various actions.


# Locate and load the configuration file.
config = load_config()
debug_message("Importing `minidom` library")
from xml.dom import minidom # Required for processing GPX data
debug_message("Importing `math` library")
import math # Required to run more complex math calculations
debug_message("Importing `numpy` library")
import numpy # Required to run more complex math calculations

import obdintegration



gps_enabled = config["general"]["gps"]["enabled"] # This setting determines whether or not Assassin's GPS features are enabled.

if (gps_enabled == True and config["general"]["gps"]["provider"] == "gpsd"): # Only import the GPS libraries if GPS is enabled in the configuration, and the GPSD provider is selected.
    debug_message("Importing `gps` library")
    from gps import * # Required to access GPS information.
    debug_message("Importing `gpsd` library")
    import gpsd # Required to access GPS information.




def calculate_speed(location_history, gps_speed, obd_connection):
    speed = 0 # This is a placeholder that will be replaced with the actual speed.
    if (config["general"]["gps"]["speed_source"] == "calculated"): # The configuration indicates that the speed should be calculated based on distance and time.
        if (len(location_history) >= 2):
            distance = get_distance(location_history[-1]["lat"], location_history[-1]["lon"], location_history[-2]["lat"], location_history[-2]["lon"]) # Get the distance between the two points.
            time_difference = abs(location_history[-1]["time"] - location_history[-2]["time"]) # Get the time difference between the two points.
            miles_per_second = distance / time_difference
            speed = miles_per_second * 1609.344
        else:
            speed = 0
    elif (config["general"]["gps"]["speed_source"] == "gps"):
        speed = gps_speed
    elif (config["general"]["gps"]["speed_source"] == "obd"):
        speed = obdintegration.fetch_obd_speed(obd_connection)
    else: # This will only happen when the configuration is invalid.
        speed = 0

    return speed


# Define the function that will be used to get the current GPS coordinates.
debug_message("Creating `get_gps_location` function")
def get_gps_location(location_history=[], obd_connection=None):
    debug_message("Getting GPS location")
    process_timing("GPS Location", "start")
    if (gps_enabled == True): # Check to see if GPS is enabled.
        if (config["general"]["gps"]["demo_mode"]["enabled"] == True): # Check to see if GPS demo mode is enabled in the configuration.
            debug_message("Returning demo GPS information")
            speed = calculate_speed(location_history, config["general"]["gps"]["demo_mode"]["data"]["speed"], obd_connection)
            current_location = [float(config["general"]["gps"]["demo_mode"]["data"]["longitude"]), float(config["general"]["gps"]["demo_mode"]["data"]["latitude"]), speed, float(config["general"]["gps"]["demo_mode"]["data"]["altitude"]), float(config["general"]["gps"]["demo_mode"]["data"]["heading"]), int(config["general"]["gps"]["demo_mode"]["data"]["satellites"]), "V0LT Assassin - GPS demo mode"] # Return the sample GPS information defined in the configuration.
        else: # GPS demo mode is disabled, so attempt to get the actual GPS data from GPSD.
            if (config["general"]["gps"]["provider"] == "gpsd"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Connecting to GPSD")
                    gpsd.connect() # Connect to the GPS daemon.
                    debug_message("Fetching GPSD information")
                    gps_data_packet = gpsd.get_current() # Get the current information.
                    debug_message("Received GPSD information")
                    speed = calculate_speed(location_history, gps_data_packet.speed())
                    current_location = gps_data_packet.position()[0], gps_data_packet.position()[1], speed, gps_data_packet.altitude(), gps_data_packet.movement()["track"], gps_data_packet.sats, "V0LT Assassin - GPSD Device" # Return GPS information.
                except: # If the current location can't be established, then return placeholder location data.
                    current_location = [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            elif (config["general"]["gps"]["provider"] == "termux"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Fetching termux-location information")
                    raw_termux_response = str(os.popen("termux-location").read()) # Execute the Termux location command.
                    termux_response = json.loads(raw_termux_response) # Load the location information from the Termux response.
                    debug_message("Received termux-location information")
                    speed = calculate_speed(location_history, termux_response["speed"])
                    current_location = [termux_response["latitude"], termux_response["longitude"], speed, termux_response["altitude"], termux_response["bearing"], 0, "V0LT Assassin - Termux-API"] # Return the fetched GPS information.
                except:
                    current_location = [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            elif (config["general"]["gps"]["provider"] == "locateme"):
                try: # Don't terminate the entire script if the GPS location fails to be aquired.
                    debug_message("Fetching LocateMe information")
                    raw_locateme_response = str(os.popen("locateme -f {LAT},{LON},{SPD},{ALT},{DIR},0").read()) # Execute the LocateMe location command.
                    locateme_response = raw_locateme_response.split(",") # Load the location information from the LocateMe response.
                    locateme_respose.append("V0LT Assassin - MacOS Location Services via LocateMe") # Append the location provider to the information.
                    debug_message("Received LocateMe information")
                    speed = calculate_speed(location_history, locateme_response[2])
                    current_location = float(locateme_response[0]), float(locateme_response[1]), speed, float(locateme_response[3]), float(locateme_response[4]), 0 # Return the fetched GPS information.
                except:
                    current_location = [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                    debug_message("GPS fetch failed")
            else:
                current_location = [0.0000, -0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
                debug_message("Invalid location provider")
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        current_location = [0.0000, 0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Return a default placeholder location.
        debug_message("GPS is disabled")

    process_timing("GPS Location", "end")
    return current_location



# This function is used to detect GPS problems.
debug_message("Creating `process_gps_alerts` function")
def process_gps_alerts(location_history):
    gps_alerts = {}

    if (config["general"]["gps"]["alerts"]["enabled"] == True): # Check to make sure GPS alerts are enabled before processing alerts.
        debug_message("Processing GPS alerts")
        if (type(location_history) == list): # Check to make sure the location history provided is actually a list.
            reversed_location_history = list(reversed(list(location_history))) # Reverse the location history list.
            location_history = reversed_location_history[:int(config["general"]["gps"]["alerts"]["look_back"])] # Remove all but the first elements in the location history.
            location_history = list(reversed(list(location_history))) # Return the location history to chronological order.


            sequential_no_data = 0 # This is a placeholder that will count the number of sequential instances of no data being returned by GPS requests.
            sequential_identical = 0 # This is a placeholder that will count the number of sequential instances of identical data being returned by multiple GPS requests.
            for i in range(0, len(location_history) - 1): # Iterate through each element in the list, minus 1.

                # Process overspeed alerts.
                if (config["general"]["gps"]["alerts"]["overspeed"]["enabled"] == True):
                    if (location_history[i]["lat"] != 0.0 and location_history[i]["lon"] != 0.0 and location_history[i+1]["lat"] != 0.0 and location_history[i+1]["lon"] != 0.0): # Only run speed alert processing if both location points are defined.
                        distance = get_distance(location_history[i]["lat"], location_history[i]["lon"], location_history[i+1]["lat"], location_history[i+1]["lon"]) # Get the distance between the two points.
                        time_difference = abs(location_history[i]["time"] - location_history[i+1]["time"]) # Get the time difference between the two points.
                        miles_per_second = distance / time_difference
                        miles_per_hour = 60 * 60 * miles_per_second
                        if (miles_per_hour >= float(config["general"]["gps"]["alerts"]["overspeed"]["max_speed"])): # Check to see if the calculated GPS speed is excessively high.
                            if (config["general"]["gps"]["alerts"]["overspeed"]["prioritize_highest"] == True): # Check to see if the configuration value to prioritize the highest speed is enabled.
                                if ("maxspeed" in gps_alerts and "active" in gps_alerts["maxspeed"] and gps_alerts["maxspeed"]["active"] == True): # Check to see if there is already a GPS overspeed alert active.
                                    if (gps_alerts["maxspeed"]["speed"] <= gps_alerts["maxspeed"]["speed"]): # Only overwrite the max-speed alert if this alert is a higher speed.
                                        gps_alerts["maxspeed"] = {}
                                        gps_alerts["maxspeed"]["active"] = True
                                        gps_alerts["maxspeed"]["speed"] = miles_per_hour
                                else: # There is no active overspeed alert.
                                    gps_alerts["maxspeed"] = {}
                                    gps_alerts["maxspeed"]["active"] = True
                                    gps_alerts["maxspeed"]["speed"] = miles_per_hour
                            else: # The configuration value to prioritize the highest speed is disabled.
                                gps_alerts["maxspeed"] = {}
                                gps_alerts["maxspeed"]["active"] = True
                                gps_alerts["maxspeed"]["speed"] = miles_per_hour


                # Process no-data alerts.
                if (config["general"]["gps"]["alerts"]["no_data"]["enabled"] == True): # Only detect 'no data' alerts if they are enabled in the configuration.
                    if (float(location_history[i+1]["lat"]) == 0.0 and float(location_history[i+1]["lon"]) == 0.0 and float(location_history[i+1]["spd"]) == 0.0 and float(location_history[i+1]["alt"]) == 0.0): # Check to see if there is no GPS data.
                        sequential_no_data = sequential_no_data + 1 # Increment the sequential no-data instance counter.
                    else:
                        sequential_no_data = 0 # Reset the sequential no-data instance counter.

                    if (sequential_no_data >= config["general"]["gps"]["alerts"]["no_data"]["length"]): # Check to see if the number of sequential no-data occurrances is greater than or equal to the trigger.
                        gps_alerts["nodata"] = {}
                        gps_alerts["nodata"]["active"] = True


                # Process frozen data alerts.
                if (config["general"]["gps"]["alerts"]["frozen"]["enabled"] == True): # Only detect 'frozen data' alerts if they are enabled in the configuration.
                    if (float(location_history[i]["lat"]) == float(location_history[i+1]["lat"]) and float(location_history[i]["lon"]) == float(location_history[i+1]["lon"]) and float(location_history[i]["spd"]) == float(location_history[i+1]["spd"]) and float(location_history[i]["alt"]) == float(location_history[i+1]["alt"])): # Check to see if these two entries in the location history are identical.
                        sequential_identical = sequential_identical + 1 # Increment the sequential identical-data instance counter.
                    else:
                        sequential_identical = 0 # Reset the sequential identical-data instance counter.

                    if (sequential_identical >= config["general"]["gps"]["alerts"]["frozen"]["length"]): # Check to see if the number of sequential identical data occurrances is greater than or equal to the trigger.
                        gps_alerts["frozen"] = {}
                        gps_alerts["frozen"]["active"] = True


                # Process frozen data alerts.
                if (config["general"]["gps"]["alerts"]["diagnostic"]["enabled"] == True): # Only issue diagnostic alerts if they are enabled in the configuration.
                    gps_alerts["diagnostic"] = location_history[-1]

        debug_message("Processed GPS alerts")

    return gps_alerts
