# File: ImageShop.py

"""
This program implements the ImageShop application, which
is a basic photo editor in Python.
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton
from GrayscaleImage import createGrayscaleImage
from equalize import equalize
from statistics import mean

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def ImageShop():
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth()) / 2
        y = (gw.getHeight() - image.getHeight()) / 2
        gw.add(image, x, y)

    def loadButtonAction():
        """Callback function for the Load button"""
        filename = chooseInputFile()
        if filename != "":
            setImage(GImage(filename))

    def flipVerticalAction():
        """Callback function for the flipVertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))

    def flipHorizontalAction():
        """Callback function for the flipHorizontal button"""
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))

    def rotateLeftAction():
        """Callback function for the rotateLeft button"""
        if currentImage is not None:
            setImage(rotateLeft(currentImage)) 

    def rotateRightAction():
        """Callback function for the rotateRight button"""
        if currentImage is not None:
            setImage(rotateRight(currentImage)) 

    def grayscaleAction():
        """Callback function for the grayscale button"""
        if currentImage is not None:
            setImage(createGrayscaleImage(currentImage)) 

    def greenScreenAction():
        """Callback function for the greenScreen button"""
        if currentImage is not None:
            setImage(greenScreen(currentImage)) 

    def equalizeAction():
        """Callback function for the equalize button"""
        if currentImage is not None:
            setImage(equalize(currentImage))
            #print(equalize(currentImage))

    def blurAction():
        """Callback function for the blur button"""
        if currentImage is not None:
            setImage(blur(currentImage))
        
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton("Flip Horizontal", flipHorizontalAction)
    addButton("Rotate Left", rotateLeftAction)
    addButton("Rotate Right", rotateRightAction)
    addButton("Grayscale", grayscaleAction)
    addButton("Green Screen", greenScreenAction)
    addButton("Equalize", equalizeAction)
    addButton("Blur", blurAction)

def flipVertical(image):
    """Creates a new GImage from the original one by flipping it vertically."""
    array = image.getPixelArray()
    return GImage(array[::-1])


def flipHorizontal(image):
    """Creates a new GImage from the original one by flipping it horizontally."""
    array = image.getPixelArray()
    for row in range(len(array)):
        array[row] = array[row][::-1]
    return GImage(array) 


def rotateLeft(image):
    """Creates a new GImage from the original one by transposing it along y = -x."""
    array = image.getPixelArray()
    #new_array = [[0]*len(array)]*len(array[0])
    new_array = [[[0] for i in range(len(array))] for j in range(len(array[0]))]
    for i in range(len(array)):
        for j in range(len(array[0])):
            new_array[-j][i] = array[i][j]
    return GImage(new_array)

def rotateRight(image):
    """Creates a new GImage from the original one by transposing it along y = x."""
    array = image.getPixelArray()
    #new_array = [[0]*len(array)]*len(array[0])
    new_array = [[[0] for i in range(len(array))] for j in range(len(array[0]))]
    for i in range(len(array)):
        for j in range(len(array[0])):
            new_array[j][-i] = array[i][j]
    return GImage(new_array)

def greenScreen(image):
    """Creates a new GImage from the original one by replacing pixels in the
    original one with pixels in another chosen picture when the pixel of 
    the chosen picture is not green."""
    array = image.getPixelArray()
    new_filename = chooseInputFile()
    new_image = GImage(new_filename)
    new_array = new_image.getPixelArray()

    for i in range(min(len(array), len(new_array))):
        for j in range(min(len(array[0]), len(new_array[0]))):
            if not (bin(new_array[i][j])[18:26] > 2*max(bin(new_array[i][j])[10:18], bin(new_array[i][j])[26:34])):
                array[i][j] = new_array[i][j]

    return GImage(array)

def blur(image):
    """Implements a blur function that takes the average of the red,
    green, and blue of surrounding pixels—needs to be applied several
    times to notice the effect, usually."""
    array = image.getPixelArray()
    for i in range(len(array)):
        for j in range(len(array[0])):
            if (i != 0) and (i != (len(array) - 1)) and (j != 0) and (j != (len(array[0]) - 1)):
                # Pick out the RBG components of surrounding pixels
                i_red = bin(array[i][j])[10:18]
                i_green = bin(array[i][j])[18:26]
                i_blue = bin(array[i][j])[26:34]
                ip1_red = bin(array[i+1][j])[10:18]
                ip1_green = bin(array[i+1][j])[18:26]
                ip1_blue = bin(array[i+1][j])[26:34]
                im1_red = bin(array[i-1][j])[10:18]
                im1_green = bin(array[i-1][j])[18:26]
                im1_blue = bin(array[i-1][j])[26:34]
                jp1_red = bin(array[i][j+1])[10:18]
                jp1_green = bin(array[i][j+1])[18:26]
                jp1_blue = bin(array[i][j+1])[26:34]
                jm1_red = bin(array[i][j-1])[10:18]
                jm1_green = bin(array[i][j-1])[18:26]
                jm1_blue = bin(array[i][j-1])[26:34]
                # Average the RBG components
                new_red = round(mean([int(i_red, 2), int(ip1_red, 2), int(im1_red, 2),
                               int(jp1_red, 2), int(jm1_red, 2)]))
                new_green = round(mean([int(i_green, 2), int(ip1_green, 2), int(im1_green, 2),
                               int(jp1_green, 2), int(jm1_green, 2)]))
                new_blue = round(mean([int(i_blue, 2), int(ip1_blue, 2), int(im1_blue, 2),
                               int(jp1_blue, 2), int(jm1_blue, 2)]))
                # Make the new pixel with the averages
                array[i][j] = GImage.createRGBPixel(new_red, new_green, new_blue)
    return GImage(array)

# Startup code

if __name__ == "__main__":
    ImageShop()
