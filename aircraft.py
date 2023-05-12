# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import csv
import os
import time
import datetime


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
import socket

# Locate and load the configuration file.
config = load_config()



def sort_aircraft_by_distance(aircraft):
    if (len(aircraft) > 1): # Only sort the aircraft threats list if there is more than 1 entry in it.
        sorted_aircraft_threats = [] # Set the sorted aircraft threats to a blank placeholder so each entry can be added one by one in the next steps.
        for i in range(0, len(aircraft)): # Run once for every entry in the aircraft threat list.
            current_closest = {"distance": 100000000000, "threatlevel": 0} # Set the current closest aircraft to placeholder data with an extremely far distance, such that any aircraft detected will be closer.
            for element in aircraft:
                if (element["threatlevel"] >= current_closest["threatlevel"]): # Check to see if the threat level of this aircraft is greater than or equal to the current closest aircraft.
                    if (element["distance"] < current_closest["distance"]): # Check to see if the distance to this aircraft is shorter than the current known closest aircraft.
                        current_closest = element # Set this aircraft to the current closest known aircraft.

            sorted_aircraft_threats.append(current_closest) # Add the closest aircraft from this cycle to the list.
            aircraft.remove(current_closest) # After adding it to the sorted list, remove it from the original list.
        aircraft = sorted_aircraft_threats # After the sorting has been finished, set the original aircraft threats list to the sorted version of it's original contents.

    return aircraft



def receive_messages():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 30003))
        client.send(b"GET / HTTP/1.1\r\n\r\n")

        while True:
            received_data = client.recv(1024)
            if (len(received_data) == 0): # Check to see if the connection has been closed.
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("localhost", 30003))
                client.send(b"GET / HTTP/1.1\r\n\r\n")
            
            received_data = received_data.decode("utf-8")
            received_data = received_data.replace("\\r", "")
            received_data = received_data.replace("\r", "")
            received_data = received_data.replace("\\n", "")
            if (len(received_data) > 3):
                if (received_data[0:3] == "MSG"):
                    add_to_file(config["general"]["working_directory"] + "/" + config["general"]["adsb_alerts"]["adsb_message_filename"], received_data)
    except:
        display_notice("ADS-B alerts are enabled, but the ADS-B message stream could not be opened.", 3)




def prune_messages(adsb_messages, file):
    messages_pruned_count = 0 # This is a placeholder variable that will be incremented by 1 for each message removed. This is used for debugging purposes.
    for message in reversed(adsb_messages): # Iterate through each message (line) in the file, in reverse order to prevent list entries from being shuffled around during the pruning process.
        try:
            message_timestamp = round(time.mktime(datetime.datetime.strptime(message[6] + " " + message[7], "%Y/%m/%d %H:%M:%S.%f").timetuple())) # Get the timestamp of this message.
        except:
            message_timestamp = 0
        message_age = time.time() - message_timestamp # Calculate the age of this message.
        if (message_age > config["general"]["adsb_alerts"]["message_time_to_live"]): # Check to see if this message's age is older than the time-to-live threshold set in the configuration.
            adsb_messages.remove(message) # Remove this message from the raw data.
            messages_pruned_count = messages_pruned_count + 1 # Increment the pruned message counter by 1.

    new_raw_csv_string = "" # This is a placeholder string that will hold the entire contents of the new CSV file.
    for line in adsb_messages: # Iterate through each line of the pruned CSV data.
        next_csv_line = "" # This is a placeholder string that holds the contents of the current line of the CSV file.
        line[0] = "MSG"
        for entry in line: # Iterate through each field in this line.
            next_csv_line = next_csv_line + str(entry) + "," # Add each entry to the line.
        next_csv_line = next_csv_line[:-1] # Remove the last comma in the line.
        new_raw_csv_string = new_raw_csv_string + next_csv_line # Add a line break at the end of the last line.

    add_to_file(file, new_raw_csv_string, True) # Save the pruned CSV data back to the original file.




