# Assassin - Database Preview

# This tool allows you to preview a point-of-interest database by plotting it's points on a graph. To use it, run it using Python3, then enter the following information as prompted.

# Type - This is the type of database. The traffic enforcement camera database uses the 'excam' format. The ALPR database, and other custom databases use the 'json' format.
# Database - This is an absolute file path to the database you want to preview.
# Longitude - This is the longitude of the center point of the graph.
# Latitude - This is the latitude of the center point of the graph.
# Radius - This is the radius you want to preview.




# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

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
        loaded_alpr_camera_database = json.load(open(database_to_load)) # Load the ALPR database.
    else:
        loaded_alpr_camera_database = {} # Load a blank database, since the actual database couldn't be loaded.
        if (database_to_load == ""): # The database entry was left empty.
            print("No database was specified")
        elif (os.path.exists(database_to_load) == False): # The specified database specified does not exist.
            print("The specified database does not exist.")
        else:
            print("An unknown error occurred")

    return loaded_alpr_camera_database # Return the loaded database information.


# Define the function that will be used to fetch all traffic cameras within a certain radius and load them to memory.
def load_traffic_cameras(current_lat, current_lon, database_file, radius):
    if (os.path.exists(database_file) == True): # Check to make sure the database specified in the configuration actually exists.
        with lzma.open(database_file, "rt", encoding="utf-8") as f: # Open the database file.
            database_lines = list(map(json.loads, f)) # Load the camera database
            loaded_database_information = [] # Load an empty placeholder database so we can write data to it later.
            
            for camera in database_lines: # Iterate through each camera in the database.
                if ("lat" in camera and "lon" in camera): # Only check this camera if it has a latitude and longitude defined in the database.
                    if (get_distance(current_lat, current_lon, camera['lat'], camera['lon']) < float(radius)): # Check to see if this camera is inside the initial loading radius.
                        loaded_database_information.append(camera)
    else: # The database file specified does not exist.
        loaded_database_information = [] # Return a blank database if the file specified doesn't exist.

    return loaded_database_information # Return the newly edited database information.


database_type = input("Type (excam, json): ")
database_to_load = input("Database: ")
current_latitude = float(input("Latitude: "))
current_longitude = float(input("Longitude: "))
load_radius = float(input("Radius: "))

x = []
y = []


if (database_type == "json"):
    loaded_database = load_database(database_to_load) # Load the specified JSON database.
    for entry in loaded_database["entries"]: # Iterate through each element in the loaded database.
        if (get_distance(current_latitude, current_longitude, entry["latitude"], entry["longitude"]) <= load_radius): # Check to see if this entry is within the range specified by the user.
            # Add this entry to the graph data.
            y.append(entry["latitude"])
            x.append(entry["longitude"])

elif (database_type == "excam"):
    loaded_traffic_camera_database = load_traffic_cameras(current_longitude, current_latitude, database_to_load, load_radius) # Load the specified traffic camera database.
    for camera in loaded_traffic_camera_database: # Iterate through each camera in the traffic camera database.
        # Add this entry to the database.
        y.append(camera["lat"])
        x.append(camera["lon"])
else:
    print ("Unknown database type")


# Set up the graph information.
plt.scatter([current_longitude], [current_latitude], color = "blue", marker = "X", s = 100) # Display the user-specified location as a large blue marker.
plt.scatter(x, y, color = "green", marker = "X", s = 30) # Display the database points as small green markers.
plt.ylabel('Longitude')
plt.xlabel('Latitude')
  
# Display the graph.
plt.show()
