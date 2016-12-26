# CS4475 Summer 2016
# Project 1 "4 Seasons"
# Sanghyun Sanny Chun
# GTID: 902759995

import cv2
import numpy as np

# findGreen sets all the pixels in a given range of colors a value of 1. Everything else is 0.
# For this project, I tried to detect as many shades of green as possible.
def findGreen(landscapeHSV):
    lowerBound = np.array([20, 00, 50], dtype=np.uint8)
    upperBound = np.array([195, 255, 195], dtype=np.uint8)
    imageMask = cv2.inRange(landscapeHSV, lowerBound, upperBound)
    cv2.imwrite("imageMask.jpg", imageMask)
    return imageMask

# This function changes the greens into white for a SNOW EFFECT. Note that not every single shade of green
# may be detected.
def changetoWinter(landscapeHSV, imageMask):
    landscapeHSV[np.where((imageMask == [255, 255, 255]).all(axis=2))] = [255, 255, 230]
    return landscapeHSV

# This function changes the greens into tan/orange for an AUTUMN EFFECT. Note that not every single shade of green
# may be detected.
def changetoFall(landscapeHSV, imageMask):
    landscapeHSV[np.where((imageMask == [255, 255, 255]).all(axis=2))] = [0, 150, 230]
    return landscapeHSV

# This function changes the greens into bright green for an SUMMEr EFFECT. Note that not every single shade of green
# may be detected.
def changetoSummer(landscapeHSV, imageMask):
    landscapeHSV[np.where((imageMask == [255, 255, 255]).all(axis=2))] = [45, 235, 143]
    return landscapeHSV

# Read the input image. Have to have 2 copies, one for Fall and one for Winter
image1 = cv2.imread("input.jpg")
image1_2 = cv2.imread("input.jpg")
image1_3 = cv2.imread("input.jpg")

# I then find the mask, and save it as imageMask.jpg
imageMask = findGreen(image1)
image2 = cv2.imread("imageMask.jpg")

# Apply season functions here
winterImage = changetoWinter(image1, image2)
fallImage = changetoFall(image1_2, image2)
summerImage = changetoSummer(image1_3, image2)

# Gaussian filter to smooth out the end images
winterImage = cv2.GaussianBlur(winterImage, (5, 5), 0)
fallImage = cv2.GaussianBlur(fallImage, (5, 5), 0)
summerImage = cv2.GaussianBlur(summerImage, (5, 5), 0)

cv2.imwrite("winterImage.jpg", winterImage)
cv2.imwrite("fallImage.jpg", fallImage)
cv2.imwrite("summerImage.jpg", summerImage)