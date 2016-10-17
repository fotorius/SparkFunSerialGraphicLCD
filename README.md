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

## Initialization Options
| Option | Default | Description |
|:---:|:---:|---|
| **baudrate** | 115200 | The serial connection baudrate. |
| **port** | '/dev/ttyAMA0' | The hardware serial port to the LCD. |
| **line_height** | 1 | The space beteen lines (dependant on the hardware. |
| **letter_spacing** | 1 | The space between letters. |
| **char_width** | 5 | The with of the actual letters. |
| **char_height** | 7 | The height of the actual letters. |
| **width** | 160 | Width of the screen (dependant on the hardware and based in the SparkFun Graphic LCD 160x128 Huge). |
| **height** | 128 | Height of the screen (dependant on the hardware and based in the SparkFun Graphic LCD 160x128 Huge). |


## Methods
| Method | Description |
|:---| --- |
| **close()** | Closes connection to the serial port. |
| **clear()** | Clears the screen. |
| **write(string)** | Writes a string. |
| **reverse()** | Clears and reverses all pixels on the screen. |
| **splash()** | Shows the SparkFun's splas screen. |
| **backlight(duty)** | Sets the backlight of the screen (0 - 100). |
| **baudrate(baudrate)** | Sets the baudrate of the screen and updates the baudrate of the serial interface. |
| **restore_baudrate()** | Restores the baudrate to the default (115200). |
| **demo()** | Launches the demonstration mode. |
| **x(x)** | Sets the cursor to the position 'x'. |
| **y(y)** | Sets the cursor to the position 'y' (inverse of the cartesian plane, from top to bottom). |
| **position(x,y)** | Sets the cursor to the position 'x','y'. |
| **row(row)** | Sets the cursor in the specified (text) row. |
| **col(col)** | Sets the cursor in the specified (text) column. |
| **row_col(row,col)** | Sets the cursor in the specified (text) row and column. |
| **home()** | Sets the cursor in the position 0,0. |
| **pixel(x,y)** | Sets the pixel in coordenates x,y. |
| **clear_pixel(x,y)** | Clears the pixel in coordenates x,y. |
| **line(x1,y1,x2,y2)** | Draws a line from x1,y1 to x2,y2. |
| **clear_line(x1,y1,x2,y2)** | Clears the line from x1,y1 to x2,y2. |
| **box(x1,y1,x2,y2)** | Draws a box from x1,y1 to x2,y2. |
| **clear_box(x1,y1,x2,y2)** | Clears the box from x1,y1 to x2,y2. |
| **circle(x,y,rad)** | Draws a circle with center x,y and radius rad. |
| **clear_circle(x,y,rad)** | Clears the circle with center x,y and radius rad. |
| **clear_block(x1,y1,x2,y2)** | Clears everything inside the block x1,y1 to x2,y2. |

## More information
- Here is the official [Graphic LCD Serial Backpack Datasheet](https://www.sparkfun.com/datasheets/LCD/Monochrome/Corrected-SFE-0016-DataSheet-08884-SerialGraphicLCD-v2.pdf) from SparkFun (very usefull but not easy to find).
- This is the [Arduino Library](https://github.com/sparkfun/SparkFun_Graphic_LCD_Serial_Backpack_Arduino_Library/tree/V_1.0.1) from the official SparkFun Repository.
- The GitHub resource to this [Open Source Project](https://github.com/sparkfun/GraphicLCD_Serial_Backpack)
- [SparkFun Graphic LCD Serial Backpack Product Page](https://www.sparkfun.com/products/9352)
