# Assassin - Database Editor

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os
import json

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory, containing all the program's support files. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(assassin_root_directory + "/../config.json")) # Load the configuration database from config.json


import time # Required to add delays and handle dates/times
import sys
import re # Required to use Regex
import validators # Required to validate URLs
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings
from geopy.distance import great_circle # Required to calculate distance between locations.
import random # Required to generate random numbers.


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






root = input("Project root directory path: ") # Prompt the user to enter a path for the current project.

# Run some validation to make sure the information just entered by the user is correct.
if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
    display_notice("The root project directory entered doesn't seem to exist. The database editor will almost certainly fail.", 2)


while True:
    clear() # Clear the console output at the beginning of each loop.

    # Prompt the user to select an operation.
    print("Please select an option.")
    print("0. Quit")
    print("1. Create database")
    print("2. Edit database")
    print("3. View database")
    print("4. Survey database")
    selection = input("Selection: ")


    if (selection == "0"): # The user has selected the "quit" option.
        print("Quitting...") # Inform the user that the database editor is quitting before breaking the loop.
        break # Break the loop to terminate the database editor.

    elif (selection == "1"): # The user has selected the "create database" option.
        database_name, database_description, database_author, database_file = "", "", "", "" # Set all variables related to the new database to a blank string as a placeholder.
        while (database_name == ""): # Ask the user for a name for the database forever until they enter something.
            database_name = input("    Database name: ") # Prompt the user to enter a name for the new database.
        database_description = input("    Database description: ") # Prompt the user to enter a description for the new database.
        database_author = input("    Database author: ") # Prompt the user to enter an author for the new database.
        while (database_file == "" or ".json" not in database_file): # Ask the user for a file name for the database file forever until they enter a valid file name.
            database_file = input("    Database file: ") # Prompt the user to enter a file name for the new database.

        database_data = { # Format the database data as a Python dictionary.
            "name": database_name,
            "description": database_description,
            "author": database_author,
            "created": str(round(time.time())),
            "modified": "",
            "elements": {},
            "entries": []
        }


        print("Enter each data element you'd like each entry in this database to have, in addition to the GPS coordinates included by default. Leave a blank and press enter to finish adding elements.")
        element_addition_counter = 0 # This is a placeholder variable that will be incremented by one for each element added in the next step.
        elements = {} # Create a placeholder dictionary that will be used to hold all of the entry elements specified by the user.
        while True: # Run forever untilt he user is finished entering entry elements.
            element_addition_counter = element_addition_counter + 1 # Increment the element addition counter by 1.
            element_name, element_format = "", "" # Set both variables to a blank placeholder string.
            print("    Element " + str(element_addition_counter) + ":") # Display the current element count so the user can keep track of how many they've added.
            element_name = input("        Name: ").lower() # Prompt the user for a name for the current element
            if (element_name != ""): # Only prompt the user to enter an element format if the element name wasn't left blank.
                while (element_format != "str" and element_format != "int" and element_format != "float" and element_format != "bool"): # Repeatedly prompt the user to enter an element type until they enter a valid one.
                    element_format = input("        Format (str/int/float/bool): ").lower() # Prompt the user to enter an element format (variable type).

            if (element_name == ""): # If the element name prompt was left blank, then break the loop, and finish adding elements.
                break
            else: # If the element was not left blank, then add this element to the list of elements for this database.
                database_data["elements"][str(element_name)] = str(element_format) # Add an element to the list of entry elements for this database based on the user's inputs.

        database_data["modified"] = str(round(time.time())) # Update the "last modified" time in the database.

        save_to_file(str(root) + "/" + str(database_file), str(json.dumps(database_data, indent = 4)), silence_file_saving) # Save the database to disk as JSON data.
        clear() # Clear the console output.
        print("Database created!") # Inform the user that the database was created.
        input("Press enter to continue...") # Wait for the user to press enter before continuing.


    elif (selection == "2"): # The user has selected the "edit database" option.
        database_file = "" # Set the current database file name to a blank placeholder string.
        while (os.path.exists(root + "/" + database_file) == False or database_file == ""): # Run forever until the user enters a valid database file name.
            database_file = input("Database file name: ") # Prompt the user to enter the name of the database file they want to view.
            if (os.path.exists(root + "/" + database_file) == False): # Check to see if the database file entered by the user exists.
                print(style.yellow + "Warning: The database file name entered doesn't seem to exist in the root project folder. Please enter a valid file name." + style.end) # Inform the user that the file name they entered doesn't exist in the root project directory.

        database_data = json.load(open(root + "/" + database_file)) # Load the database information from the file specified by the user.
        print("Leave an entry blank to leave the value unchanged.")

        print("Database name:")
        print("    Current: " + database_data["name"]) # Display the database's current name.
        new_name = str(input("New: ")) # Prompt the user to enter a new name.
        if (new_name != ""): # Only change the database name if the user didn't leave the prompt blank.
            database_data["name"] = new_name # Set the database's name to the new name specified by the user.
            print("    Name changed") # Notify the user that the name was changed.
        else: # If the 'new name' prompt was left blank, then don't change the name.
            print("    Name unchanged") # Notify the user that the name was left unchanged.

        print("Database description:")
        print("    Current: " + database_data["description"]) # Display the database's current description.
        new_description = str(input("New: ")) # Prompt the user to enter a new description.
        if (new_description != ""): # Only change the database description if the user didn't leave the prompt blank.
            database_data["description"] = new_description # Set the database's description to the new description specified by the user.
            print("    Description changed") # Notify the user that the description was changed.
        else: # If the 'new description' prompt was left blank, then don't change the description.
            print("    Description unchanged") # Notify the user that the description was left unchanged.

        print("Database author:")
        print("    Current: " + database_data["author"]) # Display the database's current author.
        new_author = str(input("New: ")) # Prompt the user to enter a new author.
        if (new_author != ""): # Only change the database author if the user didn't leave the prompt blank.
            database_data["author"] = new_author # Set the database's author to the new author specified by the user.
            print("    Author changed") # Notify the user that the author was changed.
        else: # If the 'new author' prompt was left blank, then don't change the author.
            print("    Author unchanged") # Notify the user that the author was left unchanged.


        # Show the newly updated database information.
        print("New name: " + str(database_data["name"]))
        print("New description: " + str(database_data["description"]))
        print("New author: " + str(database_data["author"]))

        database_data["modified"] = str(round(time.time())) # Update the "last modified" time on the database.

        overwrite_confirmation = input("Write changes to disk (y/n): ").lower() # Ask the user to confirm the changes before overwriting the database.

        if (overwrite_confirmation[0] == "y"): # Only overwrite the database after the user confirms doing so.
            save_to_file(str(root) + "/" + str(database_file), str(json.dumps(database_data, indent = 4)), silence_file_saving) # Save the database to disk as JSON data.
            print("Saved changes.") # Inform the user that the changes were saved.
            input("Press enter to continue...") # Wait for the user to press enter before continuing.
        elif (overwrite_confirmation[0] == "n"): # If the user didn't confirm the changes, then simply discard them and continue without saving the changes to disk.
            print("Discarded changes.") # Inform the user that the changes were discarded.
            input("Press enter to continue...") # Wait for the user to press enter before continuing.
        else: # If the user entered an invalid selection, then show a notice that an invalid selection was made, then skip.
            print(style.yellow + "Warning: Invalid option." + style.end) # Show a warning that an invalid option was selected.
            print("Discarded changes.") # Inform the user that the changes were discarded.
            input("Press enter to continue...") # Wait for the user to press enter before continuing.

        

    elif (selection == "3"): # The user has selected the "view database" option.
        database_file = "" # Set the current selected database file name to a blank placeholder string.
        while (os.path.exists(root + "/" + database_file) == False or database_file == ""): # Run forever until the user enters a valid database file name.
            database_file = input("Database file name: ") # Prompt the user to enter the name of the database file they want to view.
            if (os.path.exists(root + "/" + database_file) == False): # Check to see if the database file entered by the user exists.
                print(style.yellow + "Warning: The database file name entered doesn't seem to exist in the root project folder. Please enter a valid file name." + style.end) # Inform the user that the file name they entered doesn't exist in the root project directory.

        database_data = json.load(open(root + "/" + database_file)) # Load the database information from the file specified by the user.

        clear() # Clear the console output.
        print("Database file: " + root + "/" + database_file) # Display the current database's file path.
        print("Database name: " + database_data["name"]) # Display the current database's name.
        print("Database description: " + database_data["description"]) # Display the current database's description.
        print("Database author: " + database_data["author"]) # Display the current database's author.
        print("Database created: " + database_data["created"]) # Display the current database's creation date.
        print("Database modified: " + database_data["modified"]) # Display the current database's last-modified date.
        print("Database elements: ")
        print(json.dumps(database_data["elements"], indent = 4)) # Display all of the entry elements for the current database.
        selection = input("Display all database entries (y/n): ").lower() # Prompt the user to decide whether or not to show all database entries.

        if (selection[0] == "y"): # If the user selected to show all database entries, then clear the screen and print them to the console.
            clear()
            print("Database entries: ")
            print(json.dumps(database_data["entries"], indent = 4)) # Display all of the entries in the current database.
            input("Press enter to continue...") # Wait for the user to press enter before continuing.
        elif (selection[0] == "n"): # If the user opted not to show all database entries, then simply skip and continue.
            print("Skipping...")
        else: # If the user entered an invalid selection, then show a notice that an invalid selection was made, then skip.
            print(style.yellow + "Warning: Invalid option." + style.end)
            print("Skipping...")
            input("Press enter to continue...") # Wait for the user to press enter before continuing.

        
    elif (selection == "4"): # The user has selected the "survey database" option.
        database_file = "" # Set the current selected database file name to a blank placeholder string.
        while (os.path.exists(root + "/" + database_file) == False or database_file == ""): # Run forever until the user enters a valid database file name.
            database_file = input("Database file name: ") # Prompt the user to enter the name of the database file they want to view.
            if (os.path.exists(root + "/" + database_file) == False): # Check to see if the database file entered by the user exists.
                print(style.yellow + "Warning: The database file name entered doesn't seem to exist in the root project folder. Please enter a valid file name." + style.end) # Inform the user that the file name they entered doesn't exist in the root project directory.

        database_data = json.load(open(root + "/" + database_file)) # Load the database information from the file specified by the user.
        while True: # Run forever in a loop until terminated.
            clear() # Clear the console output.
            print("Please select an option")
            print("0. Quit")
            print("1. Add Entry To " + str(database_data["name"]))
            selection = input("Selection: ") # Prompt the user to make a selection.

            if (selection == "0"): # The user has selected the "quit" option from the survey menu in survey mode.
                break # Break the loop to return to the main survey mode menu.
            elif (selection == "1"): # The user has selected to add an enty to the database.

                if (gps_enabled == True): # Check to see if GPS features are enabled in the configuration.
                    current_location = get_gps_location() # Get the current GPS location before prompting the user to fill out each element for this entry.

                entry_data = {} # Create a placeholder dictionary for all of the elements for the new entry.

                if (gps_enabled == True): # Check to see if GPS features are enabled.
                    entry_data["latitude"] = str(current_location[0]) # Record the current GPS latitude.
                    entry_data["longitude"] = str(current_location[1]) # Record the current GPS longitude.
                else: # If GPS features are disabled, then manually prompt the user for the current position.
                    entry_data["latitude"] = float(input("latitude (float): ")) # Prompt the user to enter a value for the current latitude.
                    entry_data["longitude"] = float(input("longitude (float): ")) # Prompt the user to enter a value for the current longitude.

                element_iteration_counter = 0 # Set the element iteration counter to 0 so it can be incremented by 1 each time an element is iterated through./
                for element in database_data["elements"]: # Iterate through each entry element specified in the database.
                    element_input = input(str(element) + " (" + database_data["elements"][element] + "): ") # Prompt the user to enter a value for this entry element.
                    if (database_data["elements"][element] == "str"): # If this element is supposed to be a string, then convert the user's input to a string.
                        entry_data[element] = str(element_input) # Save the user's input to the data for this entry.
                    elif (database_data["elements"][element] == "int"): # If this element is supposed to be an integer, then convert the user's input to an integer.
                        entry_data[element] = int(element_input) # Save the user's input to the data for this entry.
                    elif (database_data["elements"][element] == "float"): # If this element is supposed to be a floating point number, then convert the user's input to a float.
                        entry_data[element] = float(element_input) # Save the user's input to the data for this entry.
                    elif (database_data["elements"][element] == "bool"): # If this element is supposed to be a boolean value, then convert the user's input to a bool.
                        if (element_input[0].lower() == "t" or element_input[0].lower() == "y"): # The user has entered an input indicating "true".
                            entry_data[element] = True # Save the user's input to the data for this entry.
                        elif (element_input[0].lower() == "f" or element_input[0].lower() == "n"): # The user has entered an input indicating "false".
                            entry_data[element] = False # Save the user's input to the data for this entry.


                database_data["entries"].append(entry_data) # Add the data for this entry to the main database.
                database_data["modified"] = str(round(time.time())) # Update the "last modified" time in the database.
                save_to_file(str(root) + "/" + str(database_file), str(json.dumps(database_data, indent = 4)), silence_file_saving) # Save the database entry additions to disk as JSON data.

            else: # The user has selected an invalid option in the survey mode survey menu.
                print(style.yellow + "Warning: Invalid selection" + style.end)
                input("Press enter to continue...")


    else: # The user has selected an invalid option in the survey mode main menu.
        print(style.yellow + "Warning: Invalid selection" + style.end)
        input("Press enter to continue...")
