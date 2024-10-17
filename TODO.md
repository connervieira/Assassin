# To Do

This is a informal to-do list for Assassin. This is not a complete change-log, nor is it an official declaration of upcoming features. This list is subject to change.

### Planned

Tasks in this section are actively planned, and are likely to be completed some time in the near future.

- Version 1.0
    - [X] Add configuration options for how warning messages are displayed.
    - [X] Add wireless access point logging.
    - [X] Fix drone hazard logging.
    - [X] Add ADS-B monitoring to detect planes.
        - [X] Complete ADS-B data processing.
        - [X] Complete alert processing.
        - [X] Add message time-to-live support.
        - [X] Complete ADS-B data streaming.
        - [X] Refine alerting sensitivity.
            - [X] Add max aircraft height threshold.
            - [X] Add minimum vehicle speed threshold.
            - [X] Add minimum aircraft speed threshold.
            - [X] Add threat confidence level.
    - [X] Improve efficiency by removing unnecessary plugin loading.
    - [X] Revise Bluetooth alerts.
        - [X] Add a Bluetooth blacklist, for which Assassin will instantly alert instead of waiting for devices to follow.
        - [X] Remove Bluetooth alert GPS dependency.
    - [X] Finish alert sounds.
        - [X] Add Bluetooth alert sound.
        - [X] Add ADS-B alert sound.
        - [X] Normalize all sounds.
    - [X] Add `information_displayed` to CONFIGURE.md.
    - [X] Add text-to-speech support.
    - [X] Add customizable file name to telemetry logging.
- Version 2.0
    - [X] Add weather alerts.
    - [X] Add GPS spoofing detection.
    - [X] Add driving attention timer.
- Version 3.0
    - [X] Improve ADS-B data intake process.
    - [X] Solve run-away ADS-B message file size.
    - [X] Improve drone detection process.
    - [X] Improve Bluetooth scanning process.
    - [X] Refine GPS alert processing.
- Version 4.0
    - [ ] Add Predator integration.
        - [X] Add alert handling.
        - [X] Add configuration validation for new configuration values.
        - [X] Add Predator start/stop capability.
        - [X] Test functionality.
        - [ ] Add alert name display.
    - [ ] Add alert sounds.
        - [ ] Add Predator alert sound.
        - [ ] Add attention monitoring alert sound.
    - [X] Add notification when no ADS-B messages are being received.


### Hypothetical

Tasks in this section are purely hypothetical, and may not ever be finished.

- [ ] Add crowd sourced alerts.
- [ ] Add integration for radar detectors.
- [ ] Add the ability to identify aircraft that are circling.
- [ ] Add the ability to activate GPIO pins on alerts.
- [ ] Add the ability to import custom GPS alert databases.
