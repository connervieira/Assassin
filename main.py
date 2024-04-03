# Assassin

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Assassin...")


import utils # Import the utils.py scripts.
debug_message = utils.debug_message # Load the function to print debugging information when the configuration says to do so.

import config
load_config = config.load_config
validate_config = config.validate_config

import sys
if ("--headless" in sys.argv):
    headless_mode = True
else:
    headless_mode = False

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



# Load the rest of the utility functions from utils.py
debug_message("Loading `utils.py` functions")
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
calculate_bearing = utils.calculate_bearing # Load the function used to calculate the bearing between two coordinate pairs.
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
get_arrow_direction = utils.get_arrow_direction # Load the function used to convert headings from degrees to arrow directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice # Load the function used to display notices, warnings, and errors.
process_timing = utils.process_timing # Load the function used to track how much time is spent doing various actions.
speak = utils.speak # Load the function used to play text-to-speech.
save_gpx = utils.save_gpx # Load the function used to save the location history to a GPX file.

save_to_file(config["external"]["local"]["interface_directory"] + "/alerts.json", "{}") # Wipe the alerts file before starting the loading process.


import gpslocation
get_gps_location = gpslocation.get_gps_location # Load the function to get the current GPS location.
process_gps_alerts = gpslocation.process_gps_alerts # Load the function used to detect GPS problems.

# Load the OBD integration system. 
obd_alerts = {}
obd_data = {}
if (config["general"]["obd_integration"]["enabled"] == True): # Only load OBD integration system if OBD integration is enabled.
    debug_message("Initializing OBD integration system")
    import obdintegration
    start_obd_monitoring = obdintegration.start_obd_monitoring
    fetch_obd_alerts = obdintegration.fetch_obd_alerts
    obd_connection = start_obd_monitoring()
else:
    obd_connection = None


display_notice("Acquiring initial GPS location", 1)
if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled before getting the initial location.
    debug_message("Acquiring initial location")
    initial_location = [0, 0] # Set the "current location" to a placeholder.
    attempts = 0 # This will be incremented each time Assassin attempts to get the current GPS location.
    while (initial_location[0] == 0 and initial_location[1] == 0): # Repeatedly attempt to get a GPS location until one is received.
        if (attempts >= 60):
            display_notice("Failed to get initial GPS location", 3)
            exit()
        if (attempts > 0): # If the GPS previously failed to get a lock, then wait 2 seconds before trying again.
            time.sleep(1) # Wait 1 second to give the GPS time to get a lock.
            display_notice("Retrying to get initial GPS location (" + str(attempts) + ")", 1)
        attempts += 1

        previous_gps_attempt = True
        initial_location = get_gps_location() # Attempt to get the current GPS location.



debug_message("Validating configuration values")
invalid_configuration_values = validate_config(config) # Validation the configuration, and display any potential problems.
for entry in invalid_configuration_values: # Iterate through each invalid configuration value in the list.
    display_notice("Invalid configuration value: " + entry, 2) # Print each invalid configuration value as a warning.
del invalid_configuration_values # Delete the variable holding the list of invalid configuration_values.
debug_message("Validated configuration values")



# Load functionality plugins

display_notice("Loading alert plugins", 1)
# Load the traffic camera alert system
if (config["general"]["traffic_camera_alerts"]["triggers"]["distance"] > 0 and config["general"]["gps"]["enabled"] == True): # Only load traffic enforcement camera information if traffic camera alerts are enabled.
    debug_message("Initializing traffic camera alert system")
    import trafficcameras
    load_traffic_camera_database = trafficcameras.load_traffic_camera_database
    traffic_camera_alert_processing = trafficcameras.traffic_camera_alert_processing

    if (config["general"]["traffic_camera_alerts"]["enabled"] == True):
        loaded_traffic_camera_database = load_traffic_camera_database(initial_location)


# Load the ADS-B aircraft alert system.
if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only load the ADS-B system if ADS-B alerts are enabled.
    debug_message("Initializing aircraft alert system")
    import aircraft
    start_adsb_monitoring = aircraft.start_adsb_monitoring
    adsb_alert_processing = aircraft.adsb_alert_processing

    start_adsb_monitoring()


# Load the Bluetooth monitoring system.
if (config["general"]["bluetooth_scanning"]["enabled"] == True):
    import bluetooth
    bluetooth.start_bluetooth_scanning()



# Load the drone/autonomous threat alert system.
if (config["general"]["drone_alerts"]["enabled"] == True): # Only load drone processing if drone alerts are enabled.
    debug_message("Initializing drone alert system")
    import drones
    drone_alert_processing = drones.drone_alert_processing
    load_drone_alerts = drones.load_drone_alerts

    drone_threat_history, radio_device_history, drone_threat_database = load_drone_alerts()
    detected_drone_hazards = []


# Load the ALPR camera alert system.
if (config["general"]["alpr_alerts"]["enabled"] == True): # Only load ALPR camera information if ALPR alerts are enabled.
    debug_message("Initializing ALPR camera system")
    import alprcameras
    load_alpr_camera_database = alprcameras.load_alpr_camera_database
    alpr_camera_alert_processing = alprcameras.alpr_camera_alert_processing

    loaded_alpr_camera_database = load_alpr_camera_database(initial_location)



# Load the weather alert system. 
if (config["general"]["weather_alerts"]["enabled"] == True): # Only load weather alert system if weather alerts are enabled.
    debug_message("Initializing weather alert system")
    import weather
    get_weather_data = weather.get_weather_data
    weather_alert_processing = weather.weather_alert_processing
    weather_data = { "requested" : 0 } # Set the current weather information to a placeholder.
    last_weather_data = { "requested" : 0 } # Set the last round's weather information to a placeholder.


