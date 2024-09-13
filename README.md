# Raspberry Pi NFC Reader and availability sign

NFC Reader with LCD Display API receiver. 

![LCD Panel](./images/lcd_panel.png)
![NFC Reader top](./images/nfc_reader_top.png)
![NFC Reader side](./images/nfc_reader_side.png)

## Overview

I designed an NFC reader with LCD Display API receiver in order to indicate when I was available or not. It's essentially an over-engineered "Do Not Disturb" digital sign, with the LCD Display intended to be glued to a door and the NFC reader to be placed by the side of my desk. 

**This guide is partially complete. I only completed it post setup and printing, meaning that the assembly section is partially complete. However, the structure is quite self-explanatory and you should be able to assemble the pieces together by yourself.**

## Resources

- PLA 
- Hot glue
- A Rpi FAN and 4 screws
- 1 Raspberry Pi Zero (with SD card)
- 1 Raspberry Pi 2B (with SD card)
- An NFC Hat
- 3 LEDS: white, red and green
- 3 resistors for each LED
- a 5x7 cm PCB
- Wires
- 1 I2C 128x64 OLED Display
- 2 power cable for the Raspberry Pis
- 1 I2C Enabled LCD Screen

### 3D prints

The parts were printed using a Creality CR-20 pro.

For the LCD Display case the pieces are as follows:
- A base
- a lid/cover

For the NFC case the pieces are as follows:

- a base
- a lid/cover

All the parts are available in the `3d` folder. 

My slicer settings were as follows:

Infill: 10%
Infill pattern: Gyroid
Support: Touching build plate
Support pattern: lines
Nozzle size: 0.4mm
Nozzle temp: 210 degrees
Bed temp: 60 degrees
Print speed: 80 mm/s
Infill speed" 40 mm/s
Travel speed 200 mm/s
Initial layer speed: 20 mm/s
Support: everywhere at 80 degrees angle

### Assembly and wiring

I completed this guide post-assembly and therefore this part is partially complete. 

#### NFC Case
You can refer to [this repository](https://github.com/AN63L/rpi_oled_display_stats) for the wiring of the LCD display on the NFC case. 

The wiring for the circuit board is as follows: 
GPIO 27 -> WHITE
GPIO 25 -> GREEN
GPIO 22 -> RED

#### LCD Display

Connect the fan to the ground and 5V power supply of the RPI. 

You can refer to [this guide](https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/) to the connect the I2C LCD screen. 

### Software

**This entire setup runs on your local network, there are no outside network calls.**

The overall of architecture of this setup is as follows: 
- The Display runs a REST API with the FAST API framework that awaits for calls from the NFC reader. 
- The NFC reader process the tags and if it is valid, it will send a call to the API. Additionally, it processes the current status of the LCD display. 

#### LCD Display

The API uses the Fast API framework and tinydb as a simple local database. 

The paths are as follows: 
- GET /: a simple hello world to test the availability of the API.
- GET /status: returns the current status of the LCD display. The statuses can be "WRITING" (currently displayed), "DO NOT DISTURB", "PLEASE COME IN!" and "INIT" (the initialisation status).
- GET /reset: resets the status of the LCD. It is ignored if it's in WRITING status.
- GET /available: changes the status to "AVAILABLE", unless it is in WRITING status. 
- GET /in_meeting: changes the status to "DO NOT DISTURB", unless it is in WRITING status. 

Each time it sets the status, it saves it to the db.json file run with tinydb. 

While the LCD display is in WRITING status, it will never be updated. This is to prevent bugs and text overlays with the LCD display. 

_Please see the README file inside the display/app folder to see how to setup logging and running the API_

You can refer to [this guide](https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/) to run the code at startup.


#### NFC Reader

**You will need to update the UID of the tag you are using for your specific purpose**. 

The NFC reader does the following: 
- Setup the NFC reader
- Initialise the LEDs
- Turn the white LED on (as an indicator that it is waiting for a tag)
- On a loop: 
  - it will wait for an NFC tag
  - turn the white LED off
  - Turn the green LED on and off if it is a valid tag and update the status
  - Turn the red LED on if there is an error with the tag of it is invalid

The current LED will indicate the status. 
RED -> IN A MEETING
GREEN -> AVAILABLE
WHITE -> INIT, WRITING, UPDATING


You can refer to [this guide](https://www.raspberrypi-spy.co.uk/2015/05/using-an-i2c-enabled-lcd-screen-with-the-raspberry-pi/) to run the code at startup.

## Future improvements
- Use magnets rather than super glue for the cases
- Improve the sign of the LCD panel space in the NFC reader
- Create a cover for the LED lights
- Reduce the size of the LCD sign
- Fix the size of the LCD holder on the LCD sign
- Add a cron job to clean logs on the API side to avoid overuse of the RPI's storage