import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
get_gps_location = utils.get_gps_location
nearby_database_poi = utils.nearby_database_poi
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file
bearing_difference = utils.bearing_difference

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.


def load_alpr_camera_database():
    if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0): # Check to see if ALPR camera alerts are enabled.
        debug_message("Loading ALPR camera database")
        if (str(config["general"]["alpr_alerts"]["database"]) != "" and os.path.exists(str(config["general"]["alpr_alerts"]["database"]))): # Check to see if the ALPR camera database exists.
            loaded_alpr_camera_database = json.load(open(str(config["general"]["alpr_alerts"]["database"]))) # Load the ALPR database.
        else:
            loaded_alpr_camera_database = {} # Load a blank database of ALPR cameras, since the actual database couldn't be loaded.
            if (str(config["general"]["alpr_alerts"]["database"]) == ""): # The ALPR alert database specified in the configuration is blank.
                display_notice("ALPR camera alerts are enabled in the configuration, but no ALPR alert database was specified.", 2)
            elif (os.path.exists(str(config["general"]["alpr_alerts"]["database"])) == False): # The ALPR alert database specified in the configuration does not exist.
                display_notice("ALPR camera alerts are enabled in the configuration, but the ALPR database specified (" + str(config["general"]["alpr_alerts"]["database"]) + ") does not exist.", 2)
            else:
                display_notice("An unexpected error occurred while processing the ALPR camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 2)

        debug_message("Loaded ALPR camera database")
        return loaded_alpr_camera_database # Return the loaded database information.

    else: # ALPR camera alerts are disabled in the configuration.
        return {} # Return a blank placeholder database in place of the loaded ALPR camera database.



def alpr_camera_alert_processing(current_location, loaded_alpr_camera_database):
    if (os.path.exists(config["general"]["alpr_alerts"]["database"]) == True and config["general"]["alpr_alerts"]["database"] != "" and config["general"]["gps_enabled"] == True): # Check to see if a valid ALPR database has been configured.
        debug_message("Processing ALPR camera alerts")
        nearby_alpr_cameras = nearby_database_poi(current_location, loaded_alpr_camera_database, float(config["general"]["alpr_alerts"]["alert_range"])) # Get nearby entries from this POI database.

        # Remove false alerts in the nearby ALPR cameras list.
        filtered_cameras = [] # This is a placeholder list that will receive all of the cameras that pass the filtering process.
        for camera in nearby_alpr_cameras:
            if (bearing_difference(0, float(camera["relativefacing"])) < float(config["general"]["alpr_alerts"]["angle_threshold"])): # Check to make sure the camera's relative bearing is inside the threshold.
                if (bearing_difference(0, float(camera["bearing"]) - current_location[4]) < float(config["general"]["alpr_alerts"]["direction_threshold"])): # Check to make sure the relative direction to this camera is within the threshold.
                    filtered_cameras.append(camera) # Add this camera to the filtered list.

        nearest_alpr_camera = {"distance": 1000000000.0}

        for entry in filtered_cameras: # Iterate through all nearby ALPR cameras.
            if (entry["distance"] < nearest_alpr_camera["distance"]): # Check to see if the distance to this camera is lower than the current closest camera.
                nearest_alpr_camera = entry # Make the current camera the new closest camera.

        debug_message("Processed ALPR camera alerts")
        return nearest_alpr_camera, filtered_cameras

    else: # ALPR camera alerts are diabled.
        return {"distance": 1000000000.0}, {} # Return a blank placeholder in place of the nearest ALPR camera.
