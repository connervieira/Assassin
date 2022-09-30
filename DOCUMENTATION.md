# Documentation

This document contains the information you need to know to set up and use Assassin.


## Introduction

Due to it's inherently customizable and open-ended philosophy, there isn't a single concrete way to set up Assassin as such, the documentation here may appear to be convoluted and complicated. This is simply to ensure that every environment and use-case is addressed. If these instructions are followed step-by-step, Assassin should operate smoothly and be configured to fit your usage situation.


## Installation

This is the installation process for Assassin and all of it's dependencies. This process is written assuming you're running a Debian based distribution of GNU/Linux, but it's theoretically possible to get Assassin to function smoothly on any Linux distribution.

1. Install the required Python packages. (Required)
    - `pip3 install validators gps geopy gpsd-py3 gpsd requests pyproj`
2. Install GPSD (Highly Recommended)
    - GPSD is required for Assassin to communicate with GPS devices.
    - You can install GPSD using this command on a Debian based Linux machine: `sudo apt-get install gpsd gpsd-clients`
    - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
    - Without GPSD, Assassin would theoretically function, but in a severely limited capacity. Many of the core functions of Assasin would fail to operate.
3. Optionally, install MPG321 (Recommended)
    - Assassin requires MPG321 in order to play audio effects for alerts.
    - If you don't install MPG321, Assassin will encounter errors when audio alerts are enabled in the configuration.
    - You can install MPG321 using the following command on a Debian based Linux machine: `sudo apt-get install mpg321`
    - If you don't intend on using Assassin's audio features, this is step is optional.
4. Optionally, install AirCrackNG (Recommended)
    - To use the drone alerting features of Assassin, `aircrack-ng` will need to be installed. AirCrack should come packaged with `airomon-ng` and `airodump-ng`.
    - You can install AirCrack using this command on a Debian based Linux machine: `sudo apt-get install aircrack-ng`
    - If you don't plan on using Assassin's radio threat detection features, this step is optional.
5. Optionally, install Bluez Tools (Recomended)
    - Bluez Tools is required to manipulate and process Bluetooth data. If you don't install it, features that require Bluetooth will be disabled.
    - You can install Bluez Tools using this command on a Debian based Linux machine: `sudo apt-get install bluez-tools; pip3 install PyBluez`
        - If you encounter issues, you may need to downgrade 'setuptools' using the following command: `pip3 install setuptools==57.5.0`
    - If you don't plan on using Assassin's Bluetooth threat features, this step is optional.
6. Optionally, install Dump1090 (Recommended)
    - Dump1090 is required for Assassin to be able to interface with ADS-B receivers in order to detect planes.
    - You can install Dump1090 using this command on a Debian based Linux machine: `sudo apt install dump1090-mutability`
    - If you don't plan on using Assassin's aircraft detection features, this step is optional.
7. Optionally, install RaspAP
    - If you're installing Assassin on a Raspberry Pi, you may find it useful to install a program like [RaspAP](https://github.com/RaspAP/raspap-webgui) (or similar program) in order to remotely manage your Assassin instance, and eliminate the need for a full keyboard and display.
    - Assassin works entirely via command line, meaning any set up that enables SSH access to the host will allow for remote management of Assassin.
    - If you already have an access point installed in the same area as Assassin, you can simply connect Assassin to it, and use SSH on a separate device to access the instance remotely.
8. Download Assassin
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
    - At the top of the `main.py` and `utils.py` scripts, you should see a variable titled `assassin_root_directory`. By default, a Python function is used to find the current directory of the script.
    - If you receive errors related to missing configuration files when trying to run Assassin, try setting this variable to a static file path.
    - Example:
        - `assassin_root_directory = "/home/user/Assassin/"`


## Hardware

Many of Assassin's features are dependent on external hardware. This section provides basic information on feature-specific hardware.

- Location Services
    - Many of Assassin's core features are dependent on GPS data. As such, it is highly recommend that you install a GPS unit to make the most of Assassin.
    - Assassin uses GPSD as a location backend, which means practically any USB GPS will work with Assassin. Simply locate a GPS that is compatible with GPSD, and connect it to your central Assassin device.
- Bluetooth Monitoring
    - To enable Bluetooth related features, Assassin simply connects to any typical Bluetooth adapter. Many devices have these adapters built in.
    - If you're device has integrated Bluetooth, Assassin whould have no problem interfacing it. However, external Bluetooth adapters can increase range.
- Radio Monitoring
    - Assassin's radio monitoring features allow it to detect WiFi devices, consumer/commercial drones, and other wireless threats.
    - Assassin uses Airodump to detect wireless devices. Airodump is capable of using most consumer network adapters.
        - Practically all consumer devices operate on either 2.4GHz or 5.0GHz
        - Certain drones operate on 5.8GHz
    - If your device has a built in wireless adapter, it's highly likely that Assassin can use it. However, external wireless receivers can increase range, especially if they're placed outside the body of the vehicle.


## Usage

After configuring Assassin, you can try it out for the first time!

1. Run Assassin
    - To run Assassin, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Assassin finishes loading, you should see a quick message displaying the "Assassin" name.
2. Use Assassin
    - Assassin runs on a cycle, where new information will be received, processed, and displayed at regular intervals. At this point, no user intervention is required.
3. Quit Assassin
    - When you finish using Assassin, simply press Ctrl + C to terminate the program.
