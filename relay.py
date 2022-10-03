import csv
import os
import time
import datetime

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message
display_notice = utils.display_notice
save_to_file = utils.save_to_file
add_to_file = utils.add_to_file


# Locate and load the configuration file.
config = load_config()

if (config["general"]["relay_alerts"]["enabled"] == True): # Only import the GPIO library if relay alerts are enabled.
    debug_message("Importing `GPIO` library")
    import RPi.GPIO as GPIO




def relay_alert_processing():
    if (config["general"]["relay_alerts"]["enabled"] == True): # Only check for relay-based alerts if relay alerts are enabled in the configuration.
        debug_message("Processing relay alerts")
        active_relay_alerts = [] # Set the active relay alerts to a blank placeholder so all of the active alerts this cycle can be added to it in the next step.
        for alert in config["general"]["relay_alerts"]["alerts"]:
            if (GPIO.input(config["general"]["relay_alerts"]["alerts"][alert]["gpio_pin"]) == config["general"]["relay_alerts"]["alerts"][alert]["alert_on_closed"]):
                if (config["general"]["gps_enabled"] == True):
                    if (float(current_speed) >= config["general"]["relay_alerts"]["alerts"][alert]["minimum_speed"] and float(current_speed) <= config["general"]["relay_alerts"]["alerts"][alert]["maximum_speed"]): # Check to see if the current speed falls within the range specified for this alert.
                        active_relay_alerts.append(config["general"]["relay_alerts"]["alerts"][alert]) # Add this alert to the list of active alerts for this cycle.
                else: # GPS features are disabled, so show the alert regardless of the current speed.
                    active_relay_alerts.append(config["general"]["relay_alerts"]["alerts"][alert]) # Add this alert to the list of active alerts for this cycle.

        debug_message("Processed relay alerts")
        return active_relay_alerts # Return the list of active relay alerts.

    else: # Relay alerts are disabled in the configuration.
        return [] # Return a blank placeholder list in place of the active relay alerts list.

