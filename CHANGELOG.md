# Changelog

This document contains a list of all the changes for each version of Assassin.


## Version 0.9

### Initial Release

October 30th, 2022

- Core functionality
    - Information dashboard
    - Traffic enforcement camera alerting
    - ALPR camera alerting
    - Drone/autonomous threat detection
    - Bluetooth threat detection
    - ADS-B aircraft detection


## Version 1.0

### First Stable Release 

December 13th, 2022

- Added several tools.
    - Added database preview tool.
    - Added database verify tool.
- Adjusted the configuration layout.
    - All alerts now have their own configuration sections.
- Updated ALPR alerting.
    - Each ALPR alert can now display additional information, including the following:
        - Camera brand
        - Camera operator
        - Camera type
        - Camera description
    - All information displayed in each alert can now be toggled on and off individually in the configuration.
    - ALPR alerts will now show the number of active alerts, in addition to the nearest alert.
    - ALPR alerts now display the location of the camera.
        - This is combined with the 'direction-to' display.
    - Added ALPR alert filtering.
        - Alerts can be filtered by direction.
            - This prevents cameras that are behind or to the side from triggering alerts.
        - Alerts can be filtered by angle.
            - This prevents from ALPR cameras from triggering alerts when they are at an angle that can't read the license plate of the car.
- Updated traffic enforcement camera alerting.
    - All information displayed in each alert can now be toggled on and off individually in the configuration.
    - Traffic camera alerts will now show the number of active alerts, in addition to the nearest alert.
    - The relative direction to and absolute bearing to the camera is now displayed in the alert.
    - Fixed speed check text alerting.
    - Added units to the speed limit text.
- Updated aircraft alerting.
    - All information displayed in each alert can now be toggled on and off individually in the configuration.
    - The total number of active aircraft alerts is now displayed at the start of the alert.
- Updated Bluetooth alerting.
    - Bluetooth alerts now have a title, like other alerts.
    - Alerts now display the total number of alerts detected at the top of each alert.
    - Alerts are now displayed as multiple lines to be more consistent with other alerts.
        - Each line of information can be enabled or disabled in the configuration.
- Updated drone alerting.
    - Fixed a typo where the packet count was prefixed by "channel" instead of "packets".
    - All information displayed in each alert can now be toggled on and off individually in the configuration.
    - Drone alerts are now sorted by signal strength.
    - The total number of hazards is now displayed in the title of the alert.
- Made the spacing between alerts more consistent.
- Added additional GPS location providers.
    - Termux-API can be used to allow Assassin to run on Android.
    - LocateMe can be used to make Assassin easier to run on MacOS.
- All disabled alerts will now supply empty data, instead of none at all.
    - This makes Assassin more stable, in the event that a disabled alert inadvertently gets called.
- Updated some sounds effects.
    - The aircraft alert sound effect is now much shorter.
    - Added an optional heartbeat sound effect to indicate when Assassin is active.
    - Added a drone sound effect.
    - Added a start-up sound effect.
- Re-arranged the dispaly order of alerts.
- Updated interface coloring.
    - Multiple alerts now share the same color.
    - Colors are now used to indicate categories, not specific alerts.
- Updated telemetry logging.
    - Assassin now logs telemetry information to a GPX file.
    - Data points, file names, and save directories can be customized in the configuration.
- Added a configuration option to disable diagonal arrows.
    - When diagonal arrows are disabled, Assassin will point in increments of 90 degrees instead of 45.
- Removed relay alert logic.
- Added text to speech support.


## Version 2.0

### Interface Update

March 22nd, 2023

This update adds the ability to interface with external services to enable new functionality, like a graphical user interface and internet based alerts.

- Added weather alert system.
- Rearranged GPS configuration options.
    - All GPS settings are now in their own category.
- Added basic GPS spoof detection system.
- Moved text-to-speech configuration to the 'audio' section.
- Added rounding to altitude and heading displays.
- Added driver attention monitoring alert system.
- Re-developed traffic camera alert handling.
    - Simplified the traffic camera alert handling process.
    - Fixed an issue where the type of a given camera couldn't be identified.
    - Fixed an issue where traffic camera alerts were stored in unexpected ways.
        - Previously, traffic camera alerts were held in disorganized duplicate nested lists depending on the number of alerts, instead of all in one single list.
    - Fixed an issue where the calculated bearing to a speed camera was reversed.
    - Traffic cameras are now sorted by distance in the back-end.
- Added local interface support, where all alerts can be stored in a local file to communicate with external local programs.
- Refined ALPR camera alerts.
    - ALPR camera alerts are now sorted by distance in the back-end.
    - Fixed an issue where ALPR alerts would be filtered improperly.
