# Assassin - Removed Database Points

# This tool takes two POI databases and returns a list of points that are present in the first database, but removed from the second.


# Copyright (C) 2025 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.


import os
import json
import utils


filepath1 = input("Starting File: ")
filepath2 = input("Ending File: ")

filepath1 = "../assets/databases/2024-09-11 alpr.json"
filepath2 = "../assets/databases/2025-03-27 alpr.json"

if (os.path.exists(filepath1)): # Check to see if the input file path exists.
    database1 = json.load(open(filepath1)) # Load the database from the file.
else:
    display_notice("The first file specified does not exist.", 3)
    exit()

if (os.path.exists(filepath2)): # Check to see if the input file path exists.
    database2 = json.load(open(filepath2)) # Load the database from the file.
else:
    display_notice("The second file specified does not exist.", 3)
    exit()



for entry1 in database1["entries"]:
    found_match = False
    for entry2 in database2["entries"]:
        direction_difference = abs(entry1["facing"] - entry2["facing"])
        if (direction_difference > 360):
            direction_difference -= 360
        if (direction_difference < 20):
            location_difference = utils.get_distance(entry1["lat"], entry1["lon"], entry2["lat"], entry2["lon"])
            if (location_difference < 0.01): # Check to see if this point is within 10 meters.
                found_match = True
                break
    if (found_match == False):
        print("REMOVED:")
        print(entry1)