# Load the attention alert system. 
if (config["general"]["attention_monitoring"]["enabled"] == True): # Only load attention monitoring system if attention alerts are enabled.
    debug_message("Initializing attention monitoring system")
    import attention
    process_attention_alerts = attention.process_attention_alerts
    get_current_attention_time = attention.get_current_attention_time
    attention_alerts = {}

# Load Predator integration.
if (config["general"]["predator_integration"]["enabled"] == True): # Only load Predator integration if Predator integration is enabled in the configuration.
    import predator
    start_predator = predator.start_predator
    process_predator_alerts = predator.process_predator_alerts

    start_predator()







# Display the startup intro header.
clear() # Clear the screen.
display_notice("Loading complete", 1)
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


if (headless_mode == False):
    time.sleep(1) # Wait briefly to allow the start-up logo to remain on-screen for a moment.




play_sound("startup")
speak("Assassin has completed loading", "Loading complete")





current_location = [] # Set the current location variable to a placeholder before starting the main loop.

# Set placeholders for all the complete alert dictionary.
all_alerts = {}

# Set placeholders for all the alert counters.
alert_count = {}
alert_count["drone"] = [0, 0]
alert_count["aircraft"] = [0, 0]
alert_count["traffic_camera"] = [0, 0]
alert_count["alpr"] = [0, 0]
alert_count["weather"] = [0, 0]
alert_count["gps"] = [0, 0]
alert_count["obd"] = [0, 0]
alert_count["attention"] = [0, 0]
alert_count["bluetooth"] = [0, 0]
alert_count["predator"] = [0, 0]

location_history = []

debug_message("Starting main loop")

