# Assassin

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




import requests
import json
import os
import time

import utils
style = utils.style
load_config = utils.load_config
debug_message = utils.debug_message

# Locate and load the configuration file.
config = load_config()


def get_weather_data(location, last_weather_data):
    debug_message("Retrieving weather information")

    time_since_request = round(time.time()) - int(last_weather_data["requested"]) # Calculate how many seconds have passed since the last API request was made.

    if (time_since_request > int(config["general"]["weather_alerts"]["refresh_interval"])): # Check to see if the refresh interval has been exceeded.
        lat = location[0]
        lon = location[1]
        api_key = config["general"]["weather_alerts"]["api_key"]
        url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

        response = requests.get(url)
        data = json.loads(response.text)
        data["requested"] = round(time.time())
    else: # The refresh interval has not be exceeded, so re-supply the old data and don't make a new API request.
        data = last_weather_data

    return data


def weather_alert_processing(weather_data):
    if (config["general"]["weather_alerts"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Check to make sure weather alerts are enabled.
        debug_message("Processing weather alerts")
        weather_alerts = {} # Set the list of active weather alerts to a blank placeholder.

        if (weather_data["visibility"] > config["general"]["weather_alerts"]["criteria"]["visibility"]["above"]): # Check to see if the visibility is above the alert criteria.
            weather_alerts["visibility"] = [weather_data["visibility"], "above"] # Add this alert to the dictionary of alerts.
        elif (weather_data["visibility"] < config["general"]["weather_alerts"]["criteria"]["visibility"]["below"]): # Check to see if the visibility is below the alert criteria.
            weather_alerts["visibility"] = [weather_data["visibility"], "below"] # Add this alert to the dictionary of alerts.

        if (weather_data["main"]["temp"] > config["general"]["weather_alerts"]["criteria"]["temperature"]["above"]): # Check to see if the temperature is above the alert criteria.
            weather_alerts["temperature"] = [weather_data["main"]["temp"], "above"] # Add this alert to the dictionary of alerts.
        elif (weather_data["main"]["temp"] < config["general"]["weather_alerts"]["criteria"]["temperature"]["below"]): # Check to see if the temperature is below the alert criteria.
            weather_alerts["temperature"] = [weather_data["main"]["temp"], "below"] # Add this alert to the dictionary of alerts.

    return weather_alerts