# The `message_file_maintainer` prunes the messages from the ADS-B file on a regular basis to reduce the lag spike when ADS-B alerts are processed.
def message_file_maintainer():
    file = config["general"]["working_directory"] + "/" + config["general"]["adsb_alerts"]["adsb_message_filename"]
    while True:
        if (os.path.exists(str(file)) == True): # Check to see if the filepath supplied exists before attempting to load it.
            message_file = open(file) # Open the ADS-B message file.
            file_contents = message_file.readlines() # Read the ADS-B message file line by line.
            message_file.close() # Close the ADS-B message file.
            save_to_file(file, "", True) # After loading the file, erase its contents. This allows new messages to be saved while the data processing takes place.
            raw_adsb_data = [] # Set the raw message output to a blank placeholder list.
            for line in file_contents: # Iterate through each line in the ADS-B file contents.
                raw_adsb_data.append(line.split(",")) # Add each line to the complete output.
            raw_adsb_data = [item for item in raw_adsb_data if len(item) > 7] # Filter out any messages that are significantly shorter than expected.


            debug_message("Removing expired messages")
            prune_messages(raw_adsb_data, file)

        time.sleep(0.2)






def start_adsb_monitoring():
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Starting ADS-B monitoring")
        save_to_file(config["general"]["working_directory"] + "/" + config["general"]["adsb_alerts"]["adsb_message_filename"], "") # Clear the ADS-B message file.
        if (config["general"]["adsb_alerts"]["adsb_message_filename"] != ""): # Check to see if an ADS-B message file has been set.
            start_command = ["sudo", "dump1090-mutability", "--net", "--quiet"] # This command is responsible for starting Dump1090.

            debug_message("Starting ADS-B receiver")
            subprocess.Popen(start_command) # Execute the command to start Dump1090 in the background.
            time.sleep(3) # Give Dump1090 time to start up.
            debug_message("Opening ADS-B message stream")
            adsb_message_receive_thread = threading.Thread(target=receive_messages, name="ADSBMessageStream")
            adsb_message_receive_thread.start()
            adsb_message_maintainer_thread = threading.Thread(target=message_file_maintainer, name="ADSBMessageMaintainer")
            adsb_message_maintainer_thread.start()
        else:
            display_notice("ADS-B alerts are enabled, but no message file name was set. ADS-B monitoring could not be started.", 3)



