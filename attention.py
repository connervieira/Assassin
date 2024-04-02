# Assassin

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import json
import time

import config
load_config = config.load_config

import utils
style = utils.style
debug_message = utils.debug_message

# Locate and load the configuration file.
config = load_config()




# Define the function to print debugging information when the configuration specifies to do so.
attention_timer_start = time.time() # This variable holds the time that the attention timer was started.
attention_reset_start = time.time() - (float(config["general"]["attention_monitoring"]["reset_time"])*60) # This variable holds the time that the attention was lost. This is used to trigger a timer reset after a certain period of time. This value is initialize at the reset time threshold so that the attention timer doesn't start until the vehicle starts moving for the first time.

def process_attention_alerts(speed):
    if (config["general"]["attention_monitoring"]["enabled"] == True): # Check to make sure attention monitoring is enabled before processing alerts.
        global attention_timer_start
        global attention_reset_start

        attention_alerts = {} # Create a blank placeholder for the attention alerts.

        speed = float(speed) # Make sure the speed is a number.

        if (speed >= float(config["general"]["attention_monitoring"]["reset_speed"])): # If the speed is above the 'stopped' threshold, reset the reset timer.
            attention_reset_start = time.time() # Reset the reset timer.

        if (time.time() - attention_reset_start > float(config["general"]["attention_monitoring"]["reset_time"]) * 60): # Check to see if the reset timer has been active for longer than the reset threshold.
            attention_timer_start = time.time() # Reset the attention timer.

        if (time.time() - attention_timer_start > float(config["general"]["attention_monitoring"]["triggers"]["time"]) * 60): # Check to see if the attention timer has been active for longer than the alert trigger threshold.
            attention_alerts["time"] = {"active": True, "time": float(time.time() - attention_timer_start)} # Add a time alert to the alerts.

        return attention_alerts # Return the dictionary of active attention alerts.

    else: # Attention monitoring is disabled.
        return {} # Return a blank placeholder dictionary.

def get_current_attention_time():
    if (config["general"]["attention_monitoring"]["enabled"] == True): # Check to make sure attention monitoring is enabled before processing alerts.
        global attention_timer_start
        global attention_reset_start
        attention_time = time.time() - attention_timer_start
        reset_time = time.time() - attention_reset_start
        return [attention_time, reset_time]
    else: # Attention monitoring is disabled.
        return [0.0, 0.0]
