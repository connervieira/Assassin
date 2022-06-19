# Assassin

**Copyright 2022 V0LT - Conner Vieira**

A driving assistant designed to detect and mitigate threats while driving.


## Note

Assassin is currently a work in progress, so consider the descriptions and features below to be a preview of what's planned. Everything is subject to change.


## Disclaimer

While Assassin is designed to be as safe as possible, it's always the driver's responsibility to drive safely and attentively. Do not use Assassin in a context where you could be distracted from the road, and do not use Assassin as a replacement for your own attention.


## Description

Assassin is a system designed to be your driving copilot by detecting and mitigating potential hazards like speed cameras, potholes, and more. During normal driving, Assassin works in the background as a dashboard, displaying basic, customizable information on screen. However, when a potential hazard or threat is encountered, Assassin alerts the driver, and suggests a solution to mitigate the problem.


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
    - For diagnostic purposes, Assasin can display the number of satellites that the GPS is currently connected to.

### Telemetry Logging

Assassin is capable of logging various pieces of information to a local file, including speed, location, altitude, heading, and more. This file is completely private, but can be used by the owner of the system to look back at historical data at a later time.

### Traffic Enforcement Camera Alerts

Assassin can process and alert to nearby speed enforcement and red light cameras as the user drives, and even check the vehicle's current speed against the speed limit associated with nearby cameras.

### Automated License Plate Recognition Camera Alerts

Assassin can use a bundled database to detect nearby ALPR cameras, and alert the user before crossing the threshold.

### Status Lighting

Assassin can interface with WLED status lighting systems to provide immersive, attention grabbing alerts while driving.

### Audio Alerts

Assassin comes bundled with various audio alert terms that are seamless and pleasant while still being distinctive and recognizable.


## Philosophy

These are some of the attributes that Assassin is designed around.

### Lightweight

Assassin is extremely lightweight and power efficient, and is designed to work on a Raspberry Pi or similar low-powered device.

### Offline

Assassin is capable of operating entirely offline, meaning it can go anywhere your car does regardless of network connectivity.

### Repairable

Assassin follows a philosophy of repairability by providing the user with everything they need to diagnose and resolve problems independently.

### Open Source

Assasin is free and open source from top to bottom, and is 'free software', meaning you can make changes and distribute them to others freely.

### Generic

By design, Assassin doesn't require specialized hardware to run. Regardless of whether you use inexpensive hardware to save money, or a high end system to improve performance, Assassin will make the most of what it has to work with.

### Easy

While being technically mindedly will certainly help, Assassin doesn't require professional installation or setup to function. As long as you're reasonably experienced with the Linux command line and automotive electronics, installing assassin should only take a few hours at most.

### Private

Since Assassin is open source, self hosted, offline, and self contained, you can rest assured that it's completely private, and it doesn't collect any of the information you provide it.

### Customizable

Assassin is extremely customizable, making it easy to fit into your driving style and needs.

### Mobile

Assassin is designed to support low-energy-usage hardware such that it can be easily installed in a vehicle. A single USB port is enough to power an entire Assassin system.

### Safe

Assassin is designed to be safe, regardless of the installation context. It's easy to configure Assassin to completely hands free, ensuring that you don't have to look away from the road.

### Documented

Assasin's extreme customizability can be a bit overwhelming to new users. For this reason, the entire platform is extensively documented, and comes bundled with step-by-step guides on how to download it, install it, configure it, and run it.
