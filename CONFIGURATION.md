# Configuration

This document describes the configuration values found `config.json`.


## General Configuration

This section of configuration values will effect Assassin's general operation.

- `working_directory` is a path to the directory where Assassin will store files as it runs.
- `active_config_refresh` is a boolean that determines whether or not Assassin will refresh the configuration file every cycle.
    - Activating this setting can easily cause fatal errors, so it should only be used for testing.
    - This setting is not be honored by some of Assassin's libraries.
- `debugging_output` is a boolean that determines whether Assassin will operate in a verbose mode, where it prints out frequent status messages with timestamps. This is useful for debugging and for finding sources of delay.
    - If you enable this, considering enabling the `disable_console_clearing` to prevent debugging messages from being cleared.
- `disable_console_clearing` is a boolean that prevents the screen from being cleared.
    - Under normal circumstances, this should not be used because it will make Assassin's output extremely chaotic and unpredictable. However, there may be some situations in which it may be useful to disable output clearing.
- `tts` contains settings regarding text-to-speech, which allows Assassin to read out information verbally.
    - This section has the following sub-values for configuration.
        - `enabled` determines whether text to speech is enabled.
        - `brief` determines whether Assassin will use brief read-outs in place of the full length ones.
            - Enabling this will reduce the amount of information in text-to-speed read-outs, but will dramatically shorten the time it takes to deliver them.
        - `speed` determines the speed at which text-to-speech will be spoken.
- `gps` contains settings that configure Assassin's GPS behavior.
    - This setting has the following sub-values for configuration:
        - `enabled` is a boolean that globally enables or disables GPS functionality throughout Assassin.
            - It should be noted that the vast majority of Assassin's functionality depends on GPS. With it disabled, many important features will not function.
            - Disabling this configuration value may cause unexpected errors.
        - `provider` is a string that determines which GPS location provider Assassin will attempt to use.
            - Below are the options this value can be set to.
                - `gpsd`
                    - GPSD is suitable for nearly all devices, and is the default.
                - `termux`
                    - Termux uses the `termux-api` package to make it possible to run Assassin on Android.
                - `locateme`
                    - In the event GPSD isn't suitable, LocateMe for MacOS can be used as location back-end.
        - `speed_source` determines which source Assassin will use for its GPS speed.
            - Below are the options this value can be set to.
                - `gps` uses the speed as returned by the GPS hardware.
                - `obd` uses the speed returned by the ECU over OBD-II. This requires OBD integration to be enabled.
                - `calculated` uses the last two locations in the history to independently calculate the speed.
        - `demo_mode` is used to supply Assassin with fake GPS data for sake of demonstration and testing purposes.
            - To use this feature, simply set `enabled` to `true`, then set each GPS variable to any value you want. Assassin will use this placeholder information whenever it would otherwise poll the GPS for information.
        - `alerts` contains settings that control the behavior of various GPS alerts.
            - `enabled` is a boolean that enables and disables all GPS alerts.
            - `look_back` is an integer that determines the how many cycles Assassin will look back through the GPS history when analyzing GPS trends.
                - Shorter values will lead to marginally faster processing, and shorter alert latch times.
                - Longer values will detect older alerts, and will latch onto alerts for longer.
                - It should be noted that the true look back length is effectively one less than this value, since GPS alerts often compare two values. 
            - `overspeed` contains settings that control the behavior of GPS over-speed alerts.
                - `enabled` determines whether overspeed detection is on or off.
                - `max_speed` is an integer that determines the detected traveled speed (in miles per hour) that needs to be reached for a spoofing alert to be triggered.
                    - This metric independently calculates the speed using distance and time, and can be used to detected unexplained dramatic changes in position.
                    - You should set this value to the fastest speed you ever expect to go, plus a significant margin for jitter due to bridges, tunnels, and other obstructions that may decrease accuracy.
                    - True spoofing attempts will generally cause your detected position to move hundreds of miles in a matter of seconds, so you can safely set this threshold very high.
                - `prioritize_highest` is a boolean value that determines whether Assassin will prioritize the alert with the highest speed when multiple alerts are found in the location history.
                    - When this is set to `false`, the most recent alert will always be prioritized.
            - `no_data` contains settings that control alert behavior when there is no GPS data received.
                - `enabled` is a boolean that determines whether or not Assassin will trigger an alert when there is no GPS data received.
                - `length` is an integer value that determines how many sequential GPS requests need to return no data before an alert is triggered.
                    - Setting this to a value of 0 will always trigger alerts, even when GPS data is successfully returned.
                    - Setting this value to 1 will trigger an alert the moment no GPS data is returned.
                    - Setting this value to values higher than 1 will wait to trigger alerts until no data is returned multiple times sequentially.
            - `frozen` contains settings that control alert behavior when the GPS repeatedly returns identical data, indicating that the GPS might be frozen.
                - `enabled` is a boolean that determines whether or not Assassin will trigger an alert when the GPS appears to be frozen.
                - `length` is an integer value that determines how many sequential GPS requests need to be identical, not including the first instance.
                    - For example:
                        - If you want to trigger an alert when identical GPS data is returned 3 times sequentially, then this value should be set to 2.
                        - If you want to trigger an alert when identical GPS data is returned 5 times sequentially, then this value should be set to 4.
                    - Setting this to a value of 0 will always trigger alerts, even when GPS data is successfully returned.
                    - Setting this value to 1 will trigger an alert the moment two instances of identical GPS data are returned sequentially.
                    - Setting this value to values higher than 1 will wait to trigger alerts until identical data is returned multiple times sequentially.
            - `diagnostic` contains settings that control if and how Assassin issues diagnostic alerts.
                - `enabled` is a boolean that determines whether or not Assassin will issue a persistent alert that contains GPS diagnostic information.
                    - This feature might be useful if you want to issue basic dashboard information to an external program.
