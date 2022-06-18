# Configuration

This document describes the configuration values found `config.json`.


## General Configuration

This section of configuration values will effect Assassin's general operation.

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


## Display Configuration

This section of configuration values effect Assassin's visual displays.

- `displays`
    - This configuration value allows the user to turn on and off each information display individually.
    - This allows the user to control what information they can see while driving.
- `large_critical_display`
    - This setting allows the user to determine whether or not they want critical messages to be shown in large ASCII font.
    - This can be useful to allow the user to quickly see critically important information at a glance, such as an imminent threat that requires immediate action.
- `shape_alerts`
    - This setting allows the user to turn on and off Assassin's "shape alerts", which are large ASCII shapes displayed when important events occur.
    - Shape alerts take up a lot of space on screen, but make it easy for the driver to understand a situation simply using their peripheral vision.
- `heading_as_cardinal_direction`
    - This setting determines if the current heading will be displayed as a cardinal direction, like "N", or "SE".
    - When set to `false`, the heading will be show in degrees off north, like "158" or "22".
- `ascii_art_header`
    - This configuration value determines whether or not Assassin will display a large title header upon start-up.
    - This this setting is set to `false`, Assassin will instead display a small, since line title.
- `custom_startup_message`
    - This setting defines a string that will be displayed the Assassin title upon start-up.
- `speed_display_unit`
    - This configuration value determines the unit that speeds will be displayed in.
    - The following speed units are supported:
        - "kph" for kilometers-per-hour
        - "mph" for miles-per-hour
        - "mps" for meters-per-second
        - "knot" for knots
        - "fps" for feet-per-second
- `big_speed_display`
    - This configuration value is used to determine whether or not Assassin will display the current speed in a large ASCII font at the top of the main display.
    - The `decimal_places` sub-value determines how many decimal places Assassin will show in the large speed display, if enabled.
- `status_lighting`
    - The status lighting configuration values allow Assassin to interact with a "WLED" RGB LED controller.
    - The `enabled` configuration value determines whether or not status lighting is enabled or disabled.
    - The `base_url` configuration value determines the base level URL that network requests will be made to in order to update the status lighting.
    - The `status_lighting_values` determine the exact URL that will be called for each condition.
        - The string `[U]` is replaced with the base URL defined earlier.


## Audio Configuration

This section of configuration values effect Assassin's audio functionality.

- `sounds`
    This configuration value determines all of the sounds that Assassin is capable of using.
    - Each sound has a `path`, `repeat`, and `delay` defined.
        - The `path` defines the file path of the sound file.
        - The `repeat` setting defines how many times the sound file is played each time the sound is triggered.
        - The `delay` setting defines how long code execution will be paused to allow the sound effect time to play.
            - It's important to note that this delay does not include the time spent playing the audio file. Therefore, a 0.5 second audio file with a 1 second delay will only leave 0.5 seconds of delay after the sound has finished playing.
