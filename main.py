# Assassin

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Assassin...")


import utils # Import the utils.py scripts.
debug_message = utils.debug_message # Load the function to print debugging information when the configuration says to do so.
load_config = utils.load_config # Load the function used to load the configuration.


debug_message("Starting loading")


import os # Required to interact with certain operating system functions
import json # Required to process JSON data


assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Assassin directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.
config = load_config()



import time # Required to add delays and handle dates/times
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
import math # Required to run more complex math functions.
import random # Required to generate random numbers.


if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only import the Bluetooth library if Bluetooth monitoring is enabled.
    debug_message("Importing `bluetooth` library")
    import bluetooth


# Load the rest of the utility functions from utils.py
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
get_distance = utils.get_distance # Load the function to get the distance between to global positions.
calculate_bearing = utils.calculate_bearing # Load the function used to calculate the bearing between two coordinate pairs.
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
get_arrow_direction = utils.get_arrow_direction # Load the function used to convert headings from degrees to arrow directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.
fetch_aircraft_data = utils.fetch_aircraft_data # Load the function used to fetch aircraft data from a Dump1090 CSV file.
debug_message("Imported `utils.py`")





# Load functionality plugins

# Load the traffic camera alert system
if (config["general"]["alert_range"]["traffic_cameras"] > 0 and config["general"]["gps_enabled"] == True): # Only load traffic enforcement camera information if traffic camera alerts are enabled.
    import trafficcameras
    load_traffic_camera_database = trafficcameras.load_traffic_camera_database
    traffic_camera_alert_processing = trafficcameras.traffic_camera_alert_processing

    loaded_traffic_camera_database = load_traffic_camera_database()


# Load the ADS-B aircraft alert system.
if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only load the ADS-B system if ADS-B alerts are enabled.
    import aircraft
    adsb_alert_processing = aircraft.adsb_alert_processing


# Load the drone/autonomous threat alert system.
if (config["general"]["drone_alerts"]["enabled"] == True): # Only load drone processing if drone alerts are enabled.
    import drones
    drone_alert_processing = drones.drone_alert_processing
    load_drone_alerts = drones.load_drone_alerts

    drone_threat_history, radio_device_history, drone_threat_database = load_drone_alerts()
    detected_drone_hazards = []