- `obd_integration` contains settings related to vehicle diagnostics integration using an ELM327 OBD-II adapter.
    - `enabled` is a boolean that determines whether or not the OBD integration system is active.
    - `device` specifies the path to the ELM327 USB device that Assassin will use to communicate with the car.
    - `values` contains the diagnostic values Assassin is capable of monitoring.
        - The following values are currently supported:
            - `speed` measures the speed of the vehicle, measured in the units specified by the `display > displays > speed > unit` configuration value.
            - `rpm` measures the revolutions of the engine, per minute.
            - `fuel_level` measures the current percentage of the fuel tank that is full, measured as a fraction between 0 and 1.
        - Each value has the following values for configuration:
            - `enabled` is a boolean value that determines whether or not Assassin will query this value at all.
            - `thresholds` sets the thresholds at which Assassin will display an alert for this value.
                - `min` is the minimum value permitted before an alert is returned.
                - `max` is the maximum value permitted before an alert is returned.
- `attention_monitoring` contains settings related to driver attention alerts.
    - `enabled` determines whether attention monitoring is active or not.
    - `reset_time` time is the length of time, in minutes, that the vehicle needs to be stationary for Assassin to reset the attention monitoring tracking.
        - This should be short enough that breaks from driving will cause a reset, but long enough that stopping for traffic won't.
    - `reset_speed` is the speed at which Assassin considers the driver to be actively driving. Any time this speed is exceeded, the reset timer resets.
        - This speed uses the units specified by the `display > displays > speed > unit` configuration value.
    - `triggers` lists criteria that will trigger an attention alert.
        - `time` is the length in time, in minutes, that need to elapse before Assassin triggers an attention alert.
