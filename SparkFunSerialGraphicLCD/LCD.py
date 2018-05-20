#!/usr/bin/python
"""
Graphic Serial LCD Libary Main File
Alfredo Rius, based on Joel Bartlett's Arduino implementation and the docs:

https://www.sparkfun.com/datasheets/LCD/Monochrome/Corrected-SFE-0016-DataSheet-08884-SerialGraphicLCD-v2.pdf

10-16-2016
"""

from PIL import Image

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

    def write(self,string,align='left',width=None):
        """
        Print text
        26 characters is the length of one line on the LCD
        align(str) can be 'left', 'right', or 'center'
        width(int) can be the width of te screen or less
        """ 
        # Set default line width
        if not width or width > self.width:
            width = self.width
        
        # Align using spaces if necessary
        if align == 'center':
            if(len(string)<self.width):
                string = ' '*int((width/(self.char_width+self.letter_spacing)/2)-(len(string)/2)) + string

        elif align == 'right':
            if(len(string)<self.width):
                string = ' '*int((width/(self.char_width+self.letter_spacing))-len(string)) + string

        self.s.write(string.encode())
      
    def writeln(self,string):
        """
        Print simple line of text
        26 characters is the length of one line on the LCD
        Doesn't work
        """ 
        self.write((string+'\x10\x13').encode())
      
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
        self.s.write(b'\x7C\x02')
        self.write_bytes(duty)
    
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
        self.s.write(b'\x7C\x07')
        self.write_bytes(key)
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
        self.s.write(b'\x7C\x18')
        self.write_bytes(x)
    
    def y(self,y):
        """
        Set Y inverse to the cartesian plane
        """
        if y > self.height - self.char_height:
            # Avoid screen overflow
            self.s.write(b'\x7C\x19')
            self.write_bytes(self.char_height)
        else:
            self.s.write(b'\x7C\x19')
            self.write_bytes(self.height-y)

    def write_bytes(self,string):
        """
        Write encoded bytes
        """
        self.s.write(bytes(chr(string),'utf-8'))

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

    def col_row(self,col,row):
        """
        Sets the cursor to the specific column and row
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
        self.s.write(b'\x7C\x10')
        self.write_bytes(x)
        self.write_bytes(self.height-y)
        self.s.write(b'\x01')

    def clear_pixel(self,x,y):
        """
        Clear Pixel
        """
        self.s.write(b'\x7C\x10')
        self.write_bytes(x)
        self.write_bytes(self.height-y)
        self.s.write(b'\x00')

    def line(self,x1,y1,x2,y2):
        """
        Set Line
        """
        self.s.write(b'\x7C\x0C')
        self.write_bytes(x1)
        self.write_bytes(self.height-y1)
        self.write_bytes(x2)
        self.write_bytes(self.height-y2)
        self.s.write(b'\x01')
        
    def clear_line(self,x1,y1,x2,y2):
        """
        Clear Line
        """
        self.s.write(b'\x7C\x0C')
        self.write_bytes(x1)
        self.write_bytes(self.height-y1)
        self.write_bytes(x2)
        self.write_bytes(self.height-y2)
        self.s.write(b'\x00')
        
    def box(self,x1,y1,x2,y2):
        """
        Set Box
        """
        self.s.write(b'\x7C\x0F')
        self.write_bytes(x1)
        self.write_bytes(self.height-y1)
        self.write_bytes(x2)
        self.write_bytes(self.height-y2)
        self.s.write(b'\x01')
        
    def clear_box(self,x1,y1,x2,y2):
        """
        Clear Box
        """
        self.s.write(b'\x7C\x0F')
        self.write_bytes(x1)
        self.write_bytes(self.height-y1)
        self.write_bytes(x2)
        self.write_bytes(self.height-y2)
        self.s.write(b'\x00')

    def circle(self,x,y,rad):
        """
        Set Circle
        """
        self.s.write(b'\x7C\x03')
        self.write_bytes(x)
        self.write_bytes(self.height-y)
        self.write_bytes(rad)
        self.s.write(b'\x01')

    def clear_circle(self,x,y,rad):
        """
        Clear Circle
        """
        self.s.write(b'\x7C\x03')
        self.write_bytes(x)
        self.write_bytes(self.height-y)
        self.write_bytes(rad)
        self.s.write(b'\x00')

    def clear_block(self,x1,y1,x2,y2):
        """
        Clear Area inside a block
        """
        self.s.write(b'\x7C\x05')
        self.write_bytes(x1)
        self.write_bytes(self.height-y1)
        self.write_bytes(x2)
        self.write_bytes(self.height-y2)

    def image(self,image_path,x1,y1,x2,y2,invert=False):
        """
        Renders a black an white image
        """
        # Load image
        img = Image.open(image_path)
        # Convert to b/w
        img = img.convert('1')
        # Validate dimensions
        if x2 < x1:
            tmp = x1
            x1 = x2
            x2 = tmp
        if y2 < y1:
            tmp = y1
            y1 = y2
            y2 = tmp
        # Resize to specific dimensions
        img = img.resize((x2-x1,y2-y1))
        # Clear the block where the image is going to be displayed
        self.clear_block(x1,y1,x2,y2)
        # Scan the image for set pixels
        for j in range(img.size[1]):
            for i in range(img.size[0]):
                if not invert and img.getpixel((i,j)):
                    # Set the pixel
                    self.pixel(x1+i,y1+j)
                elif invert and not img.getpixel((i,j)):
                    self.pixel(x1+i,y1+j)
                    
