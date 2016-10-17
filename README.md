# SparkFunSerialGraphicLCD 
A simple way te get started with the [SparkFun Graphic LCD Serial Backpack](https://www.sparkfun.com/products/9352) that supports the [Graphic LCD 128x64 STN LED Backlight](https://www.sparkfun.com/products/710) and the [Graphic LCD 160x128 Huge](https://www.sparkfun.com/products/8799) screens.

Very easy to set up (but not exclusively) with the Raspberry Pi.

## Installation
```bash
# Common dependencies
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python-serial python-pip

# The actual library
sudo pip install -U git+https://github.com/devalfrz/SparkFunSerialGraphicLCD.git
```

## Usage
On a file named `hello_world.py` write the following:
```python
#!/usr/bin/python

# Import the library
from SparkFunSerialGraphicLCD.LCD import LCD

# Initialize the display
lcd = LCD()

# Clean the display to start fresh
lcd.clear()

# Write something
lcd.write('Hello World!')

# Close the connection to the display
lcd.close()
```
Then run this code!
```bash
sudo python hello_world.py
```