while True: # Run forever in a loop until terminated.
    debug_message("Cycle started")
    play_sound("heartbeat")
    if (config["general"]["active_config_refresh"] == True): # Check to see if the configuration indicates to actively refresh the configuration during runtime.
        config = load_config() # Reload the configuration.
        debug_message("Reloaded configuration")




    # Process all information that needs to be handled at the beginning of each cycle to prevent delays in the middle of the displaying process.


    # Get the current location.
    if (config["general"]["gps"]["enabled"] == True): # If GPS is enabled, then get the current location at the beginning of the cycle.
        current_location = get_gps_location(location_history, obd_data) # Get the current location.
        current_speed = convert_speed(float(current_location[2])) # Convert the speed data from the GPS into the units specified by the configuration.
    else: # GPS functionality is disabled.
        current_location = [0.0000, 0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Set the current location to a placeholder.

    location_history.append({"lat" : current_location[0], "lon" : current_location[1], "spd" : current_location[2], "alt" : current_location[3], "hdg": current_location[4], "sat" : current_location[5], "time" : time.time(), "src": current_location[6]})# Add the most recently recorded location to the beginning of the location history list.



    # Run GPS alert processing.
    if (config["general"]["gps"]["alerts"]["enabled"] == True and config["general"]["gps"]["enabled"]): # Check to make sure GPS alerts are enabled before processing alerts.
        process_timing("Alerts/GPS", "start")
        gps_alerts = process_gps_alerts(location_history) # Process GPS alerts.
        process_timing("Alerts/GPS", "end")
    else: # GPS alert detection is disabled.
        gps_alerts = {} # Return a blank placeholder dictionary in place of the true alerts.


    # Run traffic enforcement camera alert processing.
    if (config["general"]["traffic_camera_alerts"]["enabled"] == True):
        process_timing("Alerts/Traffic Enforcement Cameras", "start")
        nearby_cameras_all = traffic_camera_alert_processing(current_location, loaded_traffic_camera_database)
        process_timing("Alerts/Traffic Enforcement Cameras", "end")
    else:
        nearby_cameras_all = []


    # Run ALPR camera alert processing.
    if (config["general"]["alpr_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run ALPR camera processing if ALPR alerts are enabled.
        process_timing("Alerts/License Plate Recognition Cameras", "start")
        nearest_alpr_camera, nearby_alpr_cameras = alpr_camera_alert_processing(current_location, loaded_alpr_camera_database)
        process_timing("Alerts/License Plate Recognition Cameras", "end")
    else:
        nearest_alpr_camera, nearby_alpr_cameras = {}, []


    # Run drone alert processing.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Only run drone processing if drone alerts are enabled.
        process_timing("Alerts/Drones", "start")
        detected_drone_hazards = drone_alert_processing(radio_device_history, drone_threat_database, detected_drone_hazards)
        process_timing("Alerts/Drones", "end")
    else:
        detected_drone_hazards = []



    # Process ADS-B alerts.
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run ADS-B alert processing if it is enabled in the configuration.
        process_timing("Alerts/Aircraft", "start")
        aircraft_threats, aircraft_data = adsb_alert_processing(current_location, current_speed)
        process_timing("Alerts/Aircraft", "end")
    else:
        aircraft_threats, aircraft_data = [], {}


    # Process weather alerts.
    if (config["general"]["weather_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run weather alert processing if it is enabled in the configuration.
        process_timing("Alerts/Weather", "start")
        last_weather_data = weather_data
        weather_data = get_weather_data(current_location, last_weather_data)
        process_timing("Alerts/Weather", "end")
        weather_alerts = weather_alert_processing(weather_data)
    else:
        weather_alerts = {}

    # Process attention alerts.
    if (config["general"]["obd_integration"]["enabled"] == True): # Only run OBD integration alert processing if it is enabled in the configuration.
        process_timing("Alerts/OBD", "start")
        obd_alerts, obd_data = fetch_obd_alerts(obd_connection)
        process_timing("Alerts/OBD", "end")
    else:
        obd_alerts = {}


    # Process attention alerts.
    if (config["general"]["attention_monitoring"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run attention monitoring alert processing if it is enabled in the configuration.
        process_timing("Alerts/Attention", "start")
        attention_alerts = process_attention_alerts(float(current_speed))
        process_timing("Alerts/Attention", "end")
    else:
        attention_alerts = {}


    # Process Bluetooth alerts.
    if (config["general"]["bluetooth_scanning"]["enabled"] == True): # Only run Bluetooth monitoring processing if it is enabled in the configuration.
        process_timing("Alerts/Bluetooth", "start")
        bluetooth_devices_new = bluetooth.get_latest_bluetooth_le()
        bluetooth_alerts = bluetooth.process_bluetooth_alerts(bluetooth_devices_new, current_location)
        bluetooth_devices = bluetooth.get_all_bluetooth_devices()
        process_timing("Alerts/Bluetooth", "end")
    else:
        bluetooth_devices = {}
        bluetooth_alerts = {}


    if (config["general"]["predator_integration"]["enabled"] == True): # Process Predator alerts.
        process_timing("Alerts/Predator", "start")
        predator_alerts = process_predator_alerts()
        process_timing("Alerts/Predator", "end")
    else:
        predator_alerts = {}
        



    debug_message("Alert processing completed")

    update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.







    # Collect all alerts.
    process_timing("Organization/Alerts", "start")
    all_alerts = dict(list(all_alerts.items())[-10:]) # Trim the dictionary of all alerts to the last 10 entries.
    current_time = time.time() # Get the current time.
    all_alerts[current_time] = {}
    all_alerts[current_time]["drone"] = detected_drone_hazards
    all_alerts[current_time]["aircraft"] = aircraft_threats
    all_alerts[current_time]["traffic_camera"] = nearby_cameras_all
    all_alerts[current_time]["alpr"] = nearby_alpr_cameras
    all_alerts[current_time]["weather"] = weather_alerts
    all_alerts[current_time]["gps"] = gps_alerts
    all_alerts[current_time]["obd"] = obd_alerts
    all_alerts[current_time]["attention"] = attention_alerts
    all_alerts[current_time]["bluetooth"] = bluetooth_alerts
    all_alerts[current_time]["predator"] = predator_alerts


    if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
        save_to_file(config["external"]["local"]["interface_directory"] + "/alerts.json", json.dumps(all_alerts)) # Save all current alerts to disk.


    # Record the number of active alerts.
    alert_count["drone"] = [len(detected_drone_hazards)] + alert_count["drone"]
    alert_count["aircraft"] = [len(aircraft_threats)] + alert_count["aircraft"]
    alert_count["traffic_camera"] = [len(nearby_cameras_all)] + alert_count["traffic_camera"]
    alert_count["alpr"] = [len(nearby_alpr_cameras)] + alert_count["alpr"]
    alert_count["weather"] = [len(weather_alerts)] + alert_count["weather"]
    alert_count["gps"] = [len(gps_alerts)] + alert_count["gps"]
    alert_count["obd"] = [len(obd_alerts)] + alert_count["obd"]
    alert_count["attention"] = [len(attention_alerts)] + alert_count["attention"]
    alert_count["bluetooth"] = [len(bluetooth_alerts)] + alert_count["bluetooth"]
    alert_count["predator"] = [len(predator_alerts)] + alert_count["predator"]


    # Only keep alert counts from the past 10 cycles.
    alert_count["drone"] = alert_count["drone"][:10]
    alert_count["aircraft"] = alert_count["aircraft"][:10]
    alert_count["traffic_camera"] = alert_count["traffic_camera"][:10]
    alert_count["alpr"] = alert_count["alpr"][:10]
    alert_count["weather"] = alert_count["weather"][:10]
    alert_count["gps"] = alert_count["gps"][:10]
    alert_count["attention"] = alert_count["attention"][:10]
    alert_count["bluetooth"] = alert_count["bluetooth"][:10]
    alert_count["predator"] = alert_count["predator"][:10]


    process_timing("Organization/Alerts", "end")




    # Alert the user via text-to-speech, as necessary.
    if (config["audio"]["tts"]["enabled"] == True): # Check to make sure text-to-speech is enabled before doing any processing.
        debug_message("Running text-to-speech processing")
        process_timing("Audio/TTS", "start")

        # Process drone text to speech alerts.
        if (alert_count["drone"][0] > alert_count["drone"][1]):
            speak("New drone alert", "Drone")

        # Process aircraft text to speech alerts.
        if (alert_count["aircraft"][0] > alert_count["aircraft"][1]):
            speak("New aircraft alert. " + str(round(aircraft_threats[0]["distance"]*10)/10) + " miles", "Aircraft")

        # Process traffic camera text to speech alerts.
        if (alert_count["traffic_camera"][0] > alert_count["traffic_camera"][1]):
            speak("New traffic camera alert. " + str(round(nearby_cameras_all[0]["dst"]*10)/10) + " miles", "Traffic camera")

        # Process ALPR text to speech alerts.
        if (alert_count["alpr"][0] > alert_count["alpr"][1]):
            speak("New A. L. P. R. Alert. " + str(round(nearest_alpr_camera["distance"]*10)/10) + " miles", "A. L. P. R")

        # Process weather text to speech alerts.
        if (alert_count["weather"][0] > alert_count["weather"][1]):
            speak("New weather alert", "Weather")

        # Process GPS text to speech alerts.
        if (alert_count["gps"][0] > alert_count["gps"][1]):
            speak("New GPS alert", "GPS")

        # Process attention text to speech alerts.
        if (alert_count["attention"][0] > alert_count["attention"][1]):
            speak("Attention threshold reached", "Attention")

        # Process Bluetooth text to speech alerts.
        if (alert_count["bluetooth"][0] > alert_count["bluetooth"][1]):
            speak("Bluetooth device threat", "Bluetooth")


        # Process Predator text to speech alerts.
        if (alert_count["predator"][0] > alert_count["predator"][1]):
            speak("Predator license plate hit", "Predator")

        process_timing("Audio/TTS", "end")
        debug_message("Completed Text-to-speech processing")










    clear() # Clear the console output at the beginning of every cycle.









    # Show all configured basic information displays.
    if (config["display"]["silence_console_displays"] == False):
        debug_message("Displaying basic dashboard")
        process_timing("Displays", "start")

        if (config["display"]["displays"]["speed"]["large_display"] == True and config["general"]["gps"]["enabled"] == True): # Check to see the large speed display is enabled in the configuration.
            current_speed = convert_speed(float(current_location[2])) # Convert the speed data from the GPS into the units specified by the configuration.
            current_speed = round(current_speed * 10**int(config["display"]["displays"]["speed"]["decimal_places"]))/10**int(config["display"]["displays"]["speed"]["decimal_places"]) # Round off the current speed to a certain number of decimal places as specific in the configuration.
            display_number(current_speed) # Display the current speed in a large ASCII font.

        if (config["display"]["displays"]["time"] == True): # Check to see the time display is enabled in the configuration.
            print("Time: " + str(time.strftime('%H:%M:%S'))) # Print the current time to the console.

        if (config["display"]["displays"]["date"]  == True): # Check to see the date display is enabled in the configuration.
            print("Date: " + str(time.strftime('%A, %B %d, %Y'))) # Print the current date to the console.

        if (config["display"]["displays"]["speed"]["small_display"] == True and config["general"]["gps"]["enabled"] == True): # Check to see the small speed display is enabled in the configuration.
            print("Speed: " + str(current_speed) + " " + str(config["display"]["displays"]["speed"]["unit"])) # Print the current speed to the console.

        if (config["display"]["displays"]["location"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if the current location display is enabled in the configuration.
            print("Position: " + str(current_location[0]) + " " + str(current_location[1])) # Print the current location as coordinates to the console.

        if (config["display"]["displays"]["altitude"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if the current altitude display is enabled in the configuration.
            print("Altitude: " + str(round(current_location[3]*100)/100) + " meters") # Print the current altitude to the console.

        if ((config["display"]["displays"]["heading"]["degrees"] == True or config["display"]["displays"]["heading"]["direction"] == True) and config["general"]["gps"]["enabled"] == True): # Check to see if the current heading display is enabled in the configuration.
            if (config["display"]["displays"]["heading"]["direction"] == True and config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees are both enabled.
                print("Heading: " + str(get_cardinal_direction(current_location[4])) + " (" + str(round(current_location[4])) + "°)") # Print the current heading to the console in cardinal directions.
            elif (config["display"]["displays"]["heading"]["direction"] == True): # Check to see if the configuration value to display the current heading in cardinal directions and degrees is enabled.
                print("Heading: " + str(get_cardinal_direction(current_location[4]))) # Print the current heading to the console in cardinal directions.
            elif (config["display"]["displays"]["heading"]["degrees"] == True): # Check to see if the configuration value to display the current heading in degrees is enabled.
                print("Heading: " + str(round(current_location[4])) + "°") # Print the current heading to the console in degrees.

        if (config["display"]["displays"]["satellites"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if the satellite display is enabled in the configuration.
            print("Satellites: " + str(current_location[5])) # Print the current altitude satellite count to the console.

        if (config["display"]["displays"]["planes"] == True and config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if the plane count display is enabled in the configuration.
            print("Aircraft: " + str(len(aircraft_data))) # Print the current detected plane count to the console.
        if (config["display"]["displays"]["attention"] == True and config["general"]["attention_monitoring"]["enabled"] == True): # Check to see if the attention timer display is enabled in the configuration.
            print("Attention: " + str(datetime.timedelta(seconds=round(get_current_attention_time()[0]))) + " active (" + str(datetime.timedelta(seconds=round(get_current_attention_time()[1]))) + " reset)") # Print the current active attention time to the console.
            print("Bluetooth: " + str(len(bluetooth_devices))) # Print the number of nearby Bluetooth devices.

        print("") # Add a line break after displaying the main information display.






        # Display GPS alerts.
        if (config["general"]["gps"]["alerts"]["enabled"] == True and len(gps_alerts) > 0):
            debug_message("Displaying GPS alerts")
            print(style.green + "GPS Alerts: " + str(len(gps_alerts))) # Display the GPS alert title.
            if ("maxspeed" in gps_alerts): # Check to see if there is an entry for 'max speed' alerts in the GPS alerts.
                if (gps_alerts["maxspeed"]["active"] == True):
                    print("    Calculated Overspeed: " + str(round(gps_alerts["maxspeed"]["speed"]*1000)/1000))
            if ("nodata" in gps_alerts): # Check to see if there is an entry for 'no data' alerts in the GPS alerts.
                if (gps_alerts["nodata"]["active"] == True):
                    print("    No GPS Data")
            if ("frozen" in gps_alerts): # Check to see if there is an entry for 'frozen' alerts in the GPS alerts.
                if (gps_alerts["frozen"]["active"] == True):
                    print("    GPS Frozen")
            if ("diagnostic" in gps_alerts): # Check to see if there is an entry for 'frozen' alerts in the GPS alerts.
                print("    GPS Diagnostics: (" + str(gps_alerts["diagnostic"]["lat"]) + ", " + str(gps_alerts["diagnostic"]["lon"]) + ") " + str(gps_alerts["diagnostic"]["spd"]) + " m/s facing " + str(gps_alerts["diagnostic"]["hdg"]) + "° at " + str(gps_alerts["diagnostic"]["alt"]) + "m with " + str(gps_alerts["diagnostic"]["sat"]) + " sat")
            print(style.end)

            update_status_lighting("gpsalert")
            play_sound("gps") # Play the alert sound associated with GPS alerts, if one is configured to run.






        # Display ALPR camera alerts.
        if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps"]["enabled"] == True and len(nearby_alpr_cameras) > 0): # Only display nearby ALPR camera alerts if they are enabled.
            debug_message("Displaying ALPR camera alerts")


            print(style.purple + loaded_alpr_camera_database["name"] + " Cameras: " + str(len(nearby_alpr_cameras))) # Display the number of active ALPR alerts.
            print("    Nearest:")
            if (config["general"]["alpr_alerts"]["information_displayed"]["location"] == True): # Only display the location if it is enabled in the configuration.
                print("        Location: " + str(nearest_alpr_camera["lat"]) + ", " + str(nearest_alpr_camera["lon"]) + " (" + get_arrow_direction(nearest_alpr_camera["direction"]) + " " + str(round(nearest_alpr_camera["direction"])) + "°)") # Display the distance to this POI.
            if (config["general"]["alpr_alerts"]["information_displayed"]["distance"] == True): # Only display the distance to the camera if it is enabled in the configuration.
                print("        Distance: " + str(round(nearest_alpr_camera["distance"]*1000)/1000) + " miles") # Display the distance to this POI.
            if (config["general"]["alpr_alerts"]["information_displayed"]["street"] == True): # Only display the street if it is enabled in the configuration.
                if (nearest_alpr_camera["street"] != ""):
                    print("        Street: " + str(nearest_alpr_camera["street"])) # Display the street that this POI is associated with.
                else:
                    print("        Street: Unknown")
            if (config["general"]["alpr_alerts"]["information_displayed"]["bearing"] == True): # Only display the bearing to the camera if it is enabled in the configuration.
                print("        Bearing: " + str(get_cardinal_direction(nearest_alpr_camera["bearing"])) + " " + str(round(nearest_alpr_camera["bearing"])) + "°") # Display the absolute bearing to this POI.
            if (config["general"]["alpr_alerts"]["information_displayed"]["absolute_facing"] == True): # Only display the absolute facing angle of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["facing"] != ""): # Check to see if this POI has direction information.
                    print("        Absolute Facing: " + get_cardinal_direction(nearest_alpr_camera["facing"]) + " " + str(nearest_alpr_camera["facing"]) + "°") # Display the direction this camera is facing.
            if (config["general"]["alpr_alerts"]["information_displayed"]["relative_facing"] == True): # Only display the relative facing angle of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["relativefacing"] != ""): # Check to see if this POI has relative direction information.
                    print("        Relative Facing: " + str(get_arrow_direction(nearest_alpr_camera["relativefacing"])) + " " + str(round(nearest_alpr_camera["relativefacing"])) + "°") # Display the direction this camera is facing relative to the current direction of movement.
            if (config["general"]["alpr_alerts"]["information_displayed"]["brand"] == True): # Only display the brand of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["brand"] != ""):
                    print("        Brand: " + str(nearest_alpr_camera["brand"])) # Display the brand of this camera.
                else:
                    print("        Brand: Unknown") # Display the brand of this camera as unknown.
            if (config["general"]["alpr_alerts"]["information_displayed"]["model"] == True): # Only display the model of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["model"] != ""):
                    print("        Model: " + str(nearest_alpr_camera["model"])) # Display the model of this camera.
                else:
                    print("        Model: Unknown") # Display the model of this camera as unknown.
            if (config["general"]["alpr_alerts"]["information_displayed"]["operator"] == True): # Only display the operator of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["operator"] != ""):
                    print("        Operator: " + str(nearest_alpr_camera["operator"])) # Display the brand of this camera.
                else:
                    print("        Operator: Unknown") # Display the operator of this camera as unknown.
            if (config["general"]["alpr_alerts"]["information_displayed"]["type"] == True): # Only display the type of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["type"] != ""):
                    print("        Type: " + str(nearest_alpr_camera["type"])) # Display the type of this camera.
                else:
                    print("        Type: Unknown") # Display the type of this camera as unknown.
            if (config["general"]["alpr_alerts"]["information_displayed"]["mount"] == True): # Only display the mount of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["mount"] != ""):
                    print("        Mount: " + str(nearest_alpr_camera["mount"])) # Display the mount of this camera.
                else:
                    print("        Mount: Unknown") # Display the mountof this camera as unknown.
            if (config["general"]["alpr_alerts"]["information_displayed"]["description"] == True): # Only display the description of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["description"] != ""):
                    print("        Description: " + str(nearest_alpr_camera["description"])) # Display the description of this camera.
            print(style.end)

            display_shape("horizontal") # Display an ASCII horizontal bar in the console output, if Assassin is configured to do so.

            update_status_lighting("alprcamera") # Run the function to update the status lighting.
            play_sound("alpr")





        # Display traffic camera alerts.
        if (config["general"]["traffic_camera_alerts"]["enabled"] == True and len(nearby_cameras_all) > 0): # Check to see if the speed camera display is enabled in the configuration.
            debug_message("Displaying traffic enforcement camera alerts")

            print(style.blue + "Traffic Enforcement Cameras: " + str(len(nearby_cameras_all)))
            print("    Nearest:")
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["type"] == True): # Only display the camera type if it is enabled in the configuration.
                if (nearby_cameras_all[0]["type"] == "speed"): # Check to see if the overall nearest camera is the nearest speed camera.
                    print("        Type: Speed Camera")
                elif (nearby_cameras_all[0]["type"] == "redlight"): # Check to see if the overall nearest camera is the nearest red light camera.
                    print("        Type: Red Light Camera")
                elif (nearby_cameras_all[0]["type"] == "misc"): # Check to see if the overall nearest camera is the nearest general traffic camera.
                    print("        Type: General Traffic Camera")
                else:
                    print("        Type: Unknown")
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["location"] == True): # Only display the location if it is enabled in the configuration.
                print("        Location: " + str(nearby_cameras_all[0]["lat"]) + ", " + str(nearby_cameras_all[0]["lon"]) + " (" + get_arrow_direction(nearby_cameras_all[0]["direction"]) + " " + str(round(nearby_cameras_all[0]["direction"])) + "°)") # Display the location of the traffic camera.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["distance"] == True): # Only display the distance if it is enabled in the configuration.
                print("        Distance: " + str(round(nearby_cameras_all[0]["dst"]*1000)/1000) + " miles") # Display the current distance to the traffic camera.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["street"] == True): # Only display the street if it is enabled in the configuration.
                if (nearby_cameras_all[0]["str"] != None): # Check to see if street data exists for this camera.
                    print("        Street: " + str(nearby_cameras_all[0]["str"])) # Display the street that the traffic camera is on.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["speed"] == True): # Only display the speed if it is enabled in the configuration.
                if (nearby_cameras_all[0]["spd"] != None): # Check to see if speed limit data exists for this camera.
                    print("        Speed: " + str(round(int(nearby_cameras_all[0]["spd"]) * 0.6213712)) + " mph") # Display the speed limit of the traffic camera, converted to miles per hour.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["bearing"] == True): # Only display the bearing if it is enabled in the configuration.
                print("        Bearing: " + str(get_cardinal_direction(nearby_cameras_all[0]["bearing"])) + " " + str(round(nearby_cameras_all[0]["bearing"])) + "°") # Display the absolute direction towards this camera.
            print(style.end)


            display_shape("circle") # Display an ASCII circle in the console output, if Assassin is configured to do so.

            update_status_lighting("enforcementcamera") # Run the function to update the status lighting.
            # Play audio alerts, as necessary.
            if (nearby_cameras_all[0]["dst"] < (float(config["general"]["traffic_camera_alerts"]["triggers"]["distance"]) * 0.1)): # Check to see if the nearest camera is within 10% of the traffic camera alert radius.
                if (nearby_cameras_all[0]["spd"] != None and config["general"]["traffic_camera_alerts"]["speed_check"] == True): # Check to see if speed limit data exists for this speed camera, and if the traffic camera speed check setting is enabled in the configuration.
                    if (float(nearby_cameras_all[0]["spd"]) < float(convert_speed(float(current_location[2])))): # If the current speed exceeds the speed camera's speed limit, then play a heightened alarm sound.
                        play_sound("alarm")

                play_sound("camera3")
            elif (nearby_cameras_all[0]["dst"] < (float(config["general"]["traffic_camera_alerts"]["triggers"]["distance"]) * 0.25)): # Check to see if the nearest camera is within 25% of the traffic camera alert radius.
                play_sound("camera2")
            elif (nearby_cameras_all[0]["dst"] < (float(config["general"]["traffic_camera_alerts"]["triggers"]["distance"]))): # Check to see if the nearest camera is within the traffic camera alert radius.
                play_sound("camera1")






        # Display drone alerts.
        if (config["general"]["drone_alerts"]["enabled"] == True and len(detected_drone_hazards) > 0): # Check to see if drone alerts are enabled.
            debug_message("Displaying drone alerts")

            print(style.blue + "Autonomous Hazards: " + str(len(detected_drone_hazards)))
            for hazard in detected_drone_hazards: # Iterate through each detected hazard.
                print("    " + hazard["mac"] + "") # Show this hazard's MAC address.
                if (config["general"]["drone_alerts"]["information_displayed"]["threat_type"] == True): # Only display the threat type if it is enabled in the configuration.
                    print("        Threat Type: " + hazard["threattype"]) # Show what kind of threat this device is.
                if (config["general"]["drone_alerts"]["information_displayed"]["company"] == True): # Only display the device company if it is enabled in the configuration.
                    print("        Company: " + hazard["company"]) # Show company or brand that this hazard is associated with.
                if (config["general"]["drone_alerts"]["information_displayed"]["name"] == True): # Only display the device name if it is enabled in the configuration.
                    print("        Name: " + hazard["name"]) # Show this hazard's name.
                if (config["general"]["drone_alerts"]["information_displayed"]["last_seen"] == True): # Only display the last-seen time if it is enabled in the configuration.
                    print("        Last Seen: " + str(hazard["lastseen"])) # Show the timestamp that this hazard was last seen.
                if (config["general"]["drone_alerts"]["information_displayed"]["first_seen"] == True): # Only display the first-seen time if it is enabled in the configuration.
                    print("        First Seen: " + str(hazard["firstseen"])) # Show the timestamp that this hazard was first seen.
                if (config["general"]["drone_alerts"]["information_displayed"]["channel"] == True): # Only display the wireless channel if it is enabled in the configuration.
                    print("        Channel: " + hazard["channel"]) # Show this hazard's wireless channel.
                if (config["general"]["drone_alerts"]["information_displayed"]["packets"] == True): # Only display the packet count if it is enabled in the configuration.
                    print("        Packets: " + hazard["packets"]) # Show this hazard's packet count.
                if (config["general"]["drone_alerts"]["information_displayed"]["strength"] == True): # Only display the signal strength if it is enabled in the configuration.
                    print("        Strength: " + str(hazard["strength"]) + "%") # Show this hazards relative signal strength.
                if (config["general"]["drone_alerts"]["information_displayed"]["wireless_type"] == True): # Only display the wireless device type if it is enabled in the configuration.
                    print("        Wireless Type: " + hazard["type"]) # Show this hazard's type.

                drone_threat_history.append(hazard) # Add this threat to the threat history.

            print(style.end) # End the font styling from the drone threat display.

            save_to_file(assassin_root_directory + "/drone_threat_history.json", str(json.dumps(drone_threat_history, indent = 4)), True) # Save the current drone threat history to disk.

            display_shape("cross") # Display an ASCII cross in the console output to represent a drone, if Assassin is configured to do so.

            update_status_lighting("autonomousthreat") # Update the status lighting to indicate that at least one autonomous threat was detected.
            play_sound("drone") # Play the sound effect associated with a potential drone threat being detected.




        # Display ADS-B aircraft alerts
        if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True and len(aircraft_threats) > 0): # Check to see if ADS-B alerts are enabled.
            debug_message("Displaying ADS-B alerts")

            print(style.blue + "Aircraft Threats: " + str(len(aircraft_threats)))
            for threat in aircraft_threats: # Iterate through each detected potential threat.
                if (float(threat["longitude"]) == 0.0 and float(threat["latitude"]) == 0.0): # Check to see if this aircraft is missing position data.
                    print("    " + threat["id"] + ": Incomplete data") # Show this aircraft as invalid.
                else:
                    print("    " + threat["id"] + ":") # Show this hazard's identifier.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["location"] == True): # Only display the location if it is enabled in the configuration.
                        print("        Location: " + str(threat["latitude"]) + ", " + str(threat["longitude"]) + " (" + get_arrow_direction(threat["direction"]) + " " + str(round(threat["direction"])) + "°)") # Show the coordinates of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["distance"] == True): # Only display the distance if it is enabled in the configuration.
                        print("        Distance: " + str(round(threat["distance"]*1000)/1000) + " miles") # Show the distance to this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["threat_level"] == True): # Only display the threat level if it is enabled in the configuration.
                        print("        Threat Level: " + str(threat["threatlevel"])) # Show the distance to this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["speed"] == True): # Only display the speed if it is enabled in the configuration.
                        print("        Speed: " + str(threat["speed"]) + " knots") # Show the speed of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["altitude"] == True): # Only display the altitude if it is enabled in the configuration.
                        print("        Altitude: " + str(threat["altitude"]) + " feet") # Show the altitude of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["absolute_heading"] == True): # Only display the absolute heading if it is enabled in the configuration.
                        if (threat["absoluteheading"] == "?"): # Check to see if this aircraft has an unknown absolute heading.
                            print("        Absolute Heading: ?") # Show the absolute heading of this aircraft.
                        else:
                            print("        Absolute Heading: " + get_cardinal_direction(threat["heading"]) + " (" + str(threat["heading"]) + "°)") # Show the absolute heading of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["relative_heading"] == True): # Only display the relative heading if it is enabled in the configuration.
                        if (threat["relativeheading"] == "?"): # Check to see if this aircraft has an unknown relative heading.
                            print("        Relative Heading: ?") # Show the direction of this aircraft relative to the current direction of movement.
                        else:
                            print("        Relative Heading: " + get_arrow_direction(threat["relativeheading"]), " (", str(threat["relativeheading"]), "°)") # Show the direction of this aircraft relative to the current direction of movement.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["time"] == True): # Only display the message age if it is enabled in the configuration.
                        print("        Time: " + str(round((time.time() - float(threat["time"]))*100)/100) + " seconds ago") # Show how long it has been since this aircraft was detected.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["callsign"] == True): # Only display the callsign if it is enabled in the configuration.
                        print("        Callsign: " + str(threat["callsign"])) # Show the callsign of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["climb"] == True): # Only display the climb rate if it is enabled in the configuration.
                        print("        Climb: " + str(threat["climb"]) + " feet per minute") # Show the vertical climb rate of this aircraft.

            print(style.end) # End the font styling from the aircraft ADS-B threat display.

            display_shape("triangle") # Display an ASCII triangle in the console output to represent a plane, if Assassin is configured to do so.

            update_status_lighting("adsbthreat") # Update the status lighting to indicate that at least one ADS-B aircraft threat was detected.
            play_sound("adsb") # Play the sound effect associated with a potential ADS-B aircraft threat being detected.



        # Display weather alerts.
        if (config["general"]["weather_alerts"]["enabled"] == True and len(weather_alerts) > 0): # Check to make sure weather alerts are enabled before displaying weather alerts.
            debug_message("Displaying weather alerts")
            print(style.yellow + "Weather Alerts: " + str(len(weather_alerts))) # Display the weather alerts title.

            # Display visibility alerts.
            if ("visibility" in weather_alerts): # Check to see if there is a visibility alert.
                if (weather_alerts["visibility"][1] == "below"): # Check to see if the alert is below the low threshold.
                    print("    Visibility low: " + str(weather_alerts["visibility"][0]))
                elif (weather_alerts["visibility"][1] == "above"): # Check to see if the alert is above the high threshold.
                    print("    Visibility high: " + str(weather_alerts["visibility"][0]))
                else: # Check to see if the alert is another case. This should never happen, and indicates a bug if it does.
                    print("    Visibility unknown alert: " + str(weather_alerts["visibility"][0]))

            # Display temperature alerts.
            if ("temperature" in weather_alerts): # Check to see if there is a temperature alert.
                if (weather_alerts["temperature"][1] == "below"): # Check to see if the alert is below the low threshold.
                    print("    Temperature low: " + str(weather_alerts["temperature"][0]))
                elif (weather_alerts["visibility"][1] == "above"): # Check to see if the alert is above the high threshold.
                    print("    Temperature high: " + str(weather_alerts["temperature"][0]))
                else: # Check to see if the alert is another case. This should never happen, and indicates a bug if it does.
                    print("    Temperature unknown alert: " + str(weather_alerts["temperature"][0]))
            print(style.end)



        # Display OBD alerts.
        if (config["general"]["obd_integration"]["enabled"] == True and len(obd_alerts) > 0): # Check to make sure OBD integration is enabled before displaying OBD alerts.
            debug_message("Displaying OBD integration alerts")
            print(style.green + "OBD: " + str(len(obd_alerts))) # Display the OBD integration alerts title.
            if ("speed" in obd_alerts): # Check to see if there are any speed alerts.
                if (obd_alerts["speed"]["alert"] == "high"):
                    print("    Speed - High: ", obd_alerts["speed"]["value"])
                elif (obd_alerts["speed"]["alert"] == "low"):
                    print("    Speed - Low: ", obd_alerts["speed"]["value"])
                else:
                    print("    Speed - Unknown: ", obd_alerts["speed"]["value"])
            if ("rpm" in obd_alerts): # Check to see if there are any engine RPM alerts.
                if (obd_alerts["rpm"]["alert"] == "high"):
                    print("    RPM - High: ", obd_alerts["rpm"]["value"])
                elif (obd_alerts["rpm"]["alert"] == "low"):
                    print("    RPM - Low: ", obd_alerts["rpm"]["value"])
                else:
                    print("    RPM - Unknown: ", obd_alerts["rpm"]["value"])
            if ("fuel_level" in obd_alerts): # Check to see if there are any fuel level alerts.
                if (obd_alerts["fuel_level"]["alert"] == "high"):
                    print("    Fuel Level - High: ", round(obd_alerts["fuel_level"]["value"]*1000)/10, "%")
                elif (obd_alerts["fuel_level"]["alert"] == "low"):
                    print("    Fuel Level - Low: ", round(obd_alerts["fuel_level"]["value"]*1000)/10, "%")
                else:
                    print("    Fuel Level - Unknown: ", round(obd_alerts["fuel_level"]["value"]*1000)/10, "%")
            if ("airflow" in obd_alerts): # Check to see if there are any airflow alerts.
                if (obd_alerts["airflow"]["alert"] == "high"):
                    print("    Airflow - High: ", obd_alerts["airflow"]["value"])
                elif (obd_alerts["fuel_level"]["alert"] == "low"):
                    print("    Airflow - Low: ", obd_alerts["airflow"]["value"])
                else:
                    print("    Airflow - Unknown: ", obd_alerts["airflow"]["value"])
            print(style.end)


        # Display attention alerts.
        if (config["general"]["attention_monitoring"]["enabled"] == True and len(attention_alerts) > 0): # Check to see if there are attention alerts.
            debug_message("Displaying attention monitoring alerts")
            print(style.yellow + "Attention Alerts: " + str(len(attention_alerts))) # Display the attention monitoring alerts title.

            # Display attention alerts.
            if ("time" in attention_alerts): # Check to see if there is a time-related attention alert.
                print("    Attentive Time: " + str(math.floor(round(attention_alerts["time"]["time"])/60)) + " min " + str(round(attention_alerts["time"]["time"]) % 60) + " sec") # Display the time-related attention alert.

            print(style.end)

            update_status_lighting("attention")


        # Display Bluetooth scanning alerts.
        if (config["general"]["bluetooth_scanning"]["enabled"] == True and len(bluetooth_alerts) > 0): # Check to see if there is 1 or more Bluetooth devices.
            debug_message("Displaying attention monitoring alerts")
            print(style.blue + "Bluetooth Alerts: " + str(len(bluetooth_alerts))) # Display the Bluetooth scanning alerts title.

            # Display Bluetooth alerts.
            for device in bluetooth_alerts:
                print("    " + str(device) + ": " + bluetooth_devices[device]["name"])
                if ("time" in bluetooth_alerts[device]): # Check to see if there is distance information associated with this alert.
                    print("        Time: " + str(round(bluetooth_alerts[device]["time"])) + " sec")
                if ("distance" in bluetooth_alerts[device]): # Check to see if there is time information associated with this alert.
                    print("        Distance: " + str(round(bluetooth_alerts[device]["distance"]*100)/100))
                if ("blacklist" in bluetooth_alerts[device]): # Check to see if there is blacklist information associated with this alert.
                    print("        Blacklist: " + bluetooth_alerts[device]["blacklist"])

            print(style.end)

            update_status_lighting("bluetooth")



        # Display Predator integration alerts.
        if (config["general"]["predator_integration"]["enabled"] == True and len(predator_alerts) > 0): # Check to make sure Predator integration is enabled before displaying Predator alerts.
            debug_message("Displaying Predator alerts")
            print(style.yellow + "Predator: " + str(len(predator_alerts))) # Display the attention monitoring alerts title.
            for plate in predator_alerts:
                print("    Plate: " + str(plate))
                for alert in predator_alerts[plate]:
                    print("        Trigger: " + str(alert))

            print(style.end)

            update_status_lighting("predator")

        process_timing("Displays", "end")






    # Record telemetry data according to the configuration.
    if (config["general"]["telemetry"]["enabled"] == True): # Check to see if Assassin is configured to record telemetry data.
        debug_message("Recording telemetry data")
        process_timing("Telemetry Saving", "start")
        save_gpx(location_history) # Save the location history to a GPX file.
        process_timing("Telemetry Saving", "end")



    #if (config["general"]["debugging_output"] == True): # Check to see if debug output is enabled.
        #debug_message("Displaying process timers\n" + str(json.dumps(process_timing("", "dump"), indent=4))) # Print the timers for all processes.

    debug_message("Executing refresh delay")
    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
