# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
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
debug_message("Loading `utils.py` functions")
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
calculate_bearing = utils.calculate_bearing # Load the function used to calculate the bearing between two coordinate pairs.
nearby_database_poi = utils.nearby_database_poi # Load the function used to check for general nearby points of interest.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
get_cardinal_direction = utils.get_cardinal_direction # Load the function used to convert headings from degrees to cardinal directions.
get_arrow_direction = utils.get_arrow_direction # Load the function used to convert headings from degrees to arrow directions.
update_status_lighting = utils.update_status_lighting # Load the function used to update the status lighting system.
play_sound = utils.play_sound # Load the function used to play sounds specified in the configuration based on their IDs.
display_notice = utils.display_notice  # Load the function used to display notices, warnings, and errors.
speak = utils.speak # Load the function used to play text-to-speech.
save_gpx = utils.save_gpx # Load the function used to save the location history to a GPX file.


import gpslocation
get_gps_location = gpslocation.get_gps_location # Load the function to get the current GPS location.
process_gps_alerts = gpslocation.process_gps_alerts # Load the function used to detect GPS problems.


debug_message("Acquiring initial location")
initial_location = [0, 0] # Set the "current location" to a placeholder.
previous_gps_attempt = False # This variable will be changed to `True` if the GPS fails to get a lock at least once. This variable is responsible for triggering a delay to allow the GPS to get a lock.
while (initial_location[0] == 0 and initial_location[1] == 0): # Repeatedly attempt to get a GPS location until one is received.
    if (previous_gps_attempt == True): # If the GPS previously failed to get a lock, then wait 2 seconds before trying again.
        time.sleep(2) # Wait 2 seconds to give the GPS time to get a lock.

    previous_gps_attempt = True
    initial_location = get_gps_location() # Attempt to get the current GPS location.



# Load functionality plugins

# Load the traffic camera alert system
if (config["general"]["traffic_camera_alerts"]["alert_range"] > 0 and config["general"]["gps"]["enabled"] == True): # Only load traffic enforcement camera information if traffic camera alerts are enabled.
    debug_message("Initializing traffic camera alert system")
    import trafficcameras
    load_traffic_camera_database = trafficcameras.load_traffic_camera_database
    traffic_camera_alert_processing = trafficcameras.traffic_camera_alert_processing

    loaded_traffic_camera_database = load_traffic_camera_database(initial_location)


# Load the ADS-B aircraft alert system.
if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only load the ADS-B system if ADS-B alerts are enabled.
    debug_message("Initializing aircraft alert system")
    import aircraft
    fetch_aircraft_data = aircraft.fetch_aircraft_data # Load the function used to fetch aircraft data from a Dump1090 CSV file.
    start_adsb_monitoring = aircraft.start_adsb_monitoring
    adsb_alert_processing = aircraft.adsb_alert_processing

    start_adsb_monitoring()



# Load the drone/autonomous threat alert system.
if (config["general"]["drone_alerts"]["enabled"] == True): # Only load drone processing if drone alerts are enabled.
    debug_message("Initializing drone alert system")
    import drones
    drone_alert_processing = drones.drone_alert_processing
    load_drone_alerts = drones.load_drone_alerts

    drone_threat_history, radio_device_history, drone_threat_database = load_drone_alerts()
    detected_drone_hazards = []


# Load the ALPR camera alert system.
if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps"]["enabled"] == True): # Only load ALPR camera information if ALPR alerts are enabled.
    debug_message("Initializing ALPR camera system")
    import alprcameras
    load_alpr_camera_database = alprcameras.load_alpr_camera_database
    alpr_camera_alert_processing = alprcameras.alpr_camera_alert_processing

    loaded_alpr_camera_database = load_alpr_camera_database(initial_location)


