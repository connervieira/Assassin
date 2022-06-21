# Configuration

This document describes the configuration values found `config.json`.


## General Configuration

This section of configuration values will effect Assassin's general operation.

- `active_config_refresh`
    - This setting determines whether or not Assassin will refresh the configuration file every cycle.
    - Activating this setting can easily cause fatal errors, so it should only be used for testing.
- `gps_enabled`
    - This setting is used to globally enable and disable GPS functionality throughout Assassin.
- `gps_demo_mode`
    - This setting is used to supply Assassin with fake GPS data for sake of demonstration purposes.
    - To use this feature, simply set `enabled` to `true`, then set each GPS variable to any value you want. Assassin will use this fake information whenever it would otherwise poll the GPS for information.
- `record_telemetry`
    - This setting determines whether Assassin will record telemetry data about it's location, speed, direction, and state.
    - To be clear, this information is never sent to an external service or logged for sake of analytics. All information collected remains local on the device.
- `alert_range`
    - This setting determines the alert range, in miles, of each point-of-interest database type.
- `refresh_delay`
    - This setting determines how long Assassin will wait between refreshes in seconds. Generally, 1 second is appropriate, but you can increase or decrease the delay to improve precision, or save processing power.
- `alert_databases`
    - This configuration value defines the file path to each of the different alert databases.
- `camera_alert_types`
    - This configuration value allows the user to set which types of enforcement cameras Assassin will alert to individually.
- `traffic_camera_loaded_radius`
    - This configuration value determines the radius around the current location that Assassin will load traffic enforcement cameras from.
    - The higher this value is, the longer Assassin will take the process traffic camera alerts each cycle.
    - The lower this value is, the smaller the loaded radius around the initial starting position will be.
        - A small loaded radius might pose an issue if you drive extremely far in a single session without restarting Assassin, since you'll reach the end of the loaded area.
- `traffic_camera_speed_check`
    - This configuration value determines whether or not Assassin will attempt to check the current speed against nearby speed enforcement cameras to inform the driver when they are at risk of getting a ticket.
    - Note that traffic enforcement camera speed checks are not always possible, since not all cameras in the database have speed limit information embedded.
- `drone_alerts`
    - Drone alerts are Assassin's system for detector drone aircraft, speed cameras, and other autonomous wireless threats.
    - This setting has the following sub-values for configuration:
        - `enabled` toggles the entire drone detection system on and off.
        - `save_detect_hazards` determines whether or not Assassin will save the drone hazards it detects to a local file for later analysis.
        - `monitoring_device` determines the wireless device that Assassin will attempt to use to run wireless network analysis.
        - `monitoring_mode` determines whether Assassin will attempt to automatically setup wireless monitoring, or prompt the user to manually start it. Due to permissions, it's extremely common for automatic starting to fail, so manual is recommended for most situations.
            - This setting can only be set to "manual" or "automatic"
        - `hazard_latch_time` is how long (in seconds) Assassin will latch onto alerts after they are no longer detected before dismissing them.
        - `alert_types` determines what types of devices in the drone alert database that Assassin will alert to. This is useful if you only want to alert to certain types of autonomous threats.
- `relay_alerts`
    - Relay alerts allow the user to connect custom relays via GPIO pins, and have Assassin alert to events from them.
    - The `enabled` configuration value enables and disables the entire relay alert system.
    - Each relay alert is defined under the `alerts` configuration value, and has the following information associated with it:
        - `title` is simply the title of the relay alert.
        - `message` is the message shown when the relay alert is activated.
        - `gpio_pin` is the GPIO pin ID that this relay is connected to.
        - `alert_on_closed` determines whether or not this alert should trigger when the relay closes or opens.
        - `minimum_activation_speed` defines the minimum GPS speed that this alert will activate at. This is useful if your connected device requires the vehicle to be moving.
        - `maximum_activation_speed` defines the maximum GPS speed that this alert will activate at. This is useful if your connected device requires the vehicle to be below a certain speed.
