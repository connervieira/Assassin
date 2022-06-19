# Documentation

This document contains the information you need to know to set up and use Assassin.


## Installation

This is the installation process for Assassin and all of it's dependencies. This process is written assuming you're running a Debian based distribution of GNU/Linux, but it's theoretically possible to get Assassin to function on MacOS as well.

1. Install the required Python packages.
    - `pip3 install validators gps geopy gpsd-py3 gpsd requests`
2. Install GPSD
    - GPSD is required for Assassin to communicate with GPS devices.
    - You can install GPSD using this command on a Debian based Linux machine: `sudo apt-get install gpsd gpsd-clients`
    - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
3. Optionally, install MPG321 (Recommended)
    - Assassin requires MPG321 in order to play audio effects for alerts.
    - If you don't install MPG321, Assassin will encounter errors when audio alerts are enabled in the configuration.
    - You can install MPG321 using the following command on a Debian based Linux machine: `sudo apt-get install mpg321`
4. Optionally, install AirCrackNG
    - To use the drone alerting features of Assassin, `aircrack-ng` will need to be installed. AirCrack should come packaged with `airomon-ng` and `airodump-ng`.
    - You can install AirCrack using this command on a Debian based Linux machine: `sudo apt-get install aircrack-ng`
5. Optionally, install RaspAP
    - If you're installing Assassin on a Raspberry Pi, you may find it useful to install a program like [RaspAP](https://github.com/RaspAP/raspap-webgui) (or similar program) in order to remotely manage your Assassin instance, and eliminate the need for a full keyboard and display.
    - Assassin works entirely via command line, meaning any set up that enables SSH access to the host will allow for remote management of Assassin.
    - If you already have an access point installed in the same area as Assassin, you can simply connect Assassin to it, and use SSH on a separate device to access the instance remotely.
6. Download Assassin
    - Download Assassin from wherever you received it, and extract it to somewhere on your filesystem. The Assassin folder can be placed anywhere with appropriate permissions, but don't place any external files in the Assassin root directory to prevent any conflicts.


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
