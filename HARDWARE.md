# Hardware

Many of Assassin's features are dependent on external hardware. This document provides basic information on feature-specific hardware.


## Introduction

### Disclaimer

This document gives hardware recommendations to make building an Assassin system as easy as possible. However, V0LT makes no guarantees regarding the reliability or compatibility or the specific devices listed. These products and manufacturers are not associated with V0LT. You should only purchase hardware from manufacturers you are familiar with in order to avoid unexpected issues.

### Note

It's important to clarify what Assassin is actually designed for, to avoid confusion during the setup process. Assassin is intended to be installed on dedicated hardware in a vehicle. This hardware, at its core, is just a Linux processing device. Other hardware is connected to this processing device to enable additional features. Assassin is very modular, so you might not need all of the hardware described on this page, depending on the features you want to use.


## Recommendations

### Processor

- At it's core, Assassin runs on a processing device, typically a low-power, Linux based, single-board computer (SBC).
- While a faster processing device will increase performance, most installations will work great with just an affordable processing device.
- Below are some common processing devices used in Assassin installations:
    - [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)
    - [LibreComputer AML-S905X-CC](https://libre.computer/products/aml-s905x-cc/)
    - [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
    - [Orange Pi 5](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5.html)

### GPS

- Nearly all of Assassin's core features are dependent on GPS data. As such, it is highly recommend that you install a GPS unit to make the most of Assassin.
- Assassin primarily uses GPSD as a location back-end, which means practically any generic USB GPS will work with Assassin. Simply locate a GPS that is compatible with GPSD, and connect it to your central Assassin device.
    - Provided you have GPSD installed and setup on your processing device, the USB GPS should be automatically recognized.
    - You can test your GPS with the `cgps` command.

### ADS-B

- Assassin makes use of ADS-B technology in order to detect aircraft and collect information from them.
- In order to enable plane detection functionality, you'll need to connect Assassin to an ADS-B receiver.
- To build a basic ADS-B system, you'll need a USB 1090MHz tuner, a 1090MHz antenna, and software to interpret data from the tuner.
    - Nearly all tuners will work with Assassin. Any standardized tuner that works with `dump1090` should work fine.
        - Below are some common ADS-B tuners used in Assassin installations:
            - [AirNav RadarBox FlightStick 1090](https://www.radarbox.com/flightstick1090)
    - Any 1090MHz antenna that connects appropriately to your tuner should work just fine with Assassin.
        - It's highly recommended that you get an externally mounted antenna. Antennas located within the body of the car will have dramatically reduced range.
    - Assassin uses the dump1090-mutability command line utility as its backend.
        - You should verify that Dump1090 can successfully connect to and interpret data from the tuner.

### Bluetooth

- To enable Bluetooth related features, Assassin simply connects to any typical Bluetooth adapter. Many devices have these adapters built in.
- If your device has integrated Bluetooth, Assassin should have no problem interfacing it. However, external Bluetooth adapters can increase range especially if they are placed outside the body of the vehicle.

### WiFi

- Assassin's radio monitoring features allow it to detect WiFi devices, consumer/commercial drones, and other wireless threats.
- Assassin uses Airodump to detect wireless devices. Airodump is capable of using most consumer network adapters.
    - Practically all consumer devices operate on either 2.4GHz or 5.0GHz
    - Certain drones operate on 5.8GHz
- If your device has a built in wireless adapter, it's possible that Airodump can use it. However, external wireless receivers can increase range, especially if they're placed outside the body of the vehicle.

