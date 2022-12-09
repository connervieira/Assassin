# Assassin - Database Verify

# This tool is designed to validate a database, and detect potentially broken information.



# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




import matplotlib.pyplot as plt # Required to create graphs.
import os # Required to handle files.
import json # Required to load custom databases.
import lzma # Required to load ExCam database.
import math # Required complete more complex calculations.


def get_distance(lat1, lon1, lat2, lon2, efficient_mode = True):
    # Convert the coordinates received.
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    # Verify the coordinates received, if efficient mode is disabled.
    if (efficient_mode == False):
        if (lat1 > 180 or lat1 < -180):
            display_notice("Latitude value 1 is out of bounds, and is invalid.", 2)
            lat1 = 0 # Default to a safe value.
        if (lon1 > 90 or lon1 < -90):
            display_notice("Longitude value 1 is out of bounds, and is invalid.", 2)
            lon1 = 0 # Default to a safe value.
        if (lat2 > 180 or lat2 < -180):
            display_notice("Latitude value 2 is out of bounds, and is invalid.", 2)
            lat2 = 0 # Default to a safe value.
        if (lon2 > 90 or lon2 < -90):
            display_notice("Longitude value 2 is out of bounds, and is invalid.", 2)
            lon2 = 0 # Default to a safe value.

    if (lon1 == lon2 and lat1 == lat2): # Check to see if the coordinates are the same.
        distance = 0 # The points are the same, so they are 0 miles apart.

    else: # The points are different, so calculate the distance between them
        # Convert the coordinates into radians.
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Calculate the distance.
        distance = 6371.01 * math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon1 - lon2))

        # Convert the distance from kilometers to miles.
        distance = distance * 0.6213712

    # Return the calculated distance.
    return distance


def load_database(database_to_load):
    if (database_to_load != "" and os.path.exists(database_to_load)): # Check to see if the ALPR camera database exists.
        loaded_database = json.load(open(database_to_load)) # Load the ALPR database.
    else:
        loaded_database = {} # Load a blank database, since the actual database couldn't be loaded.
        if (database_to_load == ""): # The database entry was left empty.
            print("No database was specified")
        elif (os.path.exists(database_to_load) == False): # The specified database specified does not exist.
            print("The specified database does not exist.")
        else:
            print("An unknown error occurred")

    return loaded_database # Return the loaded database information.


x = []
y = []


database_to_load = input("Database: ")


distance_threshold = 5
angle_threshold = 50


loaded_database = load_database(database_to_load)


# Find potential duplicate entries.
duplicate_scanned_database = loaded_database # This is a copy of the loaded database that will have entries removed as they are checked.
for entry1 in duplicate_scanned_database["entries"]:
    entry1_information = entry1
    duplicate_scanned_database["entries"].remove(entry1)
    for entry2 in duplicate_scanned_database["entries"]:
        distance = get_distance(entry1_information["latitude"], entry1_information["longitude"], entry2["latitude"], entry2["longitude"])
        if (distance < distance_threshold / 5280): # Check to see if these database entries are within 5 feet of each other.
            if (entry1_information["direction"] -  entry2["direction"] < angle_threshold / 2 and entry1_information["direction"] -  entry2["direction"] >  -1 * (angle_threshold / 2)):
                if (entry1_information["brand"] == entry2["brand"]):
                    print("Duplicate POI:")
                    print("    Distance: " + str(distance * 5280))
                    print("    Entry 1: " + str(entry1))
                    print("    Entry 2: " + str(entry2))



# Find entries with broken direction information.
for entry in loaded_database["entries"]:
    if (entry["direction"] < 0 or entry["direction"] > 360):
        print("Malformed Direction:")
        print("    Direction: " + str(entry["direction"]))
        print("    Entry: " + str(entry))