# Load the relay alert system.
if (config["general"]["relay_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only load relay alerts if relay alerts are enabled.
    import relay
    relay_alert_processing = relay.relay_alert_processing
    load_relay_alerts = relay.load_relay_alerts

    load_relay_alerts()


# Load the ALPR camera alert system.
if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps_enabled"] == True): # Only load ALPR camera information if ALPR alerts are enabled.
    import alprcameras
    load_alpr_camera_database = alprcameras.load_alpr_camera_database
    alpr_camera_alert_processing = alprcameras.alpr_camera_alert_processing

    loaded_alpr_camera_database = load_alpr_camera_database()


# Load the Bluetooth device alert system. 
if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only load Bluetooth monitoring system if Bluetooth monitoring is enabled.
    import bluetoothdevices
    load_bluetooth_log_file = bluetoothdevices.load_bluetooth_log_file
    bluetooth_alert_processing = bluetoothdevices.bluetooth_alert_processing

    detected_bluetooth_devices = load_bluetooth_log_file() # Load the detected Bluetooth device history.







# Display the startup intro header.
clear() # Clear the screen.
debug_message("Completed loading")
if (config["display"]["ascii_art_header"] == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
    print(style.red + style.bold)
    print("    _   ___ ___   _   ___ ___ ___ _  _ ")
    print("   /_\ / __/ __| /_\ / __/ __|_ _| \| |")
    print("  / _ \\\\__ \__ \/ _ \\\\__ \__ \| || .` |")
    print(" /_/ \_\___/___/_/ \_\___/___/___|_|\_|")
    print(style.end)

else: # If the user his disabled the large ASCII art header, then show a simple title header with minimal styling.
    print(style.red + style.bold + "ASSASSIN" + style.end)


if (config["display"]["custom_startup_message"] != ""): # Only display the line for the custom message if the user has defined one.
    print(config["display"]["custom_startup_message"]) # Show the user's custom defined start-up message.


time.sleep(1) # Wait two seconds to allow the start-up logo to remain on-screen for a moment.





play_sound("startup")





active_alarm = "none" # Set the active alert indicator variable to a placeholder before starting the main loop.
current_location = [] # Set the current location variable to a placeholder before starting the main loop.


debug_message("Starting main loop")

while True: # Run forever in a loop until terminated.
    debug_message("Cycle started")
    if (config["general"]["active_config_refresh"] == True): # Check to see if the configuration indicates to actively refresh the configuration during runtime.
        config = json.load(open(assassin_root_directory + "/config.json")) # Load the configuration database from config.json
        debug_message("Reloaded configuration")




    # Process all information that needs to be handled at the beginning of each cycle to prevent delays in the middle of the displaying process.


    # Get the current location.
    if (config["general"]["gps_enabled"] == True): # If GPS is enabled, then get the current location at the beginning of the cycle.
        last_location = current_location # Set the last location to the current location immediately before we update the current location for the next cycle.
        if ("current_location_time" in locals()  == True): # Check to see if the current location time variable exists. This variable will not exist on the first cycle.
            last_location_time = current_location_time # Record when the last location was received before recording the next location.
        current_location = get_gps_location() # Get the current location.
        current_location_time = time.time() # Record when this location was received.
        current_speed = round(convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"])*10**int(config["display"]["displays"]["speed"]["decimal_places"]))/(10**int(config["display"]["displays"]["speed"]["decimal_places"])) # Convert the speed data from the GPS into the units specified by the configuration.
    else: # GPS functionality is disabled.
        current_location = [0.0000, 0.0000, 0.0, 0.0, 0.0, 0] # Set the current location to a placeholder. This should be unnecessary, but this will prevent fatal errors if the current location is unexpectedly called despite GPS functionality being disabled.



    # Run traffic enforcement camera alert processing
    if (config["general"]["alert_range"]["traffic_cameras"] > 0 and config["general"]["gps_enabled"] == True): # Only run traffic enforcement camera alert processing if traffic camera alerts are enabled.
        nearest_enforcement_camera, nearest_speed_camera, nearest_redlight_camera, nearest_misc_camera = traffic_camera_alert_processing(current_location, loaded_traffic_camera_database)


    # Run ALPR camera alert processing
    if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps_enabled"] == True): # Only run ALPR camera processing if ALPR alerts are enabled.
        nearest_alpr_camera, nearby_alpr_cameras = alpr_camera_alert_processing(current_location, loaded_alpr_camera_database)


    # Run drone alert processing
    if (config["general"]["drone_alerts"]["enabled"] == True): # Only run drone processing if drone alerts are enabled.
        detected_drone_hazards = drone_alert_processing(radio_device_history, drone_threat_database, detected_drone_hazards)


    # Run relay-based alert processing.
    if (config["general"]["relay_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only run relay alert processing if relay alerts are enabled.
        active_relay_alerts = relay_alert_processing()


    # Run Bluetooth alert processing.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only run Bluetooth monitoring processing if Bluetooth monitoring is enabled.
        detected_bluetooth_devices, bluetooth_threats = bluetooth_alert_processing(current_location, detected_bluetooth_devices)
    elif (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps_enabled"] == False): # If GPS functionality is disabled, then run Bluetooth monitoring without GPS information.
        detected_bluetooth_devices, bluetooth_threats = bluetooth_alert_processing([0.0000, 0.0000, 0.0, 0.0, 0.0, 0], detected_bluetooth_devices) # Run the Bluetooth alert processing function with dummy GPS data.


    # Process ADS-B alerts.
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only run ADS-B alert processing if it is enabled in the configuration.
        aircraft_threats, aircraft_data = adsb_alert_processing(current_location)


    debug_message("Alert processing completed")


    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.


    clear() # Clear the console output at the beginning of every cycle.






    # Display any critical alarm messages that the user should know about as soon as possible.
    if (active_alarm == "speedcameralimitexceeded"):
        if (config["display"]["large_critical_display"] == True):
            print(style.red + style.bold)
            print(" $$$$$$\\  $$\\       $$$$$$\\  $$\\      $$\\       $$$$$$$\\   $$$$$$\\  $$\\      $$\\ $$\\   $$\\ ")
            print("$$  __$$\\ $$ |     $$  __$$\\ $$ | $\\  $$ |      $$  __$$\\ $$  __$$\\ $$ | $\\  $$ |$$$\\  $$ |")
            print("$$ /  \\__|$$ |     $$ /  $$ |$$ |$$$\\ $$ |      $$ |  $$ |$$ /  $$ |$$ |$$$\\ $$ |$$$$\\ $$ |")
            print("\\$$$$$$\\  $$ |     $$ |  $$ |$$ $$ $$\\$$ |      $$ |  $$ |$$ |  $$ |$$ $$ $$\\$$ |$$ $$\\$$ |")
            print(" \\____$$\\ $$ |     $$ |  $$ |$$$$  _$$$$ |      $$ |  $$ |$$ |  $$ |$$$$  _$$$$ |$$ \\$$$$ |")
            print("$$\\   $$ |$$ |     $$ |  $$ |$$$  / \\$$$ |      $$ |  $$ |$$ |  $$ |$$$  / \\$$$ |$$ |\\$$$ |")
            print("\\$$$$$$  |$$$$$$$$\ $$$$$$  |$$  /   \\$$ |      $$$$$$$  | $$$$$$  |$$  /   \\$$ |$$ | \$$ |")
            print(" \\______/ \________|\\______/ \\__/     \\__|      \\_______/  \\______/ \\__/     \\__|\\__|  \\__|")
            print(style.red + "SPEED CAMERA LIMIT EXCEEDED" + style.end)
            print(style.end)
        else:
            print(style.red + style.bold + "SLOW DOWN" + style.end)
            print(style.red + "SPEED CAMERA LIMIT EXCEEDED" + style.end)




    active_alarm = "none" # Reset the active alert to none at the beginning of each session.






    # Show all configured basic information displays.

    debug_message("Displaying basic dashboard")

    if (config["display"]["displays"]["speed"]["large_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the large speed display is enabled in the configuration.
        current_speed = convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
        current_speed = round(current_speed * 10**int(config["display"]["displays"]["speed"]["decimal_places"]))/10**int(config["display"]["displays"]["speed"]["decimal_places"]) # Round off the current speed to a certain number of decimal places as specific in the configuration.
        display_number(current_speed) # Display the current speed in a large ASCII font.

    if (config["display"]["displays"]["time"] == True): # Check to see the time display is enabled in the configuration.
        print("Time: " + str(time.strftime('%H:%M:%S'))) # Print the current time to the console.

    if (config["display"]["displays"]["date"]  == True): # Check to see the date display is enabled in the configuration.
        print("Date: " + str(time.strftime('%A, %B %d, %Y'))) # Print the current date to the console.

    if (config["display"]["displays"]["speed"]["small_display"] == True and config["general"]["gps_enabled"] == True): # Check to see the small speed display is enabled in the configuration.
        print("Speed: " + str(current_speed) + " " + str(config["display"]["displays"]["speed"]["unit"])) # Print the current speed to the console.

    if (config["display"]["displays"]["location"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current location display is enabled in the configuration.
        print("Position: " + str(current_location[0]) + " " + str(current_location[1])) # Print the current location as coordinates to the console.

    if (config["display"]["displays"]["altitude"] == True and config["general"]["gps_enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
        print("Altitude: " + str(current_location[3]) + " meters") # Print the current altitude to the console.

    if ((config["display"]["displays"]["heading"]["degrees"] == True or config["display"]["displays"]["heading"]["direction"] == True) and config["general"]["gps_enabled"] == True): # Check to see if the current heading display is enabled in the configuration.
        if (config["display"]["displays"]["heading"]["direction"] == True and config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees are both enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4])) + " (" + str(current_location[4]) + "°)") # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["direction"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees is enabled.
            print("Heading: " + str(get_cardinal_direction(current_location[4]))) # Print the current heading to the console in cardinal directions.
        elif (config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in degrees is enabled.
            print("Heading: " + str(current_location[4]) + "°") # Print the current heading to the console in degrees.

    if (config["display"]["displays"]["satellites"] == True and config["general"]["gps_enabled"] == True): # Check to see if the satellite display is enabled in the configuration.
        print("Satellites: " + str(current_location[5])) # Print the current altitude satellite count to the console.
    if (config["display"]["displays"]["planes"] == True and config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Check to see if the plane count display is enabled in the configuration.
        print("Planes: " + str(len(aircraft_data))) # Print the current detected plane count to the console.




    # Display relay-based alerts.
    if (config["general"]["relay_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Only display relay-based alerts if relay alerts are enabled in the configuration.
        debug_message("Displaying relay alerts")
        for alert in active_relay_alerts: # Iterate through each active alert, and print it to the screen.
            print(style.green + alert["title"])
            print("    " + alert["message"] + style.end)




    # Display Bluetooth monitoring alerts.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only conduct Bluetooth alert processing if Bluetooth alerts and GPS features are enabled in the configuration.
        debug_message("Displaying Bluetooth alerts")

        if (len(bluetooth_threats) > 0):
            for threat in bluetooth_threats: # Iterate through all of the active Bluetooth threats.
                active_bluetooth_alert = True # Change the current alert status to 'active'.
                print(f"{style.pink}{threat['address']} ({threat['name']}) has been following for {threat['distance_followed']:.4f} miles over the past {str(int(threat['lastseentime']) - int(threat['firstseentime']))} seconds.{style.end}") # Print a notice containing the device that is following, as well has how far and how long the device has been detected.


            display_shape("square") # Display an ASCII square in the console output to represent a device, if Assassin is configured to do so.

            play_sound("bluetooth") # Play the alert sound associated with Bluetooth alerts, if one is configured to run.
            



    # Display traffic camera alerts.
    if (config["general"]["gps_enabled"] == True and float(config["general"]["alert_range"]["traffic_cameras"]) > 0 and "nearest_enforcement_camera" in locals()): # Check to see if the speed camera display is enabled in the configuration.
        debug_message("Displaying traffic enforcement camera alerts")
        # Display the nearest traffic camera, if applicable.
        if (nearest_enforcement_camera["dst"] < float(config["general"]["alert_range"]["traffic_cameras"])): # Only display the nearest camera if it's within the maximum range specified in the configuration.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("enforcementcamera") # Run the function to update the status lighting.


            print(style.blue)
            print("Nearest Enforcement Camera:")
            if (nearest_enforcement_camera == nearest_speed_camera): # Check to see if the overall nearest camera is the nearest speed camera.
                print("    Type: Speed Camera")
            elif (nearest_enforcement_camera == nearest_redlight_camera): # Check to see if the overall nearest camera is the nearest red light camera.
                print("    Type: Red Light Camera")
            elif (nearest_enforcement_camera == nearest_misc_camera): # Check to see if the overall nearest camera is the nearest general traffic camera.
                print("    Type: General Traffic Camera")
            else:
                print("    Type: Unknown")
            print("    Location: " + str(nearest_enforcement_camera["lat"]) + ", " + str(nearest_enforcement_camera["lon"])) # Display the location of the traffic camera.
            print("    Distance: " + str(round(nearest_enforcement_camera["dst"]*1000)/1000) + " miles") # Display the current distance to the traffic camera.
            if (nearest_enforcement_camera["str"] != None): # Check to see if street data exists for this camera.
                print("    Street: " + str(nearest_enforcement_camera["str"])) # Display the street that the traffic camera is on.
            if (nearest_enforcement_camera["spd"] != None): # Check to see if speed limit data exists for this camera.
                print("    Speed: " + str(round(int(nearest_enforcement_camera["spd"]) * 0.6213712))) # Display the speed limit of the traffic camera, converted to miles per hour.
            print(style.end + style.end)


            display_shape("circle") # Display an ASCII circle in the console output, if Assassin is configured to do so.

            # Play audio alerts, as necessary.
            if (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.1)): # Check to see if the nearest camera is within 10% of the traffic camera alert radius.
                if (nearest_enforcement_camera["spd"] != None and config["general"]["traffic_camera_speed_check"] == True): # Check to see if speed limit data exists for this speed camera, and if the traffic camera speed check setting is enabled in the configuration.
                    if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then play a heightened alarm sound.
                        play_sound("alarm")

                play_sound("camera3")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]) * 0.25)): # Check to see if the nearest camera is within 25% of the traffic camera alert radius.
                play_sound("camera2")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["alert_range"]["traffic_cameras"]))): # Check to see if the nearest camera is within the traffic camera alert radius.
                play_sound("camera1")




    # Display ALPR camera alerts.
    if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps_enabled"] == True): # Only display nearby ALPR camera alerts if they are enabled.
        if (len(nearby_alpr_cameras) > 0): # Only iterate through the nearby cameras if there are any nearby cameras to begin with.
            debug_message("Displaying ALPR camera alerts")

            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("alprcamera") # Run the function to update the status lighting.

            print(style.purple)
            print("Active " + loaded_alpr_camera_database["name"] + " Alerts: " + str(len(nearby_alpr_cameras))) # Display the number of active ALPR alerts.
            print("    Nearest:")
            print("        Distance: " + str(round(nearest_alpr_camera["distance"]*1000)/1000) + " miles") # Display the distance to this POI.
            print("        Street: " + str(nearest_alpr_camera["road"])) # Display the road that this POI is associated with.
            print("        Direction To: " + str(get_arrow_direction(nearest_alpr_camera["bearing"] - current_location[4])) + " " + str(round(nearest_alpr_camera["bearing"] - current_location[4])) + "°") # Display the direction towards this POI relative to the current direction of movement.
            print("        Bearing To: " + str(get_cardinal_direction(nearest_alpr_camera["bearing"])) + " " + str(round(nearest_alpr_camera["bearing"])) + "°") # Display the absolute bearing to this POI.
            if (nearest_alpr_camera["direction"] != ""): # Check to see if this POI has direction information.
                print("        Absolute Facing: " + str(nearest_alpr_camera["direction"]) + "°" + get_cardinal_direction(nearest_alpr_camera["direction"])) # Display the direction this camera is facing.
            if (nearest_alpr_camera["relativefacing"] != ""): # Check to see if this POI has relative direction information.
                print("        Relative Facing: " + str(get_arrow_direction(nearest_alpr_camera["relativefacing"])) + " " + str(round(nearest_alpr_camera["relativefacing"])) + "°") # Display the direction this camera is facing relative to the current direction of movement.
            print(style.end + style.end)

            display_shape("horizontal") # Display an ASCII horizontal bar in the console output, if Assassin is configured to do so.

            play_sound("alpr")




    # Display drone alerts.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
        debug_message("Displaying drone alerts")
        if (len(detected_drone_hazards) > 0): # Check to see if any hazards were detected this cycle.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("autonomousthreat") # Update the status lighting to indicate that at least one autonomous threat was detected.

            print(style.cyan + "Detected autonomous hazards:")
            for hazard in detected_drone_hazards: # Iterate through each detected hazard.
                print("    " + hazard["mac"] + "") # Show this hazard's MAC address.
                print("        Threat Type: " + hazard["threattype"]) # Show what kind of threat this device is.
                print("        Company: " + hazard["company"]) # Show company or brand that this hazard is associated with.
                print("        Name: " + hazard["name"]) # Show this hazard's name.
                print("        Last Seen: " + str(hazard["lastseen"])) # Show the timestamp that this hazard was last seen.
                print("        First Seen: " + str(hazard["firstseen"])) # Show the timestamp that this hazard was first seen.
                print("        Channel: " + hazard["channel"]) # Show this hazard's wireless channel.
                print("        Channel: " + hazard["packets"]) # Show this hazard's packet count.
                print("        Strength: " + str(hazard["strength"]) + "%") # Show this hazards relative signal strength.
                print("        Wireless Type: " + hazard["type"]) # Show this hazard's type.

                drone_threat_history.append(hazard) # Add this threat to the threat history.

            print(style.end) # End the font styling from the drone threat display.

            save_to_file(assassin_root_directory + "/drone_threat_history.json", str(json.dumps(drone_threat_history, indent = 4)), True) # Save the current drone threat history to disk.

            display_shape("cross") # Display an ASCII cross in the console output to represent a drone, if Assassin is configured to do so.

            play_sound("drone") # Play the sound effect associated with a potential drone threat being detected.




    # Display ADS-B aircraft alerts
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps_enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Displaying ADS-B alerts")
        if (len(aircraft_threats) > 0 and current_location[2] >= config["general"]["adsb_alerts"]["minimum_vehicle_speed"]): # Check to see if any threats were detected this cycle, and if the GPS speed indicates that the vehicle is travelling above the minimum alert speed.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("adsbthreat") # Update the status lighting to indicate that at least one ADS-B aircraft threat was detected.

            print(style.yellow + "Detected aircraft ADS-B threats:")
            for threat in aircraft_threats: # Iterate through each detected hazard.
                print("    " + threat["id"] + ":") # Show this hazard's MAC address.
                print("        Location: " + str(threat["latitude"]) + ", " + str(threat["longitude"]) + " (" + get_arrow_direction(threat["direction"]) + " " + str(round(threat["direction"])) + "°)") # Show the coordinates of this aircraft.
                print("        Distance: " + str(round(threat["distance"]*1000)/1000) + " miles") # Show the distance to this aircraft.
                print("        Threat Level: " + str(threat["threatlevel"])) # Show the distance to this aircraft.
                print("        Speed: " + str(threat["speed"]) + " knots") # Show the speed of this aircraft.
                print("        Altitude: " + str(threat["altitude"]) + " feet") # Show the altitude of this aircraft.
                print("        Absolute Heading: " + get_cardinal_direction(threat["heading"]) + " (" + str(threat["heading"]) + "°)") # Show the absolute heading of this aircraft.
                print("        Relative Heading: " + get_arrow_direction(threat["relativeheading"]) + " (" + str(threat["relativeheading"]) + "°)") # Show the direction of this aircraft relative to the current direction of movement.
                print("        Time: " + str(round((time.time() - float(threat["time"]))*100)/100) + " seconds ago") # Show how long it has been since this aircraft was detected.
                print("        Callsign: " + str(threat["callsign"])) # Show the callsign of this aircraft.
                print("        Climb: " + str(threat["climb"]) + " feet per minute") # Show the vertical climb rate of this aircraft.

            print(style.end) # End the font styling from the aircraft ADS-B threat display.

            display_shape("triangle") # Display an ASCII triangle in the console output to represent a plane, if Assassin is configured to do so.

            play_sound("adsb") # Play the sound effect associated with a potential ADS-B aircraft threat being detected.








    # Record telemetry data according to the configuration.
    if (config["general"]["record_telemetry"] == True): # Check to see if Assassin is configured to record telemetry data.
        debug_message("Recording telemetry data")
        if (config["general"]["gps_enabled"] == True): # Check to see if GPS features are enabled.
            export_data = str(round(time.time())) + "," + str(current_speed) + "," + str(current_location[0]) + "," + str(current_location[1]) + "," + str(current_location[3]) + "," + str(current_location[4]) + "," + str(current_location[5]) + "\n" # Add all necessary information to the export data.
        else:
            export_data = str(round(time.time())) + "," + str("0") + "," + str("0.000") + "," + str("0.000") + "," + str("0") + "," + str("0") + "," + str("0") + "\n" # Add all necessary information to the export data, using placeholders for information that depends on GPS.

        add_to_file(assassin_root_directory + "/information_recording.csv", export_data, True) # Add the export data to the end of the file and write it to disk.
        debug_message("Telemetry recorded")




    debug_message("Executing refresh delay")
    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