# Load the Bluetooth device alert system. 
if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only load Bluetooth monitoring system if Bluetooth monitoring is enabled.
    debug_message("Initializing Bluetooth monitoring system")
    import bluetoothdevices
    load_bluetooth_log_file = bluetoothdevices.load_bluetooth_log_file
    bluetooth_alert_processing = bluetoothdevices.bluetooth_alert_processing
    start_bluetooth_scanning = bluetoothdevices.start_bluetooth_scanning
    fetch_nearby_bluetooth_devices = bluetoothdevices.fetch_nearby_bluetooth_devices

    detected_bluetooth_devices = load_bluetooth_log_file() # Load the detected Bluetooth device history.
    start_bluetooth_scanning()



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
alert_count["bluetooth"] = [0, 0]
alert_count["weather"] = [0, 0]
alert_count["gps"] = [0, 0]
alert_count["attention"] = [0, 0]

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
        current_location = get_gps_location() # Get the current location.
        current_speed = round(convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"])*10**int(config["display"]["displays"]["speed"]["decimal_places"]))/(10**int(config["display"]["displays"]["speed"]["decimal_places"])) # Convert the speed data from the GPS into the units specified by the configuration.
    else: # GPS functionality is disabled.
        current_location = [0.0000, 0.0000, 0.0, 0.0, 0.0, 0, "V0LT Assassin"] # Set the current location to a placeholder.

    location_history.append({"lat" : current_location[0], "lon" : current_location[1], "spd" : current_location[2], "alt" : current_location[3], "hdg": current_location[4], "sat" : current_location[5], "time" : time.time(), "src": current_location[6]})# Add the most recently recorded location to the beginning of the location history list.



    # Run GPS alert processing.
    if (config["general"]["gps"]["alerts"]["enabled"] == True and config["general"]["gps"]["enabled"]): # Check to make sure GPS alerts are enabled before processing alerts.
        gps_alerts = process_gps_alerts(location_history) # Process GPS alerts.
    else: # GPS alert detection is disabled.
        gps_alerts = {} # Return a blank placeholder dictionary in place of the true alerts.


    # Run traffic enforcement camera alert processing.
    if (config["general"]["traffic_camera_alerts"]["alert_range"] > 0 and config["general"]["gps"]["enabled"] == True): # Only run traffic enforcement camera alert processing if traffic camera alerts are enabled.
        nearest_enforcement_camera, nearby_cameras_all = traffic_camera_alert_processing(current_location, loaded_traffic_camera_database)
    else:
        nearest_enforcement_camera, nearby_cameras_all = {}, []


    # Run ALPR camera alert processing.
    if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps"]["enabled"] == True): # Only run ALPR camera processing if ALPR alerts are enabled.
        nearest_alpr_camera, nearby_alpr_cameras = alpr_camera_alert_processing(current_location, loaded_alpr_camera_database)
    else:
        nearest_alpr_camera, nearby_alpr_cameras = {}, []


    # Run drone alert processing.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Only run drone processing if drone alerts are enabled.
        detected_drone_hazards = drone_alert_processing(radio_device_history, drone_threat_database, detected_drone_hazards)
    else:
        detected_drone_hazards = []


    # Run Bluetooth alert processing.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run Bluetooth monitoring processing if Bluetooth monitoring is enabled.
        detected_bluetooth_devices, bluetooth_threats = bluetooth_alert_processing(current_location, detected_bluetooth_devices)
    elif (config["general"]["bluetooth_monitoring"]["enabled"] == True and config["general"]["gps"]["enabled"] == False): # If GPS functionality is disabled, then run Bluetooth monitoring without GPS information.
        detected_bluetooth_devices, bluetooth_threats = bluetooth_alert_processing([0.0000, 0.0000, 0.0, 0.0, 0.0, 0], detected_bluetooth_devices) # Run the Bluetooth alert processing function with dummy GPS data.
    else:
        detected_bluetooth_devices, bluetooth_threats = {}, {}


    # Process ADS-B alerts.
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run ADS-B alert processing if it is enabled in the configuration.
        aircraft_threats, aircraft_data = adsb_alert_processing(current_location)
    else:
        aircraft_threats, aircraft_data = [], {}


    # Process weather alerts.
    if (config["general"]["weather_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run weather alert processing if it is enabled in the configuration.
        last_weather_data = weather_data
        weather_data = get_weather_data(current_location, last_weather_data)
        weather_alerts = weather_alert_processing(weather_data)
    else:
        weather_alerts = {}


    # Process attention alerts.
    if (config["general"]["attention_monitoring"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Only run attention monitoring alert processing if it is enabled in the configuration.
        attention_alerts = process_attention_alerts(float(current_speed))
    else:
        attention_alerts = {}
        



    debug_message("Alert processing completed")


    if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
        update_status_lighting("normal") # Run the function to reset the status lighting to indicate normal operation.







    # Collect all alerts.
    all_alerts = dict(list(all_alerts.items())[-10:]) # Trim the dictionary of all alerts to the last 10 entries.
    current_time = time.time() # Get the current time.
    all_alerts[current_time] = {}
    all_alerts[current_time]["drone"] = detected_drone_hazards
    all_alerts[current_time]["aircraft"] = aircraft_threats
    all_alerts[current_time]["traffic_camera"] = nearby_cameras_all
    all_alerts[current_time]["alpr"] = nearby_alpr_cameras
    all_alerts[current_time]["bluetooth"] = bluetooth_threats
    all_alerts[current_time]["weather"] = weather_alerts
    all_alerts[current_time]["gps"] = gps_alerts
    all_alerts[current_time]["attention"] = attention_alerts


    if (config["external"]["local"]["enabled"] == True): # Check to see if interfacing with local services is enabled.
        save_to_file(config["external"]["local"]["interface_directory"] + "/alerts.json", json.dumps(all_alerts)) # Save all current alerts to disk.


    # Record the number of active alerts.
    alert_count["drone"] = [len(detected_drone_hazards)] + alert_count["drone"]
    alert_count["aircraft"] = [len(aircraft_threats)] + alert_count["aircraft"]
    alert_count["traffic_camera"] = [len(nearby_cameras_all)] + alert_count["traffic_camera"]
    alert_count["alpr"] = [len(nearby_alpr_cameras)] + alert_count["alpr"]
    alert_count["bluetooth"] = [len(bluetooth_threats)] + alert_count["bluetooth"]
    alert_count["weather"] = [len(weather_alerts)] + alert_count["weather"]
    alert_count["gps"] = [len(gps_alerts)] + alert_count["gps"]
    alert_count["attention"] = [len(attention_alerts)] + alert_count["attention"]


    # Only keep alert counts from the past 100 cycles.
    alert_count["drone"] = alert_count["drone"][:100]
    alert_count["aircraft"] = alert_count["aircraft"][:100]
    alert_count["traffic_camera"] = alert_count["traffic_camera"][:100]
    alert_count["alpr"] = alert_count["alpr"][:100]
    alert_count["bluetooth"] = alert_count["bluetooth"][:100]
    alert_count["weather"] = alert_count["weather"][:100]
    alert_count["gps"] = alert_count["gps"][:100]
    alert_count["attention"] = alert_count["attention"][:100]




    # Alert the user via text-to-speech, as necessary.
    if (config["audio"]["tts"]["enabled"] == True): # Check to make sure text-to-speech is enabled before doing any processing.
        debug_message("Running text-to-speech processing")

        # Process drone text to speech alerts.
        if (alert_count["drone"][0] > alert_count["drone"][1]):
            speak("New drone alert", "Drone")

        # Process aircraft text to speech alerts.
        if (alert_count["aircraft"][0] > alert_count["aircraft"][1]):
            speak("New aircraft alert. " + str(round(aircraft_threats[0]["distance"]*10)/10) + " miles", "Aircraft")

        # Process traffic camera text to speech alerts.
        if (alert_count["traffic_camera"][0] > alert_count["traffic_camera"][1]):
            speak("New traffic camera alert. " + str(round(nearest_enforcement_camera["dst"]*10)/10) + " miles", "Traffic camera")

        # Process ALPR text to speech alerts.
        if (alert_count["alpr"][0] > alert_count["alpr"][1]):
            speak("New A. L. P. R. Alert. " + str(round(nearest_alpr_camera["distance"]*10)/10) + " miles", "A. L. P. R")

        # Process Bluetooth text to speech alerts.
        if (alert_count["bluetooth"][0] > alert_count["bluetooth"][1]):
            speak("New Bluetooth alert", "Bluetooth")

        # Process weather text to speech alerts.
        if (alert_count["weather"][0] > alert_count["weather"][1]):
            speak("New weather alert", "Weather")

        # Process GPS text to speech alerts.
        if (alert_count["gps"][0] > alert_count["gps"][1]):
            speak("New GPS alert", "GPS")

        # Process attention text to speech alerts.
        if (alert_count["gps"][0] > alert_count["gps"][1]):
            speak("Attention threshold reached", "Attention")

        debug_message("Completed Text-to-speech processing")










    clear() # Clear the console output at the beginning of every cycle.









    # Show all configured basic information displays.

    debug_message("Displaying basic dashboard")

    if (config["display"]["displays"]["speed"]["large_display"] == True and config["general"]["gps"]["enabled"] == True): # Check to see the large speed display is enabled in the configuration.
        current_speed = convert_speed(float(current_location[2]), config["display"]["displays"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
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
    if (config["display"]["displays"]["bluetooth"] == True and config["general"]["bluetooth_monitoring"]["enabled"] == True): # Check to see if the Bluetooth device count display is enabled in the configuration.
        print("Bluetooth: " + str(len(fetch_nearby_bluetooth_devices()))) # Print the current detected Bluetooth device count to the console.
    if (config["display"]["displays"]["attention"] == True and config["general"]["attention_monitoring"]["enabled"] == True): # Check to see if the attention timer display is enabled in the configuration.
        print("Attention: " + str(datetime.timedelta(seconds=round(get_current_attention_time()[0]))) + " active (" + str(datetime.timedelta(seconds=round(get_current_attention_time()[1]))) + " reset)") # Print the current active attention time to the console.

    print("") # Add a line break after displaying the main information display.






    # Display GPS alerts.
    if (config["general"]["gps"]["alerts"]["enabled"] == True):
        debug_message("Displaying GPS alerts")
        if (len(gps_alerts) > 0): # Check to see if there are any GPS alerts to display.
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
            print(style.end)

            play_sound("gps") # Play the alert sound associated with GPS alerts, if one is configured to run.





    # Display Bluetooth monitoring alerts.
    if (config["general"]["bluetooth_monitoring"]["enabled"] == True): # Only conduct Bluetooth alert processing if Bluetooth alerts and GPS features are enabled in the configuration.
        debug_message("Displaying Bluetooth alerts")
        if (len(bluetooth_threats) > 0): # Check to see if at least one Bluetooth threat was detected.
            print(style.purple + "Bluetooth Hazards: " + str(len(bluetooth_threats))) # Display the Bluetooth alert title.
            for threat in bluetooth_threats: # Iterate through all of the active Bluetooth threats.
                print("    " + str(threat['address']))
                if (config["general"]["bluetooth_monitoring"]["information_displayed"]["name"] == True): # Only display the device name if it is enabled in the configuration.
                    print("        Name: " + str(threat['name']))
                if (config["general"]["bluetooth_monitoring"]["information_displayed"]["distance"] == True): # Only display the following distance if it is enabled in the configuration.
                    print("        Distance: " + str(threat['distance_followed']))
                if (config["general"]["bluetooth_monitoring"]["information_displayed"]["time"] == True): # Only display the following time if it is enabled in the configuration.
                    print("        Time: " + str(int(threat['lastseentime']) - int(threat['firstseentime']))+ " seconds")
            print(style.end)


            display_shape("square") # Display an ASCII square in the console output to represent a device, if Assassin is configured to do so.

            play_sound("bluetooth") # Play the alert sound associated with Bluetooth alerts, if one is configured to run.
            



    # Display ALPR camera alerts.
    if (float(config["general"]["alpr_alerts"]["alert_range"]) > 0 and config["general"]["gps"]["enabled"] == True): # Only display nearby ALPR camera alerts if they are enabled.
        if (len(nearby_alpr_cameras) > 0): # Only iterate through the nearby cameras if there are any nearby cameras to begin with.
            debug_message("Displaying ALPR camera alerts")

            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("alprcamera") # Run the function to update the status lighting.

            print(style.purple + loaded_alpr_camera_database["name"] + " Cameras: " + str(len(nearby_alpr_cameras))) # Display the number of active ALPR alerts.
            print("    Nearest:")
            if (config["general"]["alpr_alerts"]["information_displayed"]["location"] == True): # Only display the location if it is enabled in the configuration.
                print("        Location: " + str(nearest_alpr_camera["latitude"]) + ", " + str(nearest_alpr_camera["longitude"]) + " (" + get_arrow_direction(nearest_alpr_camera["direction"]) + " " + str(round(nearest_alpr_camera["direction"])) + "°)") # Display the distance to this POI.
            if (config["general"]["alpr_alerts"]["information_displayed"]["distance"] == True): # Only display the distance to the camera if it is enabled in the configuration.
                print("        Distance: " + str(round(nearest_alpr_camera["distance"]*1000)/1000) + " miles") # Display the distance to this POI.
            if (config["general"]["alpr_alerts"]["information_displayed"]["street"] == True): # Only display the street if it is enabled in the configuration.
                print("        Street: " + str(nearest_alpr_camera["road"])) # Display the road that this POI is associated with.
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
            if (config["general"]["alpr_alerts"]["information_displayed"]["description"] == True): # Only display the description of the camera if it is enabled in the configuration.
                if (nearest_alpr_camera["description"] != ""):
                    print("        Description: " + str(nearest_alpr_camera["description"])) # Display the description of this camera.
            print(style.end)

            display_shape("horizontal") # Display an ASCII horizontal bar in the console output, if Assassin is configured to do so.

            play_sound("alpr")





    # Display traffic camera alerts.
    if (config["general"]["gps"]["enabled"] == True and float(config["general"]["traffic_camera_alerts"]["alert_range"]) > 0 and "nearest_enforcement_camera" in locals()): # Check to see if the speed camera display is enabled in the configuration.
        debug_message("Displaying traffic enforcement camera alerts")
        # Display the nearest traffic camera, if applicable.
        if (nearest_enforcement_camera["dst"] < float(config["general"]["traffic_camera_alerts"]["alert_range"])): # Only display the nearest camera if it's within the maximum range specified in the configuration.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("enforcementcamera") # Run the function to update the status lighting.

            print(style.blue + "Traffic Enforcement Cameras: " + str(len(nearby_cameras_all)))
            print("    Nearest:")
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["type"] == True): # Only display the camera type if it is enabled in the configuration.
                if (nearest_enforcement_camera["type"] == "speed"): # Check to see if the overall nearest camera is the nearest speed camera.
                    print("        Type: Speed Camera")
                elif (nearest_enforcement_camera["type"] == "redlight"): # Check to see if the overall nearest camera is the nearest red light camera.
                    print("        Type: Red Light Camera")
                elif (nearest_enforcement_camera["type"] == "misc"): # Check to see if the overall nearest camera is the nearest general traffic camera.
                    print("        Type: General Traffic Camera")
                else:
                    print("        Type: Unknown")
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["location"] == True): # Only display the location if it is enabled in the configuration.
                print("        Location: " + str(nearest_enforcement_camera["lat"]) + ", " + str(nearest_enforcement_camera["lon"]) + " (" + get_arrow_direction(nearest_enforcement_camera["direction"]) + " " + str(round(nearest_enforcement_camera["direction"])) + "°)") # Display the location of the traffic camera.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["distance"] == True): # Only display the distance if it is enabled in the configuration.
                print("        Distance: " + str(round(nearest_enforcement_camera["dst"]*1000)/1000) + " miles") # Display the current distance to the traffic camera.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["street"] == True): # Only display the street if it is enabled in the configuration.
                if (nearest_enforcement_camera["str"] != None): # Check to see if street data exists for this camera.
                    print("        Street: " + str(nearest_enforcement_camera["str"])) # Display the street that the traffic camera is on.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["speed"] == True): # Only display the speed if it is enabled in the configuration.
                if (nearest_enforcement_camera["spd"] != None): # Check to see if speed limit data exists for this camera.
                    print("        Speed: " + str(round(int(nearest_enforcement_camera["spd"]) * 0.6213712)) + " mph") # Display the speed limit of the traffic camera, converted to miles per hour.
            if (config["general"]["traffic_camera_alerts"]["information_displayed"]["bearing"] == True): # Only display the bearing if it is enabled in the configuration.
                print("        Bearing: " + str(get_cardinal_direction(nearest_enforcement_camera["bearing"])) + " " + str(round(nearest_enforcement_camera["bearing"])) + "°") # Display the absolute direction towards this camera.
            print(style.end)


            display_shape("circle") # Display an ASCII circle in the console output, if Assassin is configured to do so.

            # Play audio alerts, as necessary.
            if (nearest_enforcement_camera["dst"] < (float(config["general"]["traffic_camera_alerts"]["alert_range"]) * 0.1)): # Check to see if the nearest camera is within 10% of the traffic camera alert radius.
                if (nearest_enforcement_camera["spd"] != None and config["general"]["traffic_camera_alerts"]["speed_check"] == True): # Check to see if speed limit data exists for this speed camera, and if the traffic camera speed check setting is enabled in the configuration.
                    if (float(nearest_enforcement_camera["spd"]) < float(convert_speed(float(current_location[2]), "mph"))): # If the current speed exceeds the speed camera's speed limit, then play a heightened alarm sound.
                        play_sound("alarm")

                play_sound("camera3")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["traffic_camera_alerts"]["alert_range"]) * 0.25)): # Check to see if the nearest camera is within 25% of the traffic camera alert radius.
                play_sound("camera2")
            elif (nearest_enforcement_camera["dst"] < (float(config["general"]["traffic_camera_alerts"]["alert_range"]))): # Check to see if the nearest camera is within the traffic camera alert radius.
                play_sound("camera1")






    # Display drone alerts.
    if (config["general"]["drone_alerts"]["enabled"] == True): # Check to see if drone alerts are enabled.
        debug_message("Displaying drone alerts")
        if (len(detected_drone_hazards) > 0): # Check to see if any hazards were detected this cycle.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("autonomousthreat") # Update the status lighting to indicate that at least one autonomous threat was detected.

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

            play_sound("drone") # Play the sound effect associated with a potential drone threat being detected.




    # Display ADS-B aircraft alerts
    if (config["general"]["adsb_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to see if ADS-B alerts are enabled.
        debug_message("Displaying ADS-B alerts")
        if (len(aircraft_threats) > 0 and current_location[2] >= config["general"]["adsb_alerts"]["minimum_vehicle_speed"]): # Check to see if any threats were detected this cycle, and if the GPS speed indicates that the vehicle is travelling above the minimum alert speed.
            if (config["display"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Assassin configuration.
                update_status_lighting("adsbthreat") # Update the status lighting to indicate that at least one ADS-B aircraft threat was detected.

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
                        print("        Absolute Heading: " + get_cardinal_direction(threat["heading"]) + " (" + str(threat["heading"]) + "°)") # Show the absolute heading of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["relative_heading"] == True): # Only display the relative heading if it is enabled in the configuration.
                        print("        Relative Heading: " + get_arrow_direction(threat["relativeheading"]) + " (" + str(threat["relativeheading"]) + "°)") # Show the direction of this aircraft relative to the current direction of movement.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["time"] == True): # Only display the message age if it is enabled in the configuration.
                        print("        Time: " + str(round((time.time() - float(threat["time"]))*100)/100) + " seconds ago") # Show how long it has been since this aircraft was detected.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["callsign"] == True): # Only display the callsign if it is enabled in the configuration.
                        print("        Callsign: " + str(threat["callsign"])) # Show the callsign of this aircraft.
                    if (config["general"]["adsb_alerts"]["information_displayed"]["climb"] == True): # Only display the climb rate if it is enabled in the configuration.
                        print("        Climb: " + str(threat["climb"]) + " feet per minute") # Show the vertical climb rate of this aircraft.

            print(style.end) # End the font styling from the aircraft ADS-B threat display.

            display_shape("triangle") # Display an ASCII triangle in the console output to represent a plane, if Assassin is configured to do so.

            play_sound("adsb") # Play the sound effect associated with a potential ADS-B aircraft threat being detected.



    # Display weather alerts.
    if (config["general"]["weather_alerts"]["enabled"] == True): # Check to make sure weather alerts are enabled before displaying weather alerts.
        debug_message("Displaying weather alerts")
        if (len(weather_alerts) > 0): # Check to see if there are any active weather alerts.
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



    # Display attention alerts.
    if (config["general"]["attention_monitoring"]["enabled"] == True): # Check to make sure attention monitoring is enabled before displaying attention alerts.
        debug_message("Displaying attention monitoring alerts")
        if (len(attention_alerts) > 0): # Check to see if there are any active attention monitoring alerts.
            print(style.yellow + "Attention Alerts: " + str(len(attention_alerts))) # Display the attention monitoring alerts title.

            # Display visibility alerts.
            if ("time" in attention_alerts): # Check to see if there is a time-related attention alert.
                print("    Attentive Time: " + str(math.floor(round(attention_alerts["time"]["time"])/60)) + " min " + str(round(attention_alerts["time"]["time"]) % 60) + " sec") # Display the time-related attention alert.

            print(style.end)






    # Record telemetry data according to the configuration.
    if (config["general"]["telemetry"]["enabled"] == True): # Check to see if Assassin is configured to record telemetry data.
        debug_message("Recording telemetry data")
        save_gpx(location_history, config["general"]["telemetry"]["directory"]) # Save the location history to a GPX file.




    debug_message("Executing refresh delay")
    time.sleep(float(config["general"]["refresh_delay"])) # Wait for a certain amount of time, as specified in the configuration.
