# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




import os # Required to use certain operating system functions.
import json # Required to process JSON data.
import time # Required to handle time information and execute delays.
import bluetooth # Required to interface with Bluetooth adapters.
import threading # Required to manage background threads.

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file
get_distance = utils.get_distance

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = load_config() # Load and load the configuration file.


def load_bluetooth_log_file():
    # Load the Bluetooth device log file, if applicable.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["bluetooth_monitoring"]["log_devices"]["enabled"] == True): # Check to see if Bluetooth device logging is enabled.
        debug_message("Loading Bluetooth log file")
        if (os.path.exists(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"])):
            detected_bluetooth_devices = json.load(open(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"])) # Load the data from the Bluetooth device log file.
        else:
            detected_bluetooth_devices = {} # Set the Bluetooth device log to a blank placeholder list.

        debug_message("Loaded Bluetooth log file")

        return detected_bluetooth_devices # Return the detected Bluetooth device dictionary.

    else: # Bluetooth monitoring and/or logging is turned off.
        return {} # Return a blank placeholder dictionary in place of the device history.



def scan_bluetooth():
    debug_message("Scanning for Bluetooth devices")
    try:
        devices = bluetooth.discover_devices(int(config["general"]["bluetooth_monitoring"]["scan_time"]), lookup_names = True) # Scan for nearby Bluetooth devices for the amount of time specified in the configuration.
    except:
        display_notice("Couldn't detect nearby Bluetooth devices due to an unknown problem.", 2) # Display a warning that Bluetooth devices could not be detected.
        devices = {}  # Set the nearby Bluetooth device list to an empty placeholder, since Bluetooth devices could not be detected.

    debug_message("Detected " + str(len(devices)) + " Bluetooth devices")
    return devices


nearby_bluetooth_devices = {}
def bluetooth_scan_cycle():
    global nearby_bluetooth_devices
    while True:
        nearby_bluetooth_devices = scan_bluetooth()


def start_bluetooth_scanning():
    bluetooth_scan_thread = threading.Thread(target=bluetooth_scan_cycle, name="BluetoothScanThread")
    bluetooth_scan_thread.start()



def bluetooth_alert_processing(current_location, detected_bluetooth_devices):
    if (config["general"]["gps"]["enabled"] == False): # Check to see if GPS functionality is enabled. If this is the case, Assassin won't be able to detect when Bluetooth devices are following, but blacklist alerts will still work.
        current_location = [0.0000, 0.0000, 0.0, 0.0, 0.0, 0] # Set the current location information to a dummy placeholder.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only conduct Bluetooth alert processing if Bluetooth alerts are enabled in the configuration.
        global nearby_bluetooth_devices
        debug_message("Processing Bluetooth alerts")

        for address, name in nearby_bluetooth_devices:
            if (address in detected_bluetooth_devices): # This device has been seen before, so update it's existing dictionary entry.
                detected_bluetooth_devices[address]["lastseenlocation"] = current_location
                detected_bluetooth_devices[address]["lastseentime"] = round(time.time())
            else: # This device has not been seen before, so add it to the dictionary.
                detected_bluetooth_devices[address] = {
                    "name": str(name),
                    "firstseenlocation": current_location, # This is the first GPS location that this device was detected at. This will not be updated upon subsequent detections.
                    "lastseenlocation": current_location, # This is the most recent GPS location that this device was detected at. This will be updated upon subsequent detections.
                    "firstseentime": round(time.time()), # This is the first time that this device was detected at. This will not be updated upon subsequent detections.
                    "lastseentime": round(time.time()), # This is the most recent time that this device was detected at. This will be updated upon subsequent detections.
                    "whitelist": address in config["general"]["bluetooth_monitoring"]["whitelist"]["devices"], # Check to see if this device address is in the whitelist specified in the configuration.
                    "blacklist": address in config["general"]["bluetooth_monitoring"]["blacklist"]["devices"] # Check to see if this device address is in the blacklist specified in the configuration.
                }

            if (config["general"]["bluetooth_monitoring"]["log_devices"]["enabled"] == True): # Check to see if Bluetooth device logging is enabled.
                save_to_file(assassin_root_directory + "/" + config["general"]["bluetooth_monitoring"]["log_devices"]["filename"], json.dumps(detected_bluetooth_devices), True) # Save the Bluetooth device history to disk.



        # Determine which Bluetooth devices meet the alert criteria, and add them to a list of Bluetooth threats.
        bluetooth_threats = [] # Set the Bluetooth threats list to an empty placeholder.
        for address in detected_bluetooth_devices: # Iterate through all detected Bluetooth devices.
            device = detected_bluetooth_devices[address] # Grab the data for the device of this iteration cycle.
            device["address"] = address # Add this device's hardware address to its information.
            device["distance_followed"] = get_distance(device["firstseenlocation"][0], device["firstseenlocation"][1], device["lastseenlocation"][0], device["lastseenlocation"][1]) # Calculate the distance that this device has been following Assassin by determining the distance between the first detected location and the last detected location.
            if ((device["distance_followed"] >= float(config["general"]["bluetooth_monitoring"]["minimum_following_distance"]) and address not in config["general"]["bluetooth_monitoring"]["whitelist"]["devices"]) or address in config["general"]["bluetooth_monitoring"]["blacklist"]["devices"]): # Check to see if the distance this device has followed Assassin is greater than or equal to the threshold set in the configuration for alerting. Also check to make sure this device is not in the whitelist. If this device is in the blacklist, the alert regardless of other conditions.
                bluetooth_threats.append(device) # Add this device to the list of active Bluetooth threats.



        debug_message("Processed Bluetooth alerts")
        return detected_bluetooth_devices, bluetooth_threats

    else: # Bluetooth alerts are disabled.
        return {} # Return an empty placeholder dictionary in place of the database of detected Bluetooth devices.


