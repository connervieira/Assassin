import csv
import os
import time
import datetime

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
get_distance = utils.get_distance
calculate_bearing = utils.calculate_bearing
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file

import subprocess


# Locate and load the configuration file.
config = load_config()





# Define the function used to fetch aircraft data from the Dump1090 ADS-B message output. This function is also responsible for managing the raw message data itself.
debug_message("Creating `fetch_aircraft_data` function")
def fetch_aircraft_data(file):
    debug_message("Fetching aircraft data")

    if (os.path.exists(str(file)) == True): # Check to see if the filepath supplied exists before attempting to load it.
        debug_message("Reading raw ADS-B messages")

        message_file = open(file)
        file_contents = message_file.readlines()
        message_file.close()
        raw_output = []
        for line in file_contents:
            raw_output.append(line.split(","))
        raw_output = [item for item in raw_output if len(item) > 7] # Filter out any messages that aren't the expected length.
                

        save_to_file(file, "", True) # After loading the file, erase its contents. This allows new messages to be saved while the data processing takes place.


        # Iterate through all received messages, and delete any that have exceeded the time-to-live threshold set in the configuration.
        debug_message("Removing expired messages")
        messages_pruned_count = 0 # This is a placeholder variable that will be incremented by 1 for each message removed. This is used for debugging purposes.
        for message in reversed(raw_output): # Iterate through each message (line) in the file, in reverse order to prevent list entries from being shuffled around during the pruning process.
            try:
                message_timestamp = round(time.mktime(datetime.datetime.strptime(message[6] + " " + message[7], "%Y/%m/%d %H:%M:%S.%f").timetuple())) # Get the timestamp of this message.
            except:
                message_timestamp = 0
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




def start_adsb_monitoring():
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        if (config["general"]["adsb_alerts"]["adsb_message_file"] != ""): # Check to see if an ADS-B message file has been set.
            stop_command = ["sudo", "killall", "dump1090-mutability"] # This command is responsible for killing any existing instances of Dump1090.
            start_command = ["sudo", "dump1090-mutability", "--net", "--quiet"] # This command is responsible for starting Dump1090.
            stream_command = ["wget", "http://localhost:30003/", "-O", config["general"]["adsb_alerts"]["adsb_message_file"], "--quiet"] # This command is responsible for streaming data from Dump1090.

            subprocess.Popen(stop_command) # Execute the command to stop existing instances of Dump1090.
            time.sleep(2) # Given Dump1090 time to exit.
            subprocess.Popen(start_command) # Execute the command to start Dump1090 in the background.
            time.sleep(3) # Given Dump1090 time to start up.
            subprocess.Popen(stream_command) # Execute the command to stream data from Dump1090 in the background.
        else:
            display_notice("ADS-B alerts are enabled, but no message file was set.", 3)


def adsb_alert_processing(current_location):
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Processing ADS-B alerts")
        aircraft_data = fetch_aircraft_data(config["general"]["adsb_alerts"]["adsb_message_file"]) # Fetch the most recent aircraft data.

        aircraft_threats = [] # Set the list of active aircraft threats to an empty placeholder database.

        debug_message("Determining ADS-B threats")
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

                precise_alert_threshold = (int(aircraft_location[2]) / config["general"]["adsb_alerts"]["base_altitude_threshold"]) * config["general"]["adsb_alerts"]["distance_threshold"] # Calculate the precise alerting distance based on the aircraft altitude, base altitude threshold, and alert distance configured by the user. Higher altitude will cause planes to alert from farther away.


                aircraft_data[key]["threatlevel"] = 0
                if (aircraft_distance < precise_alert_threshold): # Check to see if the aircraft is within the alert distance range.
                    aircraft_data[key]["threatlevel"] = 1
                    if (int(aircraft_data[key]["altitude"]) <= int(config["general"]["adsb_alerts"]["maximum_aircraft_altitude"]) and int(aircraft_data[key]["altitude"]) >= int(config["general"]["adsb_alerts"]["minimum_aircraft_altitude"])): # Check to see if the aircraft is at the altitude range specified in the configuration.
                        aircraft_data[key]["threatlevel"] = 2
                        if (int(aircraft_data[key]["speed"]) >= int(config["general"]["adsb_alerts"]["minimum_aircraft_speed"]) and int(aircraft_data[key]["speed"]) <= int(config["general"]["adsb_alerts"]["maximum_aircraft_speed"])): # Check to see if the aircraft is within the alert speed range specified in the configuration.
                            aircraft_data[key]["threatlevel"] = 3

                if (aircraft_data[key]["threatlevel"] >= config["general"]["adsb_alerts"]["threat_threshold"]): # Check to see if this aircraft's threat level exceeds the threshold set in the configuration.
                    aircraft_threats.append(aircraft_data[key]) # Add this aircraft to the list of active threats.




        # Sort the ADS-B aircraft alert database.
        if (len(aircraft_threats) > 1): # Only sort the aircraft threats list if there is more than 1 entry in it.
            debug_message("Sorting ADS-B threats")
            sorted_aircraft_threats = [] # Set the sorted aircraft threats to a blank placeholder so each entry can be added one by one in the next steps.
            for i in range(0, len(aircraft_threats)): # Run once for every entry in the aircraft threat list.
                current_closest = {"distance": 100000000000} # Set the current closest aircraft to placeholder data with an extremely far distance.
                for element in aircraft_threats:
                    if (element["distance"] < current_closest["distance"]): # Check to see if the distance to this aircraft is shorter than the current known closest aircraft.
                        current_closest = element # Set this aircraft to the current closest known aircraft.

                sorted_aircraft_threats.append(current_closest) # Add the closest aircraft from this cycle to the list.
                aircraft_threats.remove(current_closest) # After adding it to the sorted list, remove it from the original list.

            aircraft_threats = sorted_aircraft_threats # After the sorting has been finished, set the original aircraft threats list to the sorted version of it's original contents.
            

        debug_message("Processed ADS-B alerts")
        return aircraft_threats, aircraft_data # Return the processed information.
    else:
        return [], {} # Return the processed information.
