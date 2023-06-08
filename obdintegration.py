# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import obd
import time


import config
load_config = config.load_config

import utils
style = utils.style
debug_message = utils.debug_message
display_notice = utils.display_notice

# Locate and load the configuration file.
config = load_config()



def start_obd_monitoring():
    if (config["general"]["obd_integration"]["enabled"] == True): # Check to see if OBD integration is enabled.
        debug_message("Starting OBD integration")
        try:
            obd_connection = obd.OBD(config["general"]["obd_integration"]["device"]) # Attempt to open a connection to the ELM327 adapter.
            return obd_connection # Return the OBD connection object.
        except:
            display_notice("The OBD connection could not be established.", 3)
            return None # The OBD connection failed to be established, so return no data.
    return None # OBD integration is disabled, so return no data.



def fetch_obd_alerts(obd_connection):
    debug_message("Processing OBD alerts")

    obd_data = {} # This is a dictionary that holds raw OBD data as it is queried.
    obd_alerts = {} # This dictionary holds any values that fall into an alert threshold.

    if (obd_connection == None): # Check to see if the OBD connection does not exist.
        display_notice("The OBD connection is invalid. OBD alerts could not be processed.", 2)
    else:
        try: # Try to query the car for all configured attributes.
            if (config["general"]["obd_integration"]["values"]["speed"]["enabled"] == True): # Check to see if speed monitoring is enabled.
                debug_message("Querying OBD for speed")
                obd_data["speed"] = obd_connection.query(obd.commands.SPEED).value.to(str(config["display"]["displays"]["speed"]["unit"])).magnitude # Query the vehicle speed.
            if (config["general"]["obd_integration"]["values"]["rpm"]["enabled"] == True): # Check to see if RPM monitoring is enabled.
                debug_message("Querying OBD for RPM")
                obd_data["rpm"] = float(obd_connection.query(obd.commands.RPM).value.magnitude) # Query the engine RPM.
            if (config["general"]["obd_integration"]["values"]["fuel_level"]["enabled"] == True): # Check to see if fuel level monitoring is enabled.
                debug_message("Querying OBD for fuel level")
                obd_data["fuel_level"] = float(obd_connection.query(obd.commands.FUEL_LEVEL).value)/100 # Query the gas tank fuel level percentage as a decimal between 1 and 0.
            if (config["general"]["obd_integration"]["values"]["airflow"]["enabled"] == True): # Check to see if air flow rate monitoring is enabled.
                debug_message("Querying OBD for mass airflow")
                obd_data["airflow"] = float(obd_connection.query(obd.commands.MAF).value.magnitude) # Query the airflow rate from the mass-airflow sensor.
        except: # If the query fails, then return placeholder values for all configured attributes.
            display_notice("OBD information could not be queried.", 2)
            if (config["general"]["obd_integration"]["values"]["speed"]["enabled"] == True): # Check to see if speed monitoring is enabled.
                obd_data["speed"] = 0
            if (config["general"]["obd_integration"]["values"]["rpm"]["enabled"] == True): # Check to see if RPM monitoring is enabled.
                obd_data["rpm"] = 0
            if (config["general"]["obd_integration"]["values"]["fuel_level"]["enabled"] == True): # Check to see if fuel level monitoring is enabled.
                obd_data["fuel_level"] = 0
            if (config["general"]["obd_integration"]["values"]["airflow"]["enabled"] == True): # Check to see if air flow rate monitoring is enabled.
                obd_data["airflow"] = 0


        for value in config["general"]["obd_integration"]["values"]: # Iterate through each supported value.
            if (config["general"]["obd_integration"]["values"][value]["enabled"] == True): # Check to see if this value is enabled.
                if (obd_data[value] < config["general"]["obd_integration"]["values"][value]["thresholds"]["min"]): # Check to see if this value is lower than it's configured minimum value.
                    obd_alerts[value] = {"value": obd_data[value], "alert": "low"}
                elif (obd_data[value] > config["general"]["obd_integration"]["values"][value]["thresholds"]["max"]): # Check to see if this value is higher than it's configured maximum value.
                    obd_alerts[value] = {"value": obd_data[value], "alert": "high"}

    return obd_alerts, obd_data
