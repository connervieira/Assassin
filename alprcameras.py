# Assassin

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.

import config
load_config = config.load_config

import utils
style = utils.style
debug_message = utils.debug_message
nearby_database_poi = utils.nearby_database_poi
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file
bearing_difference = utils.bearing_difference
get_distance = utils.get_distance

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.


def load_alpr_camera_database(current_location):
    if (config["general"]["alpr_alerts"]["enabled"] == True):
        if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and float(config["general"]["alpr_alerts"]["loaded_radius"]) > 0): # Check to see if ALPR camera alerts are enabled.
            debug_message("Loading ALPR camera database")


            if (str(config["general"]["alpr_alerts"]["database"]) != "" and os.path.exists(str(config["general"]["alpr_alerts"]["database"]))): # Check to see if the ALPR camera database exists.
                complete_camera_database = json.load(open(str(config["general"]["alpr_alerts"]["database"]))) # Load the ALPR database.
            else:
                complete_camera_database = {"entries": {}}  # Load a blank database of ALPR cameras, since the actual database couldn't be loaded.
                if (str(config["general"]["alpr_alerts"]["database"]) == ""): # The ALPR alert database specified in the configuration is blank.
                    display_notice("ALPR camera alerts are enabled in the configuration, but no ALPR alert database was specified.", 3)
                elif (os.path.exists(str(config["general"]["alpr_alerts"]["database"])) == False): # The ALPR alert database specified in the configuration does not exist.
                    display_notice("ALPR camera alerts are enabled in the configuration, but the ALPR database specified (" + str(config["general"]["alpr_alerts"]["database"]) + ") does not exist.", 3)
                else:
                    display_notice("An unexpected error occurred while processing the ALPR camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 3)


            loaded_camera_database = complete_camera_database.copy() # Set the database of cameras in range to the complete database as a placeholder.
            loaded_camera_database["entries"] = [] # Remove all entries from the placeholder database.

            for camera in complete_camera_database["entries"]: # Iterate through all entries in the database.
                if (get_distance(current_location[0], current_location[1], camera['lat'], camera['lon']) < float(config["general"]["alpr_alerts"]["loaded_radius"])): # Check to see if this entry is within the load radius.
                    loaded_camera_database["entries"].append(camera) # Add this entry to the database of cameras that are within range.

            debug_message("Loaded " + str(len(loaded_camera_database["entries"])) + " entries from ALPR camera database")
            return loaded_camera_database # Return the loaded database information.

        else: # ALPR camera alerts are disabled in the configuration.
            display_notice("ALPR alerts are enabled in the configuration, but another configuration value caused them to be disabled.", 2)
            return {} # Return a blank placeholder database in place of the loaded ALPR camera database.
    else: # ALPR camera alerts are disabled in the configuration.
        return {} # Return a blank placeholder database in place of the loaded ALPR camera database.



def alpr_camera_alert_processing(current_location, loaded_alpr_camera_database):
    if (config["general"]["alpr_alerts"]["enabled"] == True):
        if (os.path.exists(config["general"]["alpr_alerts"]["database"]) == True and config["general"]["alpr_alerts"]["database"] != "" and config["general"]["gps"]["enabled"] == True): # Check to see if a valid ALPR database has been configured.
            debug_message("Processing ALPR camera alerts")
            nearby_alpr_cameras = nearby_database_poi(current_location, loaded_alpr_camera_database, float(config["general"]["alpr_alerts"]["alert_range"])) # Get nearby entries from this POI database.

            # Remove false alerts in the nearby ALPR cameras list.
            filtered_cameras = [] # This is a placeholder list that will receive all of the cameras that pass the filtering process.
            for camera in nearby_alpr_cameras:
                camera["direction"] = camera["bearing"] - current_location[4]
                if (bearing_difference(current_location[4], float(camera["facing"])) < float(config["general"]["alpr_alerts"]["filters"]["angle_threshold"])): # Check to make sure the camera's relative bearing is inside the threshold.
                    if (bearing_difference(current_location[4], float(camera["bearing"])) < float(config["general"]["alpr_alerts"]["filters"]["direction_threshold"])): # Check to make sure the relative facing to this camera is within the threshold.
                        filtered_cameras.append(camera) # Add this camera to the filtered list.

            deduplicated_cameras = filtered_cameras.copy()
            if (config["general"]["alpr_alerts"]["filters"]["duplicate_filtering"]["enabled"] == True): # Check to see if duplicate alert filtering is enabled.
                for base_camera in filtered_cameras: # Iterate through each camera in the list of filtered cameras.
                    duplicate_camera = False # For each base camera, reset the duplicate camera flag to false before the search for any duplicate cameras.
                    for compared_camera in filtered_cameras: # Once again, iterate through each camera in the list of filtered cameras.
                        if (base_camera != compared_camera): # Check to make sure we aren't comparing a given camera to itself.
                            if (get_distance(base_camera["lat"], base_camera["lon"], compared_camera["lat"], compared_camera["lon"]) <= config["general"]["alpr_alerts"]["filters"]["duplicate_filtering"]["distance"]): # Check to see if these two cameras are within the distance threshold of each-other.
                                if (bearing_difference(base_camera["facing"], base_camera["facing"]) <= config["general"]["alpr_alerts"]["filters"]["duplicate_filtering"]["angle"]): # Check to see if these two cameras are within the distance threshold of each-other.
                                    duplicate_camera = True # Indicate that a duplicate was found for this base camera.
                                    break # Exit the loop, since it doesn't matter if any more cameras are considered duplicates with this one; The camera is already set to be removed.
                    if (duplicate_camera == True):
                        deduplicated_cameras.remove(base_camera) # Add this camera to the list of de-duplicated cameras, since it is not a duplicate.


            # Sort the ALPR cameras list by distance.
            sorted_cameras = [] # This is a placeholder list that will receive the cameras as they are sorted.
            for i in range(0, len(deduplicated_cameras)): # Run once for every entry in the list of nearby ALPR cameras.
                current_closest = {"distance": 100000000000} # Set the current closest camera to placeholder data with an extremely far distance.
                for element in deduplicated_cameras:
                    if (element["distance"] < current_closest["distance"]): # Check to see if the distance to this camera is shorter than the current known closest camera.
                        current_closest = element # Set this camera to the current closest known camera.
                sorted_cameras.append(current_closest) # Add the closest camera from this cycle to the list.
                deduplicated_cameras.remove(current_closest) # After adding it to the sorted list, remove it from the original list.


            # Finally, places the alerts into the dictionary to pass back to the main process:
            alpr_alerts = {}
            for element in sorted_cameras:
                alpr_alerts[str(hash(str(element["lat"]) + str(element["lon"])))] = element

            debug_message("Processed ALPR camera alerts")
            return alpr_alerts

        else: # ALPR camera alerts are disabled.
            return {"distance": 1000000000.0}, {} # Return a blank placeholder in place of the nearest ALPR camera.
    else: # ALPR camera alerts are disabled.
        return {"distance": 1000000000.0}, {} # Return a blank placeholder in place of the nearest ALPR camera.
