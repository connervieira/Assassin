# Assassin

**Copyright 2024 V0LT - Conner Vieira**

The ultimate defense system for driving the technological world.


## Disclaimer

While Assassin is designed to be as safe as possible, it's always the driver's responsibility to drive safely and attentively. Do not use Assassin in a context where you could be distracted from the road, and do not use Assassin as a replacement for your own attention.

In most regions, Assassin is completely legal to possess and use. However, some areas might place legal restrictions on certain features, like traffic camera alerting, or certain devices, like radio receivers and transmitters.

Additionally, Assassin should not be relied upon for safety critical tasks. For example, if you suspect someone may be attempting to track you, you absolutely should not rely entirely on Assassin's Bluetooth tracker detection. While Assassin is intended to be as reliable, it is far from infallible.


## Description

Assassin is designed to be the ultimate copilot for driving in the digital world. At a basic level, Assassin operates like an extension of your dashboard, showing information like your speed, position, altitude, and other relevant information. However, it goes far beyond a typical information display. Assassin is a highly customizable platform for building the ultimate digital defense system. As you drive, Assassin interfaces with different sensors and devices to constantly attempt to detect and mitigate a plethora of modern threats to safety, security, and privacy.


### Telemetry Logging

Assassin is capable of logging information from various sources to a local file, including speed, location, altitude, heading, nearby radio signals (Bluetooth beacons, WiFi devices, consumer/commercial drones, etc.), and much more. This file is completely private, but can be used by the owner of the system to look back at historical data at a later time. This feature is completely optional and configurable.


### ALPR Defense

Assassin comes bundled with a database to detect nearby ALPR cameras, and alert the user before crossing the reading threshold. Assassin will determine the distance and direction to nearby ALPR cameras in real-time, and assign them a threat severity level. Assassin also comes bundled with tools to convert information from existing sources, like OpenStreetMap to further extend coverage.


### Autonomous Threat Defense

Assassin can interface with 2.4GHz, 5GHz, and 5.8GHz receivers in order to detect, record, and alert to nearby consumer and commercial drones. This feature makes use of an open, customizable database of wireless threats in order to quickly and effectively detect and alert to nearby autonomous hazards. While not its primary purpose, this feature is also theoretically capable of detecting various other radio-based devices, including remote-operated speed cameras from several common manufacturers.


### Traffic Enforcement Camera Defense

Assassin can process and alert to nearby speed enforcement and red light cameras as the user drives, and even check the vehicle's current speed against the speed limit associated with nearby cameras. If the vehicle speed exceeds a customizable offset relative to the speed camera's limit, Assassin will issue an alert.


### ADS-B Aircraft Detection

Assassin can interface with ADS-B receivers in order to independently detect nearby aircraft, and collect data like location, altitude, speed, heading, flight number, squawk code, and more. This feature doesn't depend on the internet or any other external services, and is entirely self contained and undetectable.


### GPS Spoof Detection

Assassin can detect potential GPS spoofing attempts by monitoring location history, and notifying the user of any unexplainable changes in position data.


### Weather Alerts

When connected to the internet, Assassin can fetch weather information at a regular interval, and display alerts when customizable criteria are met.


### Attention Monitoring

Assassin can monitor the time spend actively driving, and optionally display an alert when a threshold has been broken, and prompt the driver to take a break.


### Bluetooth Threat Defense

Assassin can interface with Bluetooth adapters to provide Bluetooth Low-Energy monitoring, and can display an alert when a particular Bluetooth device has been following for a suspiciously long time. This can help provide early warning of people tailing you as you drive, as well as aiding in the location of concealed tracking devices hidden in your car. This feature can also be configured to ignore certain devices (like your phone or car stereo) or instantly alert to specific devices that could be an imminent threat (like the phone of a previous security concern).



### Predator Integration

Assassin can integrate with [V0LT Predator](https://v0lttech.com/predator.php) to provide license plate recognition alerts. Assassin can automatically start Predator, and display alerts if Predator detects a license plate in a hot-list.



## Features

These are some of the key features of Assassin.

### Information Displays

- Speed display
    - Assassin can show the current speed with both a small, single-line text output, and/or a large ASCII font that's extremely easy to read at a glance.
    - Speeds can be displayed in miles per hour, kilometers per hour, meters per second, feet per second, or knots.
- Location display
    - The current GPS location can be displayed as coordinates on-screen, allowing the driver to quickly determine their exact location.
- Heading display
    - The current direction of travel can be displayed as both a number in degrees, and/or as a cardinal direction.
- Altitude display
    - The current altitude in meters can be displayed based on data derived from the GPS.
- Satellite display
    - For diagnostic purposes, Assassin can display the number of satellites that the GPS is currently connected to.

### Status Lighting

Assassin can interface with RGB lights via WLED to provide immersive and attention grabbing alerts while driving. When configured as such, these status light alerts allow Assassin to sit in the background, and issue important to the driver in a clean, integrated, OEM-like manner.

### Audio Alerts

Assassin comes bundled with various audio alert terms that are seamless and pleasant while still being distinctive and recognizable.


## Philosophy

These are some of the attributes that Assassin is designed around.

### Integrated

When installed properly, Assassin should feel like just another part of your car, working in the background to protect you from a wide gamut of potential threats.

### Lightweight

Assassin is extremely lightweight and power efficient, and is designed to work on a Raspberry Pi or similar low-powered device.

### Offline

Assassin is capable of operating entirely offline, meaning it can go anywhere your car does, regardless of network connectivity.

### Repairable

Assassin follows a philosophy of repairability by providing the user with everything they need to diagnose and resolve problems independently.

### Open Source

Assassin is free and open source from top to bottom, and is 'free software', meaning you can make changes and distribute them to others freely.

### Generic

By design, Assassin doesn't require specialized hardware to run. Regardless of whether you use inexpensive hardware to save money, or a high end system to improve performance, Assassin will make the most of what it has to work with.

### Easy

While being technically minded will certainly help, Assassin doesn't require professional installation or setup to function. As long as you're reasonably experienced with the Linux command line and automotive electronics, installing a complete Assassin system should only take a few hours at most.

### Private

Since Assassin is open source, self hosted, offline, and self contained, you can rest assured that it's completely private, and it doesn't collect any of the information you provide it.

### Customizable

Assassin is extremely customizable, making it easy to fit into your driving style and needs.

### Mobile

Assassin is designed to support low-energy-usage hardware such that it can be easily installed in a vehicle. A single USB port is enough to power an entire Assassin system.

### Safe

Assassin is designed to be safe, regardless of the installation context. It's easy to configure Assassin to completely hands free, ensuring that you don't have to look away from the road.

### Documented

Assassin's extreme customizability can be a bit overwhelming to new users. For this reason, the entire platform is extensively documented, and comes bundled with step-by-step guides on how to download it, install it, configure it, and run it.

### Modular

Assassin is designed to be as modular as possible. This makes it customizable, fault tolerant, and easy to modify.

### Filtered

Given the high volume of information processed by Assassin, it's common for dozens of alerts to be processed at once. Assassin comes with complex, customizable filtering to reduce annoying false alerts.


## Installing

Due to it's customizable nature, Assassin has extensive configuration and setup options. To learn more about how to install, configure, and use Assassin, see [DOCUMENTATION.md](DOCUMENTATION.md)
