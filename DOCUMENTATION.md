# Documentation

This document contains the information you need to know to set up and use Assassin.


## Introduction

Due to it's inherently customizable and open-ended philosophy, there isn't a single concrete way to set up Assassin. As such, the documentation here may appear to be convoluted and complicated. This is simply to ensure that every environment and use-case is addressed. If these instructions are followed step-by-step, Assassin should operate smoothly and be configured to fit your usage situation.

It's also worth clarifying that Assassin is designed to be installed on dedicated hardware in a vehicle, often a low-power single-board computer. Assassin and all of its dependencies should be installed on this dedicated hardware.


## Platforms

It's important to make a quick note about platform compatability. While Assassin can be run on several platforms, it's level of compatability varies significantly. The only officially supported platform is Linux, specifically Debian based distributions. However, other platforms may be partially compatible. To learn more, see the [COMPATABILITY.md](COMPATABILITY.md) document.


## Quick Start

This section contains a quick-start guide if you want to set up Assassin as quickly as possible on a Debian based Linux distribution. This skips optional steps, and is designed to get a basic install of Assassin quickly. It's highly recommended that you follow the full instructions below. If you've installed Assassin before, and just need a quick shortcut to a working installation, follow these steps.

1. Install Python3
    - `sudo apt-get install python3 python3-pip`
2. Install `numpy`
    - `pip3 install numpy`
3. Install GPSD
    - `sudo apt-get install gpsd gpsd-clients; pip3 install gps gpsd-py3`
4. Download Assassin
5. Configure Assassin
6. Run Assassin


## Installation

This is the installation process for Assassin and all of it's dependencies. This process is written assuming you're running a Debian based distribution of GNU/Linux, but it's theoretically possible to get Assassin to function smoothly on any Linux distribution.

1. Install Python3.
    - If your system does not already have Python3, download and install it.
    - You can install Python3 on a Debian based Linux machine using the following command: `sudo apt-get install python3 python3-pip`
2. Install required Python packages.
    - Assasin requires the following Python libraries: `numpy`
    - These libraries can be installed with this command: `pip3 install numpy`
3. Install a GPS location provider (Highly Recommended).
    - Assassin requires a GPS connection for most of it's functionality.
    - To get GPS information, you'll need to install a GPS location provider.
    - Assassin is currently compatible with three GPS providers.
        - GPSD: Linux and BSD users
            - GPSD is a very common GPS library compatible with a wide gamut of GPS devices.
            - You can install GPSD using this command on a Debian based Linux machine: `sudo apt-get install gpsd gpsd-clients`
            - You can install GPSD's Python libraries using this command on a Debian based Linux machine: `pip3 install gps gpsd-py3 gpsd`
            - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
        - Termux-API: Android users
            - `termux-location` is a GPS location provider that comes as part of the `termux-api` for Termux on Android.
            - You can install `termux-location` on Android from Termux using this command: `pkg install termux-api`
        - LocateMe: MacOS users
            - LocateMe is a public domain program for MacOS used to access location information.
            - It can be installed using the Homebrew package manager using the following command: `brew install locateme`
            - Ideally, you should install GPSD to enable support for additional external GPS devices. However, LocateMe works well in a pinch.
4. Optionally, install networking packages (Recommended).
    - `pip3 install validators requests`
    - If you planning on using any of Assassin's networking features (like status lighting interfacing), then you'll need to install networking libraries.
5. Optionally, install an audio provider (Recommended).
    - Assassin requires an audio provider in order to play audio effects for alerts.
    - There are currently two compatible options.
        - `MPG321` is a command line audio provider. It can be installed on a Debian based Linux machine with the following command: `sudo apt-get install mpg321`
        - `playsound` is a Python library used to play audio files. It can be installed with the following command: `pip3 install playsound`
    - If you don't install an audio provider, Assassin will encounter errors when audio alerts are enabled in the configuration.
    - If you don't intend on using Assassin's audio features, this is step is optional.
