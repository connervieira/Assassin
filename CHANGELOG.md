# Changelog

This document contains a list of all the changes for each version of Assassin.


## Version 0.9

### Initial release

October 30th, 2022

- Core functionality
    - Information dashboard
    - Traffic enforcement camera alerting
    - ALPR camera alerting
    - Drone/autonomous threat detection
    - Bluetooth threat detection
    - ADS-B aircraft detection


## Version 1.0

### First stable release

*To be determined*

- Added several tools.
    - Added database preview tool.
    - Added database verify tool.
- Added several new ALPR cameras to the database.
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
- [ ] Finished GPIO relay alerting.
