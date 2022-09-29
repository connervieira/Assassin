# Assassin

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Assassin...")


import os # Required to interact with certain operating system functions
import json # Required to process JSON data


assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory, containing all the program's support files.. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json



import time # Required to add delays and handle dates/times
import sys
import re # Required to use Regex
import validators # Required to validate URLs
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings

import utils # Import the utils.py scripts.
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
get_distance = utils.get_distance # Load the function to get the distance between to global positions.
load_traffic_cameras = utils.load_traffic_cameras # Load the function used to load the database of speed and red-light cameras.
nearby_traffic_cameras = utils.nearby_traffic_cameras # Load the function used to check for nearby traffic cameras.
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.


input_file = input("Input File: ")
output_file = input("Output File: ")


if (os.path.exists(input_file)): # Check to see if the input file path exists.
    input_database = json.load(open(input_file)) # Load the database from the file.
else:
    display_notice("The input file specified does not exist.", 3)
    exit()


output_database = { }

output_database["name"] = "Imported Database"
output_database["description"] = "This is a database imported from Overpass"
output_database["author"] = "OpenStreetMap Contributors"
output_database["created"] = str(round(time.time()))
output_database["modified"] = str(round(time.time()))
output_database["elements"] = {'direction': 'int', 'operator': 'str', 'name': 'str', 'description': 'str'}
output_database["entries"] = []

for entry in input_database["elements"]:
    new_entry_data = {}
    new_entry_data["latitude"] = entry["lat"]
    new_entry_data["longitude"] = entry["lon"]

    if "direction" in entry["tags"].keys():
        new_entry_data["direction"] = int(entry["tags"]["direction"])
    elif "camera:direction" in entry["tags"].keys():
        new_entry_data["direction"] = int(entry["tags"]["camera:direction"])
    else:
        new_entry_data["direction"] = ""

    if "operator" in entry["tags"].keys():
        new_entry_data["operator"] = str(entry["tags"]["operator"])
    else:
        new_entry_data["operator"] = ""

    if "name" in entry["tags"].keys():
        new_entry_data["name"] = str(entry["tags"]["name"])
    else:
        new_entry_data["name"] = ""

    if "description" in entry["tags"].keys():
        new_entry_data["description"] = str(entry["tags"]["description"])
    else:
        new_entry_data["description"] = ""

    output_database["entries"].append(new_entry_data)



print (json.dumps(output_database, indent=4))