6. Optionally, install text-to-speech (Recommended).
    - Assassin is capable of using PyTTSx3 to announce text-to-speech alerts.
    - PyTTSx3 can be installed using the following command: `pip3 install pyttsx3`
    - If you don't plan on using Assassin's text-to-speech functionality, this step is optional.
5. Optionally, install AirCrackNG (Recommended).
    - To use the drone alerting features of Assassin, `aircrack-ng` will need to be installed. AirCrack should come packaged with `airomon-ng` and `airodump-ng`.
    - You can install AirCrack using this command on a Debian based Linux machine: `sudo apt-get install aircrack-ng`
    - If you don't plan on using Assassin's radio threat detection features, this step is optional.
6. Optionally, install Bluez Tools (Recommended).
    - Bluez Tools is required to manipulate and process Bluetooth data. If you don't install it, features that require Bluetooth will be disabled.
    - You can install Bluez Tools using this command on a Debian based Linux machine: `sudo apt-get install bluez-tools; pip3 install PyBluez`
        - If you encounter issues, you may need to downgrade 'setuptools' using the following command: `pip3 install setuptools==57.5.0`
    - If you don't plan on using Assassin's Bluetooth threat features, this step is optional.
7. Optionally, install Dump1090 (Recommended).
    - Dump1090 is required for Assassin to be able to interface with ADS-B receivers in order to detect planes.
    - You can install Dump1090 using this command on a Debian based Linux machine: `sudo apt install dump1090-mutability`
    - Assassin needs the ability to execute the Dump1090 command as root with passwordless authentication.
        - To grant these permissions, authenticate as root with the command `sudo su`, then execute this command, replacing `[username]` with the username you will be running Assassin as: `echo "[username] ALL=(ALL) NOPASSWD: /usr/bin/dump1090-mutability" >> /etc/sudoers`
    - If you don't plan on using Assassin's aircraft detection features, this step is optional.