# Define the function used to fetch aircraft data from the Dump1090 ADS-B message output. This function is also responsible for managing the raw message data itself.
debug_message("Creating `fetch_aircraft_data` function")
def fetch_aircraft_data(file):
    debug_message("Fetching aircraft data")

    if (os.path.exists(str(file)) == True): # Check to see if the filepath supplied exists before attempting to load it.
        debug_message("Reading raw ADS-B messages")

        message_file = open(file) # Open the ADS-B message file.
        file_contents = message_file.readlines() # Read the ADS-B message file line by line.
        message_file.close() # Close the ADS-B message file.
        save_to_file(file, "", True) # After loading the file, erase its contents. This allows new messages to be saved while the data processing takes place.
        raw_adsb_data = [] # Set the raw message output to a blank placeholder list.
        for line in file_contents: # Iterate through each line in the ADS-B file contents.
            raw_adsb_data.append(line.split(",")) # Add each line to the complete output.
        raw_adsb_data = [item for item in raw_adsb_data if len(item) > 7] # Filter out any messages that are significantly shorter than expected.



        debug_message("Collecting aircraft data")
        aircraft_data = {} # Set the aircraft data as a placeholder dictionary so information can be added to it in later steps.
        for entry in raw_adsb_data: # Iterate through each entry in the CSV list data.
            if (len(entry) >= 17): # Only process this entry if it has valid message information.
                if (entry[4] in aircraft_data): # Check to see if the aircraft associated with this message already exists in the database.
                    individual_data = aircraft_data[entry[4]] # If so, fetch the existing aircraft data.
                else:
                    individual_data = {"latitude":"0", "longitude":"0", "altitude":"0", "speed":"0", "heading":0, "climb":"0", "callsign":"", "time":""} # Set the data for this aircraft to a fresh placeholder.

                if (entry[4] != ""): # Only fetch the identification if the message data for it isn't blank.
                    individual_data["id"] = entry[4] # Get the aircraft's identification.
                if (entry[14] != ""): # Only update the latitude information if the message data for it isn't blank.
                    try:
                        individual_data["latitude"] = float(entry[14])
                    except:
                        individual_data["latitude"] = 0.0
                if (entry[15] != ""): # Only update the longitude information if the message data for it isn't blank.
                    try:
                        individual_data["longitude"] = float(entry[15])
                    except:
                        individual_data["longitude"] = 0.0
                if (entry[11] != ""): # Only update the altitude information if the message data for it isn't blank.
                    try:
                        individual_data["altitude"] = float(entry[11])
                    except:
                        individual_data["altitude"] = 0.0
                if (entry[12] != ""): # Only update the speed information if the message data for it isn't blank.
                    try:
                        individual_data["speed"] = float(entry[12])
                    except:
                        individual_data["speed"] = 0.0
                if (entry[13] != ""): # Only update the heading information if the message data for it isn't blank.
                    try:
                        individual_data["heading"] = int(entry[13]) # Get the aircraft's compass heading.
                    except:
                        individual_data["heading"] = 0 # Use a placeholder for the aircraft's heading.
                if (entry[16] != ""): # Only update the climb rate information if the message data for it isn't blank.
                    try:
                        individual_data["climb"] = float(entry[16]) # Get the aircraft's vertical climb rate.
                    except:
                        individual_data["climb"] = 0.0
                if (entry[10] != ""): # Only update the callsign information if the message data for it isn't blank.
                    individual_data["callsign"] = entry[10].strip() # Get the aircraft's callsign, removing any trailing or leading spaces.
                if (entry[6] != "" and entry[7] != ""): # Ensure the message date and time are set.
                    try:
                        individual_data["time"] = round(time.mktime(datetime.datetime.strptime(entry[6] + " " + entry[7], "%Y/%m/%d %H:%M:%S.%f").timetuple())) # Convert the human readable timestamp into a Unix timestamp.
                    except:
                        individual_data["time"] = 0
                else:
                    display_notice("An ADS-B message didn't have an associated date and time. This should never happen.", 2)

                aircraft_data[entry[4]] = individual_data # Add the updated aircraft information back to the main database.
            
        return aircraft_data # Return the processed aircraft data.

    else: # The file supplied to load ADS-B messages from does not exist.
        display_notice("The ADS-B message stream file specified in the configuration does not exist. ADS-B messages can't be loaded.", 3)
        return {} # Return blank aircraft data.





