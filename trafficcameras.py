import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
load_traffic_cameras = utils.load_traffic_cameras
get_gps_location = utils.get_gps_location
convert_speed = utils.convert_speed
nearby_traffic_cameras = utils.nearby_traffic_cameras
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.



def load_traffic_camera_database():
    if (float(config["general"]["alert_range"]["traffic_cameras"]) > 0 and config["general"]["gps_enabled"] and float(config["general"]["traffic_camera_loaded_radius"] > 0): # Check to see if traffic camera alerts are enabled, and the GPS is enabled.
        debug_message("Loading traffic enforcement camera database")
        current_location = [0, 0] # Set the "current location" to a placeholder.
        previous_gps_attempt = False # This variable will be changed to `True` if the GPS fails to get a lock at least once. This variable is responsible for triggering a delay to allow the GPS to get a lock.
        while (current_location[0] == 0 and current_location[1] == 0): # Repeatedly attempt to get a GPS location until one is received.
            if (previous_gps_attempt == True): # If the GPS previously failed to get a lock, then wait 2 seconds before trying again.
                time.sleep(2) # Wait 2 seconds to give the GPS time to get a lock.

            previous_gps_attempt = True
            current_location = get_gps_location() # Attempt to get the current GPS location.

        if (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == True): # Check to see that the traffic camera database exists at the path specified in the configuration.
            loaded_traffic_camera_database = load_traffic_cameras(current_location[0], current_location[1], config["general"]["alert_databases"]["traffic_cameras"], float(config["general"]["traffic_camera_loaded_radius"])) # Load all traffic cameras within the configured loading radius.
        else: # Traffic enforcement camera alerts are enabled, but the traffic enforcement camera database doesn't exist, so print a warning message.
            loaded_traffic_camera_database = [] # Load a blank list of traffic cameras.
            if (str(config["general"]["alert_databases"]["traffic_cameras"]) == ""): # The traffic enforcement camera alert database specified in the configuration is blank.
                display_notice("Traffic enforcement camera alerts are enabled in the configuration, but no traffic camera database was specified.", 2)
            elif (os.path.exists(str(config["general"]["alert_databases"]["traffic_cameras"])) == False): # The traffic camera alert database specified in the configuration does not exist.
                display_notice("Traffic enforcement camera alerts are enabled in the configuration, but the traffic camera database specified (" + str(config["general"]["alert_databases"]["traffic_cameras"]) + ") does not exist.", 2)
            else:
                display_notice("An unexpected error occurred while processing the traffic enforcement camera database. This error should never occur, so you should contact the developers to help resolve the issue.", 3)
        debug_message("Loaded traffic enforcement camera database")
        return loaded_traffic_camera_database

    else: # Traffic camera alerts are disabled.
        return [] # Return a blank placeholder list in place of the loaded traffic camera database.



def traffic_camera_alert_processing(current_location, loaded_traffic_camera_database):
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
            for camera in nearby_redlight_cameras: # Iterate through all nearby red-light cameras.
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
            nearest_enforcement_camera = nearest_misc_camera # Set the overall nearest camera to the nearest miscellaneous camera.
        else:
            nearest_enforcement_camera = {"dst": 1000000000.0, "lat": 0.0, "lon": 0.0, "spd": 0, "str": ""} # Set the nearest overall enforcement camera to a blank placeholder.

        if (config["general"]["traffic_camera_speed_check"] == True and "nearest_enforcement_camera" in locals()): # Check to see if the traffic camera speed check setting is enabled in the configuration, and that a speed camera is actually within the alert radius at all.
            if (nearest_enforcement_camera["spd"] != None): # Check to see if the nearest speed camera has speed limit data associated with it.
                if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then enable a heightened alert.
                    active_alarm = "speedcameralimitexceeded" # Set an active alarm indicating that the speed camera speed limit has been exceeded.

        debug_message("Processed traffic enforcement camera alerts")
        return nearest_enforcement_camera, nearest_speed_camera, nearest_redlight_camera, nearest_misc_camera # Return the nearest cameras of each type.


    else: # Traffic enforcement camera alert processing is disabled, so return blank placeholder information.
        return {}, {}, {}, {}