8. Optionally, install a graphical interface.
    - Assassin is capable of being used fully from the command line. However, you may find it useful to install a graphical interface like [Marksman](https://v0lttech.com/marksman.php).
9. Download Assassin.
    - Download Assassin from wherever you received it, and extract it to somewhere on your filesystem. The Assassin folder can be placed anywhere with appropriate permissions, but don't place any external files in the Assassin root directory to prevent conflicts.


## Configuration

After installing Assassin, you should do some quick configuration in order to get the most out of it.

1. Open the Assassin configuration
    - Open the `config.json` file in the Assassin root directory using your text editor of choice.
2. Make configuration changes
    - All configuration values are explained extensively in the [CONFIGURATION.md](CONFIGURATION.md) document.
    - Make changes to any of the configuration values to better fit your usage context.
    - This step is very open-ended. Depending on your situation, you may leave the configuration almost untouched, while other situations might involve intensive changes.
3. Depending on the platform, Assassin might not be able to locate the `config.json` file. If you encounter issues during the steps described in the "Usage" section, you may need to manually set Assassin's directory. Under normal circumstances, this shouldn't be necessary.
    - At the top of the `main.py`, `utils.py`, and other scripts, you should see a variable titled `assassin_root_directory`. By default, a Python function is used to find the current directory of the script.
    - If you receive errors related to missing configuration files when trying to run Assassin, try setting this variable to a static file path.
    - Example:
        - `assassin_root_directory = "/home/user/Assassin/"`


## Hardware

Many of Assassin's features are dependent on external hardware. This section provides basic information on feature-specific hardware.

- Processor
    - Assassin is specific designed to be extremely lightweight, so it should run smoothly on low-power computers.
    - Since Assassin is capable of interfacing with several external devices and sensors at once, a processing device with reliable I/O is recommended.
- Location Services
    - Many of Assassin's core features are dependent on GPS data. As such, it is highly recommend that you install a GPS unit to make the most of Assassin.
    - Assassin uses GPSD as a location back-end, which means practically any generic USB GPS will work with Assassin. Simply locate a GPS that is compatible with GPSD, and connect it to your central Assassin device.
- Bluetooth Monitoring
    - To enable Bluetooth related features, Assassin simply connects to any typical Bluetooth adapter. Many devices have these adapters built in.
    - If your device has integrated Bluetooth, Assassin should have no problem interfacing it. However, external Bluetooth adapters can increase range especially if they are placed outside the body of the vehicle.
- Radio Monitoring
    - Assassin's radio monitoring features allow it to detect WiFi devices, consumer/commercial drones, and other wireless threats.
    - Assassin uses Airodump to detect wireless devices. Airodump is capable of using most consumer network adapters.
        - Practically all consumer devices operate on either 2.4GHz or 5.0GHz
        - Certain drones operate on 5.8GHz
    - If your device has a built in wireless adapter, it's highly likely that Airodump can use it. However, external wireless receivers can increase range, especially if they're placed outside the body of the vehicle.
- Plane Detection
    - Assassin makes use of ADS-B technology in order to detect planes and collect information from them.
    - In order to enable plane detection functionality, you'll need to connect Assassin to an ADS-B receiver.
    - To build a basic ADS-B system, you'll need a USB 1090MHz tuner, a 1090MHz antenna, and software to interpret data from the tuner.
        - Nearly all tuners will work with Assassin. Any standardized tuner that works with dump1090 should work fine.
            - Generally speaking, less expensive tuners will work just fine for Assassin's purposes. More expensive tuners allow for increased detection range, but even low-end tuners can easily detect planes from 50+ miles away, far beyond the point of visibility.
        - Any 1090MHz antenna that connects appropriately to your tuner should work just fine with Assassin.
            - It's highly recommended that you get an externally mounted antenna. Antennas located within the body of the car will have dramatically reduced range.
        - Assassin uses the dump1090-mutability command line utility as its backend.
            - You should verify that Dump1090 can successfully connect to and interpret data from the tuner.


## Usage

After configuring Assassin, you can try it out for the first time!

1. Run Assassin
    - To run Assassin, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Assassin finishes loading, you should see a quick message displaying the "Assassin" name.
2. Use Assassin
    - Assassin runs on a cycle, where new information will be received, processed, and displayed at regular intervals. At this point, no user intervention is required.
    - See [USAGE.md](USAGE.md) for more information.
3. Quit Assassin
    - When you finish using Assassin, simply hold Ctrl + C to terminate the program.


## Debugging

After you get Assassin up and running, you may want to use some of the integrated debugging tools to find and fix issues, and improve the efficiency of your installation.

1. Enable debugging
    - Assassin's debugging mode can be used by enabling the `debugging_output` and `disable_console_clearing` configuration values.
2. Start Assassin
    - Start Assassin as normal.
3. Observe debugging messages
    - When the debugging configuration values are enabled, Assassin should print out frequent grayed out messages explaining what processes are currently running.
    - These messages follow this format:
        - `[current time] ([time since last message]) - [message]`
        - Example: `1664770806.6115972996 (0.0029230118) - Importing 'math' library`
4. Locate sources of errors
    - If you happen to encounter errors, the debugging messages can be a valuable tool in the process of finding the source.
    - Look at the last few messages before the error occurs. This can show what process was being completed when the error occurred.
    - Once you've located the process that triggered the error, you can focus your search for solutions on that particular process.
5. Locate sources of delay
    - The 'time since last message' field can be used to quickly determine how long the previous processing message took to complete. This is useful for locating sources of delay.
    - Once you've located sources of delay, consider disabling functions you don't need. Assassin is designed to avoid unnecessary processing, and will skip processes that aren't required to complete the functions enabled in the configuration.
        - For example, if you don't see yourself using traffic enforcement camera alerts, setting the `alert_range` configuration value for `traffic_cameras` to `0` will cause Assassin to skip loading the traffic camera database entirely to save processing time.
    - In the following example, the process of opening the traffic camera database was a source of significant delay, as indicated by the (3.5831029) in the second line. This tells that the process of opening the traffic camera data in the previous line took 3.58 seconds.
        - `1664771344.831 (0.0000543) - Opening traffic enforcement camera database`
        - `1664771348.414 (3.5831029) - Loading traffic enforcement cameras from database`
        - `1664771349.143 (0.7282614) - Loaded traffic enforcement camera database`
