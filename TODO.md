# To Do

This is a informal to-do list for Assassin. This is not a complete changelog, nor is it an official declaration of upcoming features. This list is subject to change.

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
    - [ ] Add weather alerts.
    - [ ] Add speed trap alerts.


### Hypothetical

Tasks in this section are purely hypothetical, and may not ever be finished.

- [ ] Add crowd sourced alerts.
- [ ] Add the ability to activate GPIO pins on alerts.
- [ ] Add the ability to import custom GPS alert databases.
- [ ] Add more extensive vehicle integration using OBD-II.
- [ ] Add integration for radar detectors.
- [ ] Add optical motion detection using a webcam.
