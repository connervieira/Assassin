# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
load_traffic_cameras = utils.load_traffic_cameras
convert_speed = utils.convert_speed
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file
get_distance = utils.get_distance
calculate_bearing = utils.calculate_bearing

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.



def load_traffic_camera_database(current_location):
    if (float(config["general"]["traffic_camera_alerts"]["alert_range"]) > 0 and config["general"]["gps"]["enabled"] and float(config["general"]["traffic_camera_alerts"]["loaded_radius"]) > 0): # Check to see if traffic camera alerts are enabled, and the GPS is enabled.
        debug_message("Loading traffic enforcement camera database")

        if (os.path.exists(str(config["general"]["traffic_camera_alerts"]["database"])) == True): # Check to see that the traffic camera database exists at the path specified in the configuration.
            loaded_traffic_camera_database = load_traffic_cameras(current_location[0], current_location[1], config["general"]["traffic_camera_alerts"]["database"], float(config["general"]["traffic_camera_alerts"]["loaded_radius"])) # Load all traffic cameras within the configured loading radius.
        else: # Traffic enforcement camera alerts are enabled, but the traffic enforcement camera database doesn't exist, so print a warning message.
            loaded_traffic_camera_database = [] # Load a blank list of traffic cameras.
            if (str(config["general"]["traffic_camera_alerts"]["database"]) == ""): # The traffic enforcement camera alert database specified in the configuration is blank.
                display_notice("Traffic enforcement camera alerts are enabled in the configuration, but no traffic camera database was specified.", 2)
            elif (os.path.exists(str(config["general"]["traffic_camera_alerts"]["database"])) == False): # The traffic camera alert database specified in the configuration does not exist.
                display_notice("Traffic enforcement camera alerts are enabled in the configuration, but the traffic camera database specified (" + str(config["general"]["traffic_camera_alerts"]["database"]) + ") does not exist.", 2)
            else:
                display_notice("An unexpected error occurred while processing the traffic enforcement camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 3)
        debug_message("Loaded traffic enforcement camera database")
        return loaded_traffic_camera_database

    else: # Traffic camera alerts are disabled.
        return [] # Return a blank placeholder list in place of the loaded traffic camera database.




# Define the function that will be used to get nearby speed, red light, and traffic cameras from a loaded database.
debug_message("Creating `nearby_traffic_cameras` function")
def nearby_traffic_cameras(current_lat, current_lon, database_information, radius=1.0): # This function is used to get a list of all traffic enforcement cameras within a certain range of a given location.
    nearby_cameras = [] # Create empty an placeholder list for the nearby cameras.

    if (len(database_information) > 0): # Check to see if the supplied database information has data in it.
        camera_id = 0 # This will be incremented up by 1 for each camera iterated through in the database.
        for camera in database_information: # Iterate through each camera in the loaded database.
            camera_id = camera_id + 1
            camera["id"] = camera_id
            current_distance = get_distance(current_lat, current_lon, camera['lat'], camera['lon'])
            if (current_distance < float(radius)): # Only show the camera if it's within a certain radius of the current location.
                camera["dst"] = current_distance # Save the current distance from this camera to it's data before adding it to the list of nearby speed cameras.
                camera["bearing"] = calculate_bearing(current_lat, current_lon, camera["lat"], camera["lon"])
                camera["flags"] = str("{0:012b}".format(camera["flg"]))[::-1] # Convert the flag integer into a binary bitmask.
                if (camera["flags"][0] == "1" or camera["flags"][2] == "1" or camera["flags"][3] == "1"): # Check to see if this particular camera is speed related.
                    camera["type"] = "speed"
                elif (camera["flags"][1] == "1"): # Check to see if this particular camera is red-light related.
                    camera["type"] = "redlight"
                else:
                    camera["type"] = "misc"

                if (config["general"]["traffic_camera_alerts"]["enabled_types"][camera["type"]] == True): # Check to see if this camera type is enabled in the configuration.
                    nearby_cameras.append(camera) # Add this camera to the nearby camera list.

    else: # The supplied database information was empty.
        pass

    return nearby_cameras # Return the list of nearby cameras.





def traffic_camera_alert_processing(current_location, loaded_traffic_camera_database):
    if (config["general"]["gps"]["enabled"] == True and float(config["general"]["traffic_camera_alerts"]["alert_range"]) > 0): # Check to see if the speed camera display is enabled in the configuration.
        debug_message("Processing traffic enforcement camera alerts")
        # Create placeholders for each camera type so we can add the closet camera for each category in the next step .
        nearest_camera = {"dst": 10000000.0}

        nearby_cameras = nearby_traffic_cameras(current_location[0], current_location[1], loaded_traffic_camera_database, float(config["general"]["traffic_camera_alerts"]["alert_range"])) # Get all traffic cameras within the configured radius.

        for camera in nearby_cameras: # Iterate through all nearby cameras.
            camera["direction"] = camera["bearing"] - current_location[4] # Calculate the direction to this camera, relative to the current direction of movement.
            if (camera["dst"] < nearest_camera["dst"]): # Check to see if the distance to this camera is lower than the current closest camera.
                nearest_camera = camera # Make the current camera the new closest camera.

        # Sort the cameras list by distance.
        sorted_cameras = [] # This is a placeholder list that will receive the cameras as they are sorted.
        for i in range(0, len(nearby_cameras)): # Run once for every entry in the list of nearby cameras.
            current_closest = {"dst": 100000000000} # Set the current closest camera to placeholder data with an extremely far distance.
            for element in nearby_cameras:
                if (element["dst"] < current_closest["dst"]): # Check to see if the distance to this camera is closer than the current known closest camera.
                    current_closest = element # Set this camera to the current closest known camera .
            sorted_cameras.append(current_closest) # Add the closest camera from this cycle to the list.
            nearby_cameras.remove(current_closest) # After adding it to the sorted list, remove it from the original list.
        nearby_cameras = sorted_cameras # Set the original list of cameras to the sorted list.

        debug_message("Processed traffic enforcement camera alerts")
        return nearest_camera, nearby_cameras # Return the nearby cameras.


    else: # Traffic enforcement camera alert processing is disabled, so return blank placeholder information to avoid errors.
        return {}, []
