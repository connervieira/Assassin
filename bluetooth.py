# Assassin

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os
import time
import re


import config
load_config = config.load_config

import utils
style = utils.style
debug_message = utils.debug_message
get_distance = utils.get_distance
calculate_bearing = utils.calculate_bearing
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file

import subprocess

import threading

# Locate and load the configuration file.
config = load_config()


bluetooth_le_scan_queue = []
def scan_bluetooth_le(): # This function scans for Bluetooth LE devices, and dumps all detected devices to a queue.
    global bluetooth_le_scan_queue
    global config
    scan_command = "sudo hcitool lescan --duplicates"
    proc = subprocess.Popen(scan_command.split(" "), stdout=subprocess.PIPE)
    while True: # Run forever, until the sub process terminates.
        line = proc.stdout.readline()
        if not line:
            display_notice("The Bluetooth LE scan process has closed. Bluetooth LE devices are no longer being detected.", 2)
            break
        bluetooth_le_scan_queue.append(line.decode('utf-8').rstrip()) # Add this line to the queue to be processed.
        time.sleep(0.001) # Wait briefly


def start_bluetooth_scanning(): # This function initializes the Bluetooth scanning system.
    # Validate Bluetooth configuration values
    for entry in config["general"]["bluetooth_scanning"]["blacklist"]:
        if (entry != entry.upper()):
            display_notice("One or more entries in the Bluetooth blacklist contain lowercase letters. These entries will never be triggered.", 2)
    for entry in config["general"]["bluetooth_scanning"]["whitelist"]:
        if (entry != entry.upper()):
            display_notice("One or more entries in the Bluetooth whitelist contain lowercase letters. These entries will be ignored.", 2)

    # Start the Bluetooth scanning process in the background.
    bluetooth_le_scan_thread = threading.Thread(target=scan_bluetooth_le, name="BluetoothLEScan")
    bluetooth_le_scan_thread.start()


def get_latest_bluetooth_le(): # This function returns the devices from the queue.
    global bluetooth_le_scan_queue

    devices = {}
    for x in range(0, len(bluetooth_le_scan_queue)):
        current_line = bluetooth_le_scan_queue.pop().split(" ")
        if (len(current_line) == 2):
            if (re.match("[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$", current_line[0].upper())): # Check to see if the first element in this line is a MAC address.
                devices[current_line[0]] = {} # Create an entry for this device, using its MAC address as the key.
                devices[current_line[0]]["name"] = current_line[1]

    return devices


bluetooth_device_data = {}
def process_bluetooth_alerts(devices, current_position):
    global bluetooth_device_data
    for device in devices:
        if (device in bluetooth_device_data): # Check to see if this device does not yet exist in the complete device data.
            if (time.time() - bluetooth_device_data[device]["seen"]["original"]["time"] > config["general"]["bluetooth_scanning"]["latch_time"] * 60): # Check to see if it has been at least a certain number of minutes since this device was seen.
                bluetooth_device_data[device]["seen"]["first"]["time"] = time.time()
                bluetooth_device_data[device]["seen"]["first"]["pos"] = [current_position[0], current_position[1]]
            bluetooth_device_data[device]["seen"]["last"]["time"] = time.time()
            bluetooth_device_data[device]["seen"]["last"]["pos"] = [current_position[0], current_position[1]]
        else:
            bluetooth_device_data[device] = {}
            bluetooth_device_data[device]["seen"] = {}
            bluetooth_device_data[device]["seen"]["original"] = {}
            bluetooth_device_data[device]["seen"]["original"]["time"] = time.time()
            bluetooth_device_data[device]["seen"]["original"]["pos"] = [current_position[0], current_position[1]]
            bluetooth_device_data[device]["seen"]["first"] = {}
            bluetooth_device_data[device]["seen"]["first"]["time"] = time.time()
            bluetooth_device_data[device]["seen"]["first"]["pos"] = [current_position[0], current_position[1]]
            bluetooth_device_data[device]["seen"]["last"] = {}
            bluetooth_device_data[device]["seen"]["last"]["time"] = time.time()
            bluetooth_device_data[device]["seen"]["last"]["pos"] = [current_position[0], current_position[1]]

        bluetooth_device_data[device]["name"] = devices[device]["name"]

    bluetooth_threats = {}
    for device in bluetooth_device_data: # Iterate through each device in the Bluetooth device data.
        time_since_last = time.time() - bluetooth_device_data[device]["seen"]["last"]["time"]
        if (time_since_last < 5): # Check to see if it has been less than 5 seconds since this device was last seen.
            if (len(config["general"]["bluetooth_scanning"]["blacklist"]) > 0): # Check to see if there is at least one entry in the blacklist.
                if (device in config["general"]["bluetooth_scanning"]["blacklist"]): # Check to see if this device is in the blacklist.
                    if (device.upper() not in bluetooth_threats):
                        bluetooth_threats[device] = {}
                    bluetooth_threats[device]["blacklist"] = config["general"]["bluetooth_scanning"]["blacklist"][device]
            if (config["general"]["bluetooth_scanning"]["thresholds"]["time"]["enabled"] == True): # Check to see if time-based alerts are enabled.
                total_time_seen = bluetooth_device_data[device]["seen"]["last"]["time"] - bluetooth_device_data[device]["seen"]["first"]["time"]
                if (total_time_seen > config["general"]["bluetooth_scanning"]["thresholds"]["time"]["limit"]): # Check to see if the Bluetooth time threhsold has been exceeded for this device.
                    if (device not in bluetooth_threats):
                        bluetooth_threats[device] = {}
                    bluetooth_threats[device]["time"] = total_time_seen
            if (config["general"]["bluetooth_scanning"]["thresholds"]["distance"]["enabled"] == True): # Check to see if time-based alerts are enabled.
                followed_distance = get_distance(bluetooth_device_data[device]["seen"]["first"]["pos"][0], bluetooth_device_data[device]["seen"]["first"]["pos"][1], bluetooth_device_data[device]["seen"]["last"]["pos"][0], bluetooth_device_data[device]["seen"]["last"]["pos"][1]) # Calculate the distance between the start and end points of this device (measured in miles).
                if (followed_distance < config["general"]["bluetooth_scanning"]["thresholds"]["distance"]["limit"]): # Check to see if this device has been following for a distance greater than the threshold.
                    if (device not in bluetooth_threats):
                        bluetooth_threats[device] = {}
                    bluetooth_threats[device]["distance"] = followed_distance


    return bluetooth_threats

def get_all_bluetooth_devices(): # This function simply returns all known Bluetooth devices.
    global bluetooth_device_data
    return bluetooth_device_data
