import csv
import os
import time
import datetime

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
fetch_aircraft_data = utils.fetch_aircraft_data
get_distance = utils.get_distance
calculate_bearing = utils.calculate_bearing
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file


# Locate and load the configuration file.
config = load_config()



def adsb_alert_processing(current_location):
    if (config["general"]["adsb_alerts"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
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

                # Calculate the direction to the aircraft relative to the current position.
                relative_direction = calculate_bearing(current_location[0], current_location[1], aircraft_data[key]["latitude"], aircraft_data[key]["longitude"])
                if (relative_direction < 0): # Check to see if the direction to the aircraft is negative.
                    relative_direction = 360 + relative_direction
                aircraft_data[key]["direction"] = relative_direction # Add the direction to the aircraft to its data.

                precise_alert_threshold = (int(aircraft_location[2]) / config["general"]["adsb_alerts"]["base_altitude_threshold"]) * config["general"]["adsb_alerts"]["distance_threshold"] # Calculate the precise alerting distance based on the aircraft altitude, base altitude threshold, and alert distance configured by the user. Higher altitude will cause planes to alert from farther away.


                aircraft_data[key]["threatlevel"] = 0
                if (aircraft_distance < precise_alert_threshold): # Check to see if the aircraft is within the alert distance range.
                    aircraft_data[key]["threatlevel"] = 1
                    if (int(aircraft_data[key]["altitude"]) <= int(config["general"]["adsb_alerts"]["maximum_aircraft_altitude"])): # Check to see if the aircraft is at the altitude range specified in the configuration.
                        aircraft_data[key]["threatlevel"] = 2
                        if (int(aircraft_data[key]["speed"]) >= int(config["general"]["adsb_alerts"]["minimum_aircraft_speed"]) and int(aircraft_data[key]["speed"]) <= int(config["general"]["adsb_alerts"]["maximum_aircraft_speed"])): # Check to see if the aircraft is within the alert speed range specified in the configuration.
                            aircraft_data[key]["threatlevel"] = 3

                if (aircraft_data[key]["threatlevel"] >= config["general"]["adsb_alerts"]["threat_threshold"]): # Check to see if this aircraft's threat level exceeds the threshold set in the configuration.
                    aircraft_threats.append(aircraft_data[key]) # Add this aircraft to the list of active threats.




        # Sort the ADS-B aircraft alert database.
        if (len(aircraft_threats) > 1): # Only sort the aircraft threats list if there is more than 1 entry in it.
            debug_message("Sorting ADS-B threats")
            sorted_aircraft_threats = [] # Set the sorted aircraft threats to a blank placeholder so each entry can be added one by one in the next steps.
            for i in range(1, len(aircraft_threats)): # Run once for every entry in the aircraft threat list.
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
