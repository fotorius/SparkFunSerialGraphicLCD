#!/usr/bin/python
"""
Graphic Serial LCD Libary Main File
Alfredo Rius, based on Joel Bartlett's Arduino implementation and the docs:

https://www.sparkfun.com/datasheets/LCD/Monochrome/Corrected-SFE-0016-DataSheet-08884-SerialGraphicLCD-v2.pdf

10-16-2016
"""

class LCD:
    def __init__(
        self,
        baudrate=115200,
        port='/dev/ttyAMA0',
        line_height=1,
        letter_spacing=1,
        char_width=5,
        char_height=7,
        width=160,
        height=128):
        """
        Initialize display
        """
        # General properties
        self.line_height = line_height
        self.letter_spacing = letter_spacing
        self.char_width = char_width
        self.char_height = char_height
        self.width = width
        self.height = height

        
        # Initialize serial interface

        import serial

        self.s = serial.Serial()

        self.s.baudrate = baudrate
        self.s.port = port
        
        self.s.open()

    def close(self):
        """
        Close Connection with serial interface
        """
        self.s.close()

    def __enter__(self):
        return self.s

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Properly close serial interace
        """
        self.close()

    def clear(self):
        #clears the screen, you will use this a lot!
        self.s.write(b'\x7C\x00')

    def write(self,string):
        """
        Print text
        26 characters is the length of one line on the LCD
        """ 
        self.s.write(string)
      
    def writeln(self,string):
        """
        Print simple line of text
        26 characters is the length of one line on the LCD
        Doesn't work
        """ 
        self.write(string+'\x10\x13')
      
    def reverse(self):
        """
        Reverse Mode, this clears the screen also
        """
        self.s.write(b'\x7C\x12')

    def splash(self):
        """
        Sparkfun Splash Screen
        Doesn't work
        """
        self.s.write(b'\x7C\x13')
    
    def backlight(self,duty):
        """
        Set the back light
        Duty goes from 0 to 100
        """
        self.s.write(b'\x7C\x02%s' % (chr(duty)))
    
    def baudrate(self,baudrate):
        """
        Sets the baudrate
        4800bps - 0x31 = 49
        9600bps - 0x32 = 50
        19,200bps - 0x33 = 51
        38,400bps - 0x34 = 52
        57,600bps - 0x35 = 53
        115,200bps - 0x36 = 54
        """
        import time

        if baudrate == 4800:
            key = 0x31
        elif baudrate == 9600:
            key = 0x32
        elif baudrate == 19200:
            key = 0x33
        elif baudrate == 38400:
            key = 0x34
        elif baudrate == 57600:
            key = 0x35
        elif baudrate == 115200:
            key = 0x36
        else:
            raise ValueError("%d is an invalid baudrate" % baud)
        self.s.write(b'\x7C\x07%s' % (chr(key)))
        self.s.baudrate = baudrate
        time.sleep(1)


    def restore_baudrate(self):
        """
        Restores the baudrate to 115200
        """
        self.baudrate(4800)
        self.baudrate(9600)
        self.baudrate(19200)
        self.baudrate(38400)
        self.baudrate(57600)
        self.baudrate(115200)

    def demo(self):
        """
        Sparkfun Demo
        Doesn't work
        """
        self.s.write(b'\x7C\x04')
    
    def x(self,x):
        """
        Set X
        """
        self.s.write(b'\x7C\x18%s' % (chr(x)))
    
    def y(self,y):
        """
        Set Y inverse to the cartesian plane

        """
        if y > self.height - self.char_height:
            # Avoid screen overflow
            self.s.write(b'\x7C\x19%s' % (chr(self.char_height)))
        else:
            self.s.write(b'\x7C\x19%s' % (chr(self.height-y)))

    def position(self,x,y):
        """
        Set position

        characters are 8 pixels tall x 6 pixels wide
        The top left corner of a char is where the x/y value will start its print
        For example, if you print a char at position 1,1, the bottom right of your char will be at position 7,9.
        Therefore, to print a character in the very bottom right corner, you would need to print at the coordinates 
        x = 154 , y = 120. You should never exceed these values.


         Here we have an example using an upper case 'B'. The star is where the character starts, given a set 
        of x,y coordinates. # represents the blocks that make up the character, and _ represnets the remaining 
        unused bits in the char space. 
            *###__
            #   #_
            #   #_
            ####__
            #   #_
            #   #_
            ####__
            ______

        """
        self.x(x)
        self.y(y)

    def row(self,row):
        """
        Sets the cursor to the specific row
        """
        self.y((row*(self.char_height+self.line_height))+1)

    def col(self,col):
        """
        Sets the cursor to the specific column
        """
        self.x((col*(self.char_width+self.letter_spacing))+1)

    def row_col(self,row,col):
        """
        Sets the cursor to the specific row and column
        """
        self.row(row)
        self.col(col)



    def home(self):
        """
        Sets the cursor in 0,0
        """
        self.x(0)
        self.y(0)

    def pixel(self,x,y):
        """
        Set Pixel
        """
        self.s.write(b'\x7C\x10%s%s\x01' % (chr(x),chr(y)))

    def clear_pixel(self,x,y):
        """
        Clear Pixel
        """
        self.s.write(b'\x7C\x10%s%s\x00' % (chr(x),chr(y)))

    def line(self,x1,y1,x2,y2):
        """
        Set Line
        """
        self.s.write(b'\x7C\x0C%s%s%s%s\x01' % (chr(x1),chr(y1),chr(x2),chr(y2)))
        
    def clear_line(self,x1,y1,x2,y2):
        """
        Clear Line
        """
        self.s.write(b'\x7C\x0C%s%s%s%s\x00' % (chr(x1),chr(y1),chr(x2),chr(y2)))
        
    def box(self,x1,y1,x2,y2):
        """
        Set Box
        """
        self.s.write(b'\x7C\x0F%s%s%s%s\x01' % (chr(x1),chr(y1),chr(x2),chr(y2)))
        
    def clear_box(self,x1,y1,x2,y2):
        """
        Clear Box
        """
        self.s.write(b'\x7C\x0F%s%s%s%s\x00' % (chr(x1),chr(y1),chr(x2),chr(y2)))

    def circle(self,x,y,rad):
        """
        Set Circle
        """
        self.s.write(b'\x7C\x03%s%s%s\x01' % (chr(x),chr(y),chr(rad)))

    def clear_circle(self,x,y,rad):
        """
        Clear Circle
        """
        self.s.write(b'\x7C\x03%s%s%s\x00' % (chr(x),chr(y),chr(rad)))

    def clear_block(self,x1,y1,x2,y2):
        """
        Clear Area inside a block
        """
        self.s.write(b'\x7C\x05%s%s%s%s' % (chr(x1),chr(y1),chr(x2),chr(y2)))

