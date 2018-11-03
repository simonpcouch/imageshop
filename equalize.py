# File: equalize.py

"""
This module implements the equalize function that is included
in the ImageShop program.
"""

from GrayscaleImage import luminance
from pgl import GImage

def equalize(image):
    array = image.getPixelArray()
    image_hist = computeImageHistogram(array)
    cuml_hist = computeCumulativeHistogram(image_hist)
    lum_array = computeNewLuminance(cuml_hist, array)
    new_array = luminanceToGreyscale(lum_array)
    return(GImage(new_array))

def computeImageHistogram(array):
    """Takes in an image array and computes an image histogram"""
    histogram = [0]*256
    lum = 0
    for i in range(len(array)):
        for j in range(len(array[0])):
            lum = luminance(array[i][j])
            histogram[lum] += 1
    return(histogram)

def computeCumulativeHistogram(image_hist):
    """Takes in an image histogram and computes a cumulative histogram"""
    histogram = [0]*256
    for i in range(len(image_hist)):
        if i == 1:
            histogram[1] = image_hist[1]
        else: histogram[i] = image_hist[i] + histogram[i - 1]
    return(histogram)

def computeNewLuminance(cuml_hist, array):
    """Takes in a cumulative histogram and computes equalized luminances"""
    for i in range(len(array)):
        for j in range(len(array[0])):
            array[i][j] = round(255 * cuml_hist[luminance(array[i][j])] / (len(array)*len(array[0])))
    return(array)

def luminanceToGreyscale(lum_array):
    """Takes in an array of luminances and returns an image array"""
    for i in range(len(lum_array)):
        for j in range(len(lum_array[0])):
            lum_array[i][j] = GImage.createRGBPixel(lum_array[i][j], lum_array[i][j], lum_array[i][j])
    return(lum_array)