- `bluetooth_monitoring`
    - Bluetooth monitoring allows Assassin to detect nearby Bluetooth devices, and monitor when a particular device has been following for a suspiciously long distance.
    - `enabled` determines whether the Bluetooth monitoring system is enabled or disabled.
    - `scan_time` determines how long (in seconds) that Assassin will scan for Bluetooth devices each cycle.
    - `minimum_followin_distance` the minimum distance (in miles) that a device has to follow Assassin before an alert will be displayed.
    - `whitelist` allows the user to whitelist devices that are supposed to be following, like their car's stereo or their cell phone.
        - The `enabled` value enables or disables the whitelist.
        - The `devices` contains dictionary entries where the device's MAC address is the key, and a human readable name is the value.
    - `blacklist` allows the user to specify devices that Assassin should immediately alert to, regardless of whether they've been following.
        - The `enabled` value enables or disables the blacklist.
        - The `devices` contains dictionary entries where the device's MAC address is the key, and a human readable name is the value.
- `adsb_alerts`
    - ADS-B alerts allow Assassin to monitor and analyze aircraft in surrounding areas as a way to detect potential threats.
    - The `enabled` value enables and disables the entire ADS-B system.
    - The `minimum_speed` setting defines the minimum GPS speed that ADS-B alerts will be triggered at. This is useful to prevent alerts from sounding while the car is on residential roads.
    - The `distance_threshold` setting defines the base distance (in miles) that ADS-B aircraft alerts will be played at. This distance will be adjusted based on the altitude of the plane in question.
    - The `base_altitude_threshold` setting defines the altitude at which the alert distance threshold will be the same as the distance defined by the `distance_threshold` configuration value.
        - Below the base altitude threshold, the distance threshold will be proportionally decreased, and above the base altitude threshold, the distance threshold will be proportionally increased.
        - The `base_altitude_threshold` should roughly be the altitude that you expect hazardous planes to be at. Any planes above that altitude will be able to see farther, so the alert distance will increase. By the same logic, lower planes pose less of a threat, so the alert distance decreases.


## Display Configuration

This section of configuration values effect Assassin's visual displays.

- `displays`
    - This configuration value allows the user to turn on and off each information display individually.
    - This allows the user to control what information they can see while driving.
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
    - `satellites` can be toggled on and off.
- `large_critical_display`
    - This setting allows the user to determine whether or not they want critical messages to be shown in large ASCII font.
    - This can be useful to allow the user to quickly see critically important information at a glance, such as an imminent threat that requires immediate action.
- `shape_alerts`
    - This setting allows the user to turn on and off Assassin's "shape alerts", which are large ASCII shapes displayed when important events occur.
    - Shape alerts take up a lot of space on screen, but make it easy for the driver to understand a situation simply using their peripheral vision.
- `ascii_art_header`
    - This configuration value determines whether or not Assassin will display a large title header upon start-up.
    - This this setting is set to `false`, Assassin will instead display a small, since line title.
- `custom_startup_message`
    - This setting defines a string that will be displayed the Assassin title upon start-up.
- `status_lighting`
    - The status lighting configuration values allow Assassin to interact with a "WLED" RGB LED controller.
    - The `enabled` configuration value determines whether or not status lighting is enabled or disabled.
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

- `sounds`
    This configuration value determines all of the sounds that Assassin is capable of using.
    - Each sound has a `path`, `repeat`, and `delay` defined.
        - The `path` defines the file path of the sound file.
            - This file path can be relative to the Assassin directory, or an absolute path.
        - The `repeat` setting defines how many times the sound file is played each time the sound is triggered.
            - When `repeat` is set to zero for a particular sound, that sould will be disabled.
        - The `delay` setting defines how long code execution will be paused to allow the sound effect time to play.
            - It's important to note that this delay does not include the time spent playing the audio file. Therefore, a 0.5 second audio file with a 1 second delay will only leave 0.5 seconds of delay after the sound has finished playing.