- `telemetry` contains settings related to Assassin's telemetry recording behavior.
    - `enabled` determines whether Assassin will record telemetry at all.
    - `directory` is the directory that Assassin will save telemetry files to.
    - `file` is the file-name that Assassin will write the telemetry data to.
        - This file name should be a GPX file.
        - The `{T}` string will be replaced by the timestamp that the first location point was recorded.
            - If the `{T}` string doesn't appear anywhere in the file name, then Assassin will overwrite the file every time it runs.
        - Example: `AssassinTelemetry{T}.gpx`
    - `information` specifies what information will be saved to the telemetry file.
        - `altitude` is the GPS altitude.
        - `satellites` is the number of GPS satellites used to get the location.
        - `speed` is the current GPS speed in meters-per-second.
            - It should be noted that the speed can easily be determined from location information and timestamps, regardless of whether it directly is embedded in the file.
        - `source` is the location back-end Assassin used to get the location.
- `refresh_delay` is a floating point value that determines the amount of time, in seconds, that Assassin will wait at the beginning of each processing cycle before continuing.
    - It's important to note that this setting doesn't guarantee Assassin will refresh exactly at the interval specified. This delay is added in addition to the natural delay created by processing alerts and handling data.
- `weather_alerts` contains settings related to Assassin's weather alert capabilities.
    - `enabled` is a boolean that determines if weather alerts are active.
    - `api_key` is an [OpenWeatherMap](https://openweathermap.org) API key to retrieve weather information.
    - `refresh_interval` is an integer that determines how often Assassin will fetch new weather data.
        - This should be a number low enough that you receive regular updates, but not so low that you burn through allocated API requests too quickly.
    - `criteria` contains a dictionary of weather metrics, and the criteria under which an alert should be shown.
        - `visibility` is the current visibility, measured in meters.
            - This value maxes out at 10,000 meters, and will never go above it.
        - `temperature` is the current temperature, measured in Celsius.
        - `precipitation` is the current chance of precipitation.
- `predator_integration` contains settings related to Predator integration, which allows Assassin to show alerts detected by [Predator](https://v0lttech.com/predator.php).
    - `enabled` is a boolean that determines if Predator integration alerts are active.
    - `instance_directory` is a complete file-path that points to the root Predator instance directory (the directory containing `main.py`)
    - `start_predator` is a boolean value that determines whether Assassin will start Predator on start-up. If your use case involves Predator being started separately before Assassin starts, then you should change this configuration value to `false`.
    - `latch_time` is a floating point value that determines how many seconds Assassin will look back in the plate history for active alerts.
- `traffic_camera_alerts` contains settings related to traffic enforcement camera alerts.
    - `enabled` is a boolean value that determines whether or not traffic camera alerts are enabled or disabled.
    - `loaded_radius` is a decimal number that determines the radius, in miles, around the current location that Assassin will load traffic enforcement cameras during start-up.
        - The higher this value is, the longer Assassin will take the process traffic camera alerts each cycle.
        - The lower this value is, the smaller the loaded radius around the initial starting position will be.
            - A small loaded radius might pose an issue if you drive extremely far in a single session without restarting Assassin, since you'll reach the end of the loaded area.
        - Setting this to '0' will disable traffic enforcement camera alerts.
    - `database` is the file-path to an ExCam database containing traffic camera locations and information.
    - `speed_check` determines whether or not Assassin will consider the speed limit associated with a traffic camera when determining whether or not to alert to it.
        - This setting uses the `speed` threshold as defined in the `triggers` section.
        - When no speed limit data is available, Assassin will skip the speed check and alert normally regardless of the current speed.
    - `triggers` contains the criteria that need to be met for a traffic enforcement camera alert to be triggered.
        - `distance` is the distance in miles away from a traffic camera that Assassin will trigger an alert.
        - `speed` is the minimum speed, relative to the camera's speed limit required for Assassin to trigger an alert, measured in the units specified by the `display>displays>speed>unit` configuration value.
            - For example, if a camera has a speed limit of 25 mph, and this value is set to 5 mph, then Assassin will trigger an alert at 30 mph.
        - `angle` determines the maximum allowed difference between the current direction of movement, and direction the camera monitors.
            - This setting can be used to eliminate alerts from cameras that face directions different from the current direction of travel.
            - Values higher than 180 will effectively disable this filter.
        - `direction` determines the maximum allowed bearing to the camera, relative to the cirrent direction of movement before the alert is filtered out.
            - You can think of this value as a way to specify the width of the imaginary cone in front of your car, where cameras outside of the cone are filtered out.
            - This setting can be used to eliminate alerts from cameras that have already been passed, or cameras that are on adjacent roads.
            - Values higher than 180 will effectively disable this filter.
    - `enabled_types` controls which types of enforcement cameras Assassin will alert to.
        - `speed` enables and disables speed camera alerts.
        - `redlight` enables and disables red light camera alerts.
        - `misc` enables and disables all other camera types, including unknown cameras.
    - `information_displayed` determines what information is displayed in alerts.
        - This value is a dictionary containing all the information Assassin is capable of displaying. Set each value to `true` or `false` to enable or disable it.
- `drone_alerts` contains settings related to Assassin's unmanned device alert behavior.
    - `enabled` toggles the entire drone detection system on and off.
    - `save_detected_hazards` determines whether or not Assassin will save the radio devices it deems to be hazards to a local file for later analysis.
    - `save_detected_devices` determines whether or not Assassin will save the all radio devices it detects to a local file for later analysis.
        - Be warned that this file can become extremely large in just a few minutes, especially if you happen to be in an area with a lot of radio traffic.
    - `monitoring_device` determines the wireless device that Assassin will attempt to use to run wireless network analysis.
        - To list the network devices available on your system, use the `iwconfig` command. Note that this lists all network interfaces, not just wireless ones.
    - `monitoring_mode` determines whether Assassin will attempt to automatically setup wireless monitoring, or prompt the user to manually start it.
        - Due to permissions, it's extremely common for automatic starting to fail, so manual is recommended for most situations.
        - This setting can only be set to `manual` or `automatic`
    - `hazard_latch_time` is how long (in seconds) Assassin will latch onto alerts after they are no longer detected before dismissing them.
    - `alert_types` determines what types of devices in the drone alert database that Assassin will alert to.
        - This is useful if you only want to alert to certain types of autonomous threats without needing to completely remove them from the database.
    - `information_displayed` determines what information is displayed in alerts.
        - This value is a dictionary containing all the information Assassin is capable of displaying. Set each value to `true` or `false` to enable or disable it.
- `alpr_alerts` contains settings related to automatic license plate recogntion camera alerts.
    - `enabled` is a boolean that determines whether or not ALPR camera alerts are enabled.
    - `alert_range` is the alert distance, in miles.
        - Setting this to '0' will effectively disable ALPR camera alerts.
    - `database` is the file-path to the ALPR database containing ALPR camera locations and information.
    - `loaded_radius` is a decimal number that determines the radius, in miles, around the current location that Assassin will load ALPR cameras during start-up.
        - The higher this value is, the longer Assassin will take the process ALPR camera alerts each cycle.
        - The lower this value is, the smaller the loaded radius around the initial starting position will be.
            - A small loaded radius might pose an issue if you drive extremely far in a single session without restarting Assassin, since you'll reach the end of the loaded area.
        - Setting this to '0' will disable ALPR camera alerts.
    - `filters` contains settings that control how Assassin filters out useless or unwanted alerts.
        - `angle_threshold` determines the maximum allowed difference between the current direction of movement, and the camera's angle before the alert is filtered out.
            - This setting can be used to eliminate alerts from cameras that aren't at an angle to see the license plate of the car.
            - Values higher than 180 will effectively disable this filter.
        - `direction_threshold` determines the maximum allowed bearing to the camera before the alert is filtered out.
            - This setting can be used to eliminate alerts from cameras that have already been passed, or cameras that are on adjacent roads.
            - Values higher than 180 will effectively disable this filter.
        - `duplicate_filtering` contains settings that control how Assassin filters out duplicate ALPR alerts.
            - `enabled` is a boolean value that sets whether or not de-duplication is enabled.
            - `distance` is the maximum distance between two cameras, measured in miles, before they are no longer considered to be duplicates.
            - `angle` is the maximum difference in the direction two cameras are facing, measured in degrees, before they are considered no longer considered to be duplicates.
    - `information_displayed` determines what information is displayed in alerts.
        - This value is a dictionary containing all the information Assassin is capable of displaying. Set each value to `true` or `false` to enable or disable it.
- `adsb_alerts` contains settings related to Assassin's aircraft threat alerting behavior.
    - The `enabled` value enables and disables the entire ADS-B system.
    - The `threat_threshold` determines how likely a plane is to be a threat before Assassin displays it as an alert. A plane has to match all of the criteria at its threshold level, and all levels below it.
        - A threshold of `0` includes all aircraft detected.
        - A threshold of `1` includes all aircraft within the alert distance threshold.
            - This is a good threshold to use if you want to be certain you don't miss any legitimate alerts.
        - A threshold of `2` includes aircraft within the alert altitude range.
        - A threshold of `3` includes aircraft within the alert speed range.
            - This is a good threshold to use if you want to eliminate as many false alerts as positive.
    - The `minimum_vehicle_speed` setting defines the minimum GPS speed that ADS-B alerts will be triggered at, measured in the units specified by the `display>displays>speed>unit` configuration value. This is useful to prevent alerts from sounding while the car is on residential roads.
    - `message_time_to_live` is a floating point value that determines how long (in seconds) received in ADS-B messages will be considered before discarding their information. This prevents planes that haven't been detected for an extended period from clogging up the alert procesing with outdated information.
        - If certain information is missing from a message, Assassin will look back through old messages within this time-frame to find it. As such, increasing this configuration value will trade information recency for resiliency and fault tolerance.
        - If you find that enabling ADS-B alerts causes Assassin to dramatically slow down after a few moments of running, decreasing this value should significantly decrease processing time.
    - `prune_interval` is a floating point value that determines how long (in seconds) the ADS-B message maintainer will wait between rounds of pruning expired messages.
        - The higher this value is, the more processor intensive each processing cycle will be, since there will be more messages to scan. However, setting this value too low can cause the ADS-B message file to be cleared so often that Assassin will start reading an empty file.
    - `criteria` contains the alert criteria for aircraft.
        - `speed` contains the speed range that aircraft hazards are expected to moving, measured in knots.
            - The `minimum` setting defines the minimum aircraft speed that ADS-B alerts will be triggered at. This is useful to filter alerts from aircraft that aren't at cruising speed.
            - The `maximum` setting defines the maximum aircraft speed that ADS-B alerts will be triggered at. This is useful to filter alerts from aircraft that are moving faster than specific models of aircraft are capable of.
        - `altitude` contains the altitude range that aircraft hazards are expected to at, measured in feet.
            - The `minimum` setting defines the minimum aircraft altitude that ADS-B alerts will be triggered at.
            - The `maximum` setting defines the maximum aircraft altitude that ADS-B alerts will be triggered at.
        - `distance` contains criteria regarding the distance between the aircraft and the vehicle.
            - The `base_distance` setting defines the base distance (in miles) that ADS-B aircraft alerts will be played at. This distance will be adjusted based on the altitude of the plane in question.
            - The `base_altitude` setting defines the altitude at which the alert distance threshold will be the same as the distance defined by the `distance_threshold` configuration value.
                - Below the base altitude, the alert radius will be proportionally decreased, and above the base altitude, the alert radius will be proportionally increased.
                - This value should be roughly be the altitude that you expect aircraft threats to be at. Any aircraft above that altitude will be able to see farther, so the alert distance will increase. By the same logic, lower aircraft have a lower vision radius, so the alert distance decreases.
    - `information_displayed` determines what information is displayed in alerts.
        - This value is a dictionary containing all the information Assassin is capable of displaying. Set each value to `true` or `false` to enable or disable it.
- `bluetooth_scanning` contains settings that control how Assassin scans for Bluetooth tracking devices.
    - `enabled` determines whether Bluetooth scanning is enabled or disabled.
    - `memory_time` is the length of time (measured in minutes) after which Assassin will "forget" a Bluetooth device.
        - Behind the scenes, Assassin actually keeps track of the original time/location that each device was seen. This value simply changes how Assassin determines what devices are considered threats.
        - For example, if you are traveling with someone in separate cars, Assassin may detect the other driver's devices before leaving. Once the destination has been reached, these devices may come back into detection range. Since the device was out of range through-out the trip, the memory time will prevent the device from being considered a threat.
    - `thresholds` contains criteria under which Assassin will alert to Bluetooth devices.
        - `time` controls alerts based on the length of time a device has been detected for.
            - `enabled` is a boolean that determines if this type of alert is enabled.
            - `limit` is the number of seconds between the first-seen time and last-seen time before Assassin considers this device to be a threat.
        - `distance` controls alerts based on the distance between the first-seen location, and last-seen location.
            - `enabled` is a boolean that determines if this type of alert is enabled.
            - `limit` is the number of miles between the first-seen location and last-seen location before Assassin considers this device to be a threat.
    - `whitelist` contains a list of devices that Assassin will never alert to.
        - The whitelist should contain devices that you expect to "follow" you everywhere you go, including your phone, laptop, or personal trackers.
        - Each entry in the whitelist uses a colon separated MAC address (in all uppercase letters) as the key, and a friendly name as a value.
            - Example: `"FF:FF:FF:FF:FF:FF": "My Phone"
    - `blacklist` contains a list of devices that Assassin will immediately consider threats, regardless of the following time or distance.
        - The blacklist should contain devices that you always want to know about if they come within detection range.
            - The blacklist may contain something as serious as the devices of someone you suspect to be tracking you, or something as simple a friend's device, such that you receive an alert when passing them.
        - Each entry in the blacklist uses a colon separated MAC address (in all uppercase letters) as the key, and a friendly name as a value.
            - Example: `"FF:FF:FF:FF:FF:FF": "My Phone"


## Display Configuration

This section of configuration values effect Assassin's visual displays.

- `silence_console_displays` is a boolean value that determines whether all alerts and information displays will be disabled in the console output.
    - This might be useful if you use an external interface for Assassin, and only want diagnostic, debug, error, and warning messages to be displayed.
- `displays` contains values that allow the user to turn on and off each information display individually.
    - `time` can be toggled on and off.
    - `date` can be toggled on and off.
    - `speed` has several configuration values.
        - `small_display` toggles the small, single line speed text display on and off.
        - `large_display` toggles the large, ASCII font speed display on and off
        - `decimal_places` determines how many decimal places will be displayed in both speed display types.
        - `unit` determines the unit of speed that Assassin will use.
            - "kph" for kilometers-per-hour
            - "mph" for miles-per-hour
            - "mps" for meters-per-second
            - "knot" for knots
            - "fps" for feet-per-second
    - `location` can be toggled on and off.
    - `altitude` can be toggled on and off.
    - `heading` has several configuration values.
        - `degrees` determines whether or not the current heading will be displayed in degrees off north. When both `degrees` and `direction` are enabled, the degrees will be displayed in parenthesis after the cardinal direction.
        - `direction` determines whether or not the current heading will be displayed as a cardinal direction, such as 'N', 'SW', or 'E'.
    - `satellites` can be toggled on and off, and shows how many GPS satellites are connected.
    - `planes` can be toggled on and off, and shows many many aircraft are being detected. This is dependent on the ADS-B alerts system and requires `adsb_alerts` to be enabled.
    - `bluetooth` can be toggled on and off, and shows many many total Bluetooth devices are being detected. This is dependent on the Bluetooth alerts system and requires `bluetooth_scanning` to be enabled.
- `shape_alerts`
    - This setting allows the user to turn on and off Assassin's "shape alerts", which are large ASCII shapes displayed when important events occur.
    - Shape alerts take up a lot of space on screen, but make it easy for the driver to understand a situation simply using their peripheral vision.
- `ascii_art_header`
    - This configuration value determines whether or not Assassin will display a large title header upon startup.
    - This this setting is set to `false`, Assassin will instead display a small, since line title.
- `custom_startup_message`
    - This setting defines a string that will be displayed the Assassin title upon startup.
- `status_lighting`
    - The status lighting configuration values allow Assassin to interact with a "WLED" RGB LED controller.
    - The `enabled` configuration value determines whether or not status lighting is enabled or disabled.
    - The `delay` configuration value is a position floating point number that determines how long Assassin will wait for after updating the status lighting.
        - This allows you to see multiple alerts each cycle, without the previous alert being immediately replaced with the subsequent ones.
    - The `base_url` configuration value determines the base level URL that network requests will be made to in order to update the status lighting.
    - The `status_lighting_values` determine the exact URL that will be called for each condition.
        - The string `[U]` is replaced with the base URL defined earlier.
- `notices`
    - This configuration value contains all of the different levels of notices Assassin can show the user when issues are encountered. Level 1 indicates basic notices, level 2 indicates warnings, and level 3 indicates errors.
    - Each notice level has the following configuration values:
        - `wait_for_input` indicates whether Assassin should pause, and prompt the user to press enter to continue. This can be useful to allow the user to read the message at their own pace before continuing, but it can lead to situations where the user doesn't notice the message while driving, and Assassin remains paused.
        - `delay` indicates how long, in seconds, Assassin should allow the message to be read before continuing. This delay is only used when `wait_for_input` is disabled.


## Audio Configuration

This section of configuration values effect Assassin's audio functionality.

- `provider` determines the back-end that Assassin will use to play audio.
    - This value can be set to the following options:
        - `mpg321` will use the MPG321 command line utility.
        - `playsound` will use Python's playsound library.
- `sounds` contains settings related to how Assassin handles audio alerts.
    - This configuration value determines all of the sounds that Assassin is capable of using.
    - Different sounds are triggered by different events.
        - The `heartbeat` sound plays at the beginning of every cycle.
        - The `startup` sound is played when Assassin initially loads.
        - The `camera` sounds are played during a traffic camera alert.
            - `camera1` indicates a low priority alert.
            - `camera2` indicates a medium priority alert.
            - `camera3` indicates a high priority alert.
        - The `alarm` sound plays during a heightened alarm state.
            - This sound is reserved for times in which immediate action is required.
            - Normal alert noises will play before this, and this sound will only be played if the other alerts aren't acknowledged and resolved.
        - The `alpr` sound plays during an ALPR camera alert.
        - The `drone` sound is played during an autonomous wireless threat alert.
        - The `adsb` sound is played during an aircraft alert.
        - The `bluetooth` sound is played during a Bluetooth alert.
        - The `gps` sound is played during a GPS spoof detection alert.
    - Each sound has a `path`, `repeat`, and `delay` defined.
        - The `path` defines the file path of the sound file.
            - This file path can be relative to the Assassin directory, or an absolute path.
        - The `repeat` is an integer that defines how many times the sound file is played each time the sound is triggered.
            - When `repeat` is set to zero for a particular sound, that should will be disabled.
        - The `delay` is a decimal number that defines how long code execution will be paused to allow the sound effect time to play.
            - It's important to note that this delay does not include the time spent playing the audio file. Therefore, a 0.5 second audio file with a 1 second delay will only leave 0.5 seconds of delay after the sound has finished playing.


## External Service Configuration

This section contains configuration values that control how Assassin interacts with external services.

- `local` contains settings relating to how Assassin communicates with local programs.
    - `enabled` is a boolean value that determines whether or not Assassin will publish information for local programs to read.
    - `interface_directory` is a string that determines an absolute directory path where Assassin will store files used to publish information to external programs.
        - Example: `/home/assassin/Documents/Assassin/interface`