def adsb_alert_processing(current_location, current_speed):
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Processing ADS-B alerts")
        aircraft_data = fetch_aircraft_data(config["general"]["working_directory"] + "/" + config["general"]["adsb_alerts"]["adsb_message_filename"]) # Fetch the most recent aircraft data.

        aircraft_threats = [] # Set the list of active aircraft threats to an empty placeholder database.

        if (current_speed >= config["general"]["adsb_alerts"]["minimum_vehicle_speed"]): # Check to see if the current vehicle speed is greater than or equal to the minimum to issue alerts.
            for key in aircraft_data.keys(): # Iterate through all detected aircraft
                aircraft_location = [aircraft_data[key]["latitude"], aircraft_data[key]["longitude"], aircraft_data[key]["altitude"]] # Grab the location information for the aircraft.

                if (aircraft_location[0] != "" and aircraft_location[1] != ""): # Check to make sure this aircraft has location information. Otherwise, skip it.
                    # Calculate the distance to the aircraft.
                    aircraft_distance = get_distance(current_location[0], current_location[1], aircraft_location[0], aircraft_location[1]) # Calculate the distance to the aircraft.
                    aircraft_data[key]["distance"] = aircraft_distance # Add the distance to the aircraft to its data.

                    # Calculate the heading of the aircraft relative to the current direction of motion.
                    try: # Try calculating the relative heading using relevant information.
                        relative_heading = int(aircraft_data[key]["heading"]) - int(current_location[4]) # Calculate the heading direction of this aircraft relative to the current direction of movement
                    except: # If the relative heading fails to be calculated, then use a placeholder.
                        relative_heading = 0
                    if (relative_heading < 0): # Check to see if the relative heading is a negative number.
                        relative_heading = 360 + relative_heading # Convert the relative heading to a positive number.
                    aircraft_data[key]["relativeheading"] = relative_heading # Add the relative heading of the aircraft to its data.

                    # Calculate the direction to the aircraft relative to the current position and direction of movement.
                    relative_direction = calculate_bearing(current_location[0], current_location[1], aircraft_data[key]["latitude"], aircraft_data[key]["longitude"]) - current_location[4]
                    if (relative_direction < 0): # Check to see if the direction to the aircraft is negative.
                        relative_direction = 360 + relative_direction
                    aircraft_data[key]["direction"] = relative_direction # Add the direction to the aircraft to its data.

                    if (config["general"]["adsb_alerts"]["criteria"]["distance"]["base_altitude"] > 0): # Check to make sure the base altitude configuration value is positive.
                        adjusted_alert_threshold = (int(aircraft_location[2]) / config["general"]["adsb_alerts"]["criteria"]["distance"]["base_altitude"]) * config["general"]["adsb_alerts"]["criteria"]["distance"]["base_distance"] # Calculate the precise alerting distance based on the aircraft altitude, base altitude threshold, and alert distance configured by the user. Higher altitude will cause planes to alert from farther away.
                    else: # The base altitude configuration value is less than or equal to 0.
                        display_notice("The general>adsb_alerts>criteria>distance>base_altitude is less than or equal to 0. The alert radius could not be calculated. Defaulting to 3 miles.", 2)
                        adjusted_alert_threshold = 3.0


                    aircraft_data[key]["threatlevel"] = 0
                    if (aircraft_distance < adjusted_alert_threshold): # Check to see if the aircraft is within the alert distance range.
                        aircraft_data[key]["threatlevel"] = 1
                        if (int(aircraft_data[key]["altitude"]) <= int(config["general"]["adsb_alerts"]["criteria"]["altitude"]["maximum"]) and int(aircraft_data[key]["altitude"]) >= int(config["general"]["adsb_alerts"]["criteria"]["altitude"]["minimum"])): # Check to see if the aircraft is at the altitude range specified in the configuration.
                            aircraft_data[key]["threatlevel"] = 2
                            if (int(aircraft_data[key]["speed"]) >= int(config["general"]["adsb_alerts"]["criteria"]["speed"]["minimum"]) and int(aircraft_data[key]["speed"]) <= int(config["general"]["adsb_alerts"]["criteria"]["speed"]["maximum"])): # Check to see if the aircraft is within the alert speed range specified in the configuration.
                                aircraft_data[key]["threatlevel"] = 3

                    if (aircraft_data[key]["threatlevel"] >= config["general"]["adsb_alerts"]["threat_threshold"]): # Check to see if this aircraft's threat level exceeds the threshold set in the configuration.
                        aircraft_threats.append(aircraft_data[key]) # Add this aircraft to the list of active threats.


            # Sort the ADS-B aircraft alert database.
            if (len(aircraft_threats) > 1): # Only sort the alerts if there is more than 1 aircraft threat detected.
                debug_message("Sorting ADS-B threats")

                level0_threats = []
                level1_threats = []
                level2_threats = []
                level3_threats = []

                for element in aircraft_threats:
                    if (element["threatlevel"] == 0):
                        level0_threats.append(element)
                    elif (element["threatlevel"] == 1):
                        level1_threats.append(element)
                    elif (element["threatlevel"] == 2):
                        level2_threats.append(element)
                    elif (element["threatlevel"] == 3):
                        level3_threats.append(element)

                sorted_level0_threats = sort_aircraft_by_distance(level0_threats)
                sorted_level1_threats = sort_aircraft_by_distance(level1_threats)
                sorted_level2_threats = sort_aircraft_by_distance(level2_threats)
                sorted_level3_threats = sort_aircraft_by_distance(level3_threats)

                sorted_aircraft_threats = []
                for element in sorted_level3_threats:
                    sorted_aircraft_threats.append(element)
                for element in sorted_level2_threats:
                    sorted_aircraft_threats.append(element)
                for element in sorted_level1_threats:
                    sorted_aircraft_threats.append(element)
                for element in sorted_level0_threats:
                    sorted_aircraft_threats.append(element)

                aircraft_threats = sorted_aircraft_threats
            

        debug_message("Processed ADS-B alerts")
        return aircraft_threats, aircraft_data # Return the processed information.
    else:
        return [], {} # Return blank placeholders.
