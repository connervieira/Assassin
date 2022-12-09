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
    - ALPR alerts now have their own section.
- Updated ALPR alerting.
    - ALPR alerts will now show the number of ALPR cameras within range, in addition to the nearest alert.
    - Added ALPR alert filtering.
        - Alerts can be filtered by direction.
            - This prevents cameras that are behind or to the side from triggering alerts.
        - Alerts can be filtered by angle.
            - This prevents from ALPR cameras from triggering alerts when they are at an angle that can't read the license plate of the car.
- [ ] Finished GPIO relay alerting.
