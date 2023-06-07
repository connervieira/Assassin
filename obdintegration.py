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

    obd_data = []

    if (obd_connection == None): # Check to see if the OBD connection does not exist.
        display_notice("The OBD connection is invalid. OBD alerts could not be processed.", 2)
    else:
        if (config["general"]["obd_integration"]["values"]["speed"]["enabled"] == True): # Check to see if speed monitoring is enabled.
            obd_data["speed"] = obd_connection.query(obd.commands.SPEED).value.to(str(config["display"]["displays"]["speed"]["unit"])) # Query the vehicle speed.
        if (config["general"]["obd_integration"]["values"]["rpm"]["enabled"] == True):
            obd_data["rpm"] = obd_connection.query(obd.commands.RPM).value # Query the engine RPM.

    return obd_data