- Fixed an issue where Bluetooth alerts wouldn't be color coded properly when multiple alerts were displayed.
- Improved ADS-B alert handling.
    - Fixed a bug in the aircraft distance sorting algorithm where 1 aircraft would be thrown out during the sorting process.
    - The direction of the aircraft is now display relative to the current direction of movement.


## Version 3.0

### Stability Update

April 10th, 2023

This update focuses on improving stability, reliability, and usability.

- Improved aircraft alert processing.
    - The ADS-B intake process is now automatic, and is managed by Assassin.
    - Aircraft with no location data are now filtered from the alert display.
    - Improved the resiliency of the data intake process.
    - Fixed an issue where the message intake file could grow exponentially.
    - Renamed the "Planes" display to "Aircraft".
- Improved drone alert process.
    - The wireless threat database can now contain full MAC addresses to identify individual devices.
    - The drone detection process now considers all Airodump-NG output files, not just the first.
    - Automatic start-up mode is not significantly more reliable.
- Improved the Bluetooth alert process.
    - Bluetooth scanning is now done on a separate thread to prevent Assassin from freezing during scanning.
    - There is now a dedicated Bluetooth display in the main information display that shows the number of Bluetooth devices currently detected.
    - Added alert latch time configuration value to prevent alerts from being displayed until Assassin restarts after they are triggered.
- Improved GPS alert process.
    - The GPS alert configuration section has been re-organized for sake of clarity.
    - GPS no-data alerts can now be configured the require multiple sequential instances of no GPS data being returned before an alert is triggered.
    - Improved overspeed alerts.
        - GPS alerts overspeed alerts are no longer triggered when no GPS data is received.
        - Overspeed alerts can now be configured to prioritize the highest speed alert when multiple alerts are triggered at once.
    - Added support for frozen GPS alerts, where alerts can be triggered when exactly identitical GPS data is received repeatedly.
    - GPS alerts are now detected in chronological order, such that the process looks through the location history in order from oldest to most recent.
    - Alert types in the GPS alert display are now capitalized.
- Modified the loading process for ALPR camera and traffic cameras.
    - ALPR cameras now load based on the current location.
        - The loaded radius can be set in the configuration.
    - The initial GPS location lock is now acquired separately from the loading process, then passed to the loading functions.
- Re-organized the GPS demo-mode configuration.
- Fixed an issue where errors could sometimes occur when the local interface directory was disabled.
- Added attention monitoring timer display option.
- Moved GPS functions to a dedicated file for sake of organization.


## Version 3.1

April 19th, 2023

- Fixed a bug that would cause a hard crash when drone threat logging was disabled.
- Improved the stability of the drone data parsing process.


## Version 4.0

### Name Pending

*Release date to be determined*

- Refined the POI database format.
    - The ALPR camera database has been updated to reflect these changes, and includes additional refinements as well.
- Refined the configuration loading process.
    - Functions related to configuration loading and validation have been moved to a dedicated script, titled `config,py`
    - The configuration is now validated at startup based on an outline template.
- Added support for GPS diagnostic alerts, which simply issue an alert containing the most recent GPS information.
- Created a dedicated working directory configuration value.
    - Removed the telemetry directory configuration value.
    - Renamed the `general > adsb_alerts > adsb_message_file` configuration value to `adsb_message_filename`, which is now only a file name that is saved to the dedicated working directory.
- Moved the drone detection working directory to the new general working directory.
- Improved ADS-B alerts.
    - Updated the way the minimum vehicle speed configuration value is handled.
        - This value is now considered during alert processing, instead of when alerts are displayed. This improves efficiency, and means the minimum vehicle speed will be respected by external programs.
    - Re-organized the ADS-B alert configuration for sake of clarity.
    - The ADS-B message file is now cleared on start-up to prevent Assassin from needing to parse the entire file to remove old entries individually.
    - Fixed an issue that could cause Assassin to crash when parsing aircraft messages.
        - When an invalid ADS-B message was encountered, a fatal error would occur.
    - Aircraft threats are now sorted by highest to lowest threat level, then closest to furthest distance.
    - Moved the ADS-B message pruning process to a separate thread for sake of efficiency.
- Assassin can now be configured to display "status messages", which fall between the normal output and the debugging output, in terms of verbosity.
- Added `--headless` command line argument for external interfaces to disable user interaction elements of the console output.
- File-saving debug messages are now only displayed when the "silence" flag is set to `false`.
- Added support for "calculated" GPS speed, where the speed is determined based on the most recent two GPS locations, rather than the speed provided by the hardware.
- Added process timing for helping users experienced improve speed.
