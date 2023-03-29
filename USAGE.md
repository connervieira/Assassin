# Usage

This document explains how to effectively use Assassin.


## Introduction

Assassin is a very complex platform, designed to integrate multiple features and devices into a single system. Naturally, this means it may not be immediately apparent how to effectivelyt use it. This document contains tips, tricks, and explanations on how to effectively use Assassin.


## Interface

### Information Display

The information display is shown at the top of the Assassin interface, and contains information about the current location, speed, direction, and more. The information shown here can be adjusted in the configuration.

### Alerts

Assassin uses 'alerts' to inform the user of important information. Below is a list of all the alerts Assassin is currently capable of displaying.

- Traffic enforcement camera alerts
    - Traffic enforcement camera alerts are triggered when proximity to a traffic enforcement camera is detected.
        - Traffic enforcement cameras include speed cameras, red light cameras, lane monitoring cameras, and more.
    - Assassin contains a database of traffic enforcement cameras, and be configured to alert with a camera is within a certain distance.
- ALPR alerts
    - ALPR alerts are triggered when proximity to an automated license plate recognition (ALPR) camera is detected.
    - Many cities and towns set up large networks of ALPR cameras to automatically monitor and record the behavior of all vehicles in a certain area.
    - Assassin contains a database of ALPR cameras, and can be configured to alert when certain proximity criteria are met.
- Aircraft alerts
    - Aircraft alerts are triggered when proximity to an aircraft matching certain criteria is detected.
    - Many law enforcement organizations use aircraft to issue traffic citations on remote, rural highways where ground enforcement may not be practical due to infrequent intersections, limited access, low traffic volume, or other reasons.
        - Like all other aircraft, these planes and helicopters are required to have ADS-B transmitters to share important safety information with other aircraft and air traffic controllers.
    - Assassin can interface with an ADS-B receiver to detect nearby aircraft, and alert to those that match criteria like speed, altitude, and distance.
- Drone/radio threat alerts
    - Autonomous alerts are triggered when radio traffic from a wireless hazard is detected.
    - Many commercially available drones, autonomous speed cameras, and other devices of interest operate on 2.4GHz, 5GHz, and 5.8GHz frequencies.
        - Nearly all consumer devices have a network card capable of operating on at least two of these frequencies.
    - Assassin can monitor radio traffic, and identify hazards using their hardware identifier.
- Attention monitoring
    - Assassin can monitor the time spent driving, and alert the driver when they've broken a threshold without stopping for a break.
    - Long, continuous sessions of driving can decrease awareness and increase reaction time.
- Weather alerts
    - Weather alerts are triggered when certain weather criteria are met.
    - This feature uses an internet-based weather information provider to alert the driver when potentially dangerous or important weather conditions are present.
- Bluetooth alerts
    - Bluetooth alerts are triggered when a Bluetooth device has been detected following for a certain distance.
    - This alert can be useful to detect Bluetooth trackers, or even to detect the precense of known bad devices using a blacklist.

### Colors

Assassin uses text coloring to make it quick and easy to identify information. Below is an explanation of each color's meaning.

- White
    - White text is used to indicate general information.
    - This is the color used to display the main information display.
- Gray
    - Gray text is used to indicate operational information, like debugging messages.
    - This color is rarely used during Assassin's typical operation.
- Green
    - Green text is used to indicate hardware alerts.
    - These alerts are generally related to sensors or devices installed in the car.
- Blue
    - Blue text is used to indicate law enforcement alerts.
    - Alerts like traffic enforcement cameras and suspicious aircraft will fall into this section.
- Purple
    - Purple text is used to display alerts concerning privacy.
    - Alerts like ALPR cameras and suspicious Bluetooth devices will be displayed in this color.
- Red
    - Red text is used to indicate immediately critical information.
    - High priority alerts and system errors will be displayed in this color.
    - While not necessarily part of this category, the Assassin start-up header will also be displayed in red.
- Yellow
    - Yellow text is used to indicate safety related alerts.
    - Alerts related to weather and driver attention will appear in this color.
    - While not necessarily part of the category, non-fatal system warnings will also be displayed in yellow.


## Audio

Assassin makes use of audio based notifications to reduce the need to look at the display while driving.

### Sound Effects

Assassin comes with individually configurable sound effects that are triggered when certain events occur. By default, these sounds are short, recognizable samples, but custom audio files can be used as well.

For more information on how to configure audio alerts, see [CONFIGURATION.md](CONFIGURATION.md).

### Text To Speech

Assassin can use text-to-speech to read out important information.

Unlike sound effects, text to speech samples are used infrequently to indicate new alerts. They do not repeatedly update alerts that have already been announced.
