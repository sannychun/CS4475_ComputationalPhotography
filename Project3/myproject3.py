import cv2
import numpy as np
import os

sourceImageList = os.listdir("sources")
src_img = cv2.imread("original.jpg")

# Resizes sources images to 15 x 12 pixels
# Returns array of resized mosaic images
def resizeImages(images):
    fileFormat = ["jpg", "jpeg"]
    images[:] = [img for img in images if img.split(".")[-1].lower() in fileFormat]

    for img in images:
        print img
        image = cv2.imread(os.path.join("sources", img))
        mosaics = cv2.resize(image, (15, 12))
        cv2.imwrite("mosaics/" + img, mosaics)
    return images

# Calculates the average color of each source image
# @param img (numpy.ndarray): image represented as a numpy array
# @return: avg (numpy.ndarray) : tuple with 4 values mean values of (BGR)
def averageRGB(img):
    avg = cv2.mean(img)
    avg = avg[:3]
    return avg

def averageTileRGB(origImage, index):
    pixelSum = np.array([0, 0, 0])
    pixelCount = 0

    difference_y = origImage.shape[0] - index[0]
    difference_x = origImage.shape[1] - index[1]

    if difference_y > 12 and difference_x > 15:
        for i in range(index[0], index[0] + 12):
            for j in range(index[1], index[1] + 15):
                pixelCount += 1
                pixelSum = np.add(pixelSum, origImage[i, j])
    elif difference_y <= 12 and difference_x > 15:
        for i in range(index[0], index[0] + difference_y):
            for j in range(index[1], index[1] + 15):
                pixelCount += 1
                pixelSum = np.add(pixelSum, origImage[i, j])
    elif difference_y > 12 and difference_x <= 15:
        for i in range(index[0], index[0] + 12):
            for j in range(index[1], index[1] + difference_x):
                pixelCount += 1
                pixelSum = np.add(pixelSum, origImage[i, j])
    else:
        for i in range(index[0], index[0] + difference_y):
            for j in range(index[1], index[1] + difference_x):
                pixelCount += 1
                pixelSum = np.add(pixelSum, origImage[i, j])

    average = pixelSum / pixelCount
    return average

# Replace pixels in the original image with mosaics
def createMosaic(mosaic_img, image, index):
    difference = mosaic_img.shape[0] - index[0]
    d = mosaic_img.shape[1] - index[1]
    if difference > 12 and d > 15:
        for i in range(index[0], index[0] + 12):
            for j in range(index[1], index[1] + 15):
                mosaic_img[i, j] = image[i % 12, j % 15]
    elif difference <= 12 and d > 15:
        for i in range(index[0], index[0] + difference):
            for j in range(index[1], index[1] + 15):
                mosaic_img[i, j] = image[i % difference, j % 15]
    elif difference > 12 and d <= 15:
        for i in range(index[0], index[0] + 12):
            for j in range(index[1], index[1] + d):
                mosaic_img[i, j] = image[i % 12, j % d]
    else:
        for i in range(index[0], index[0] + difference):
            for j in range(index[1], index[1] + d):
                mosaic_img[i, j] = image[i % difference, j % d]

# Calculates the best mosaic image to replace in original image
# @param origImage: the original image to be modified
# @param images: list of images in mosaics folder
# @return: the newly created output image
def createNewImage(origImage, images):
    createNewImage = images[0]
    mosaic_img = np.zeros((origImage.shape[0], origImage.shape[1], 3))

    for i in range(0, origImage.shape[0], 12):  # 0 to height of image
        for j in range(0, origImage.shape[1], 15):  # 0 to width of image
            block_index = (i, j)
            block_avg = averageTileRGB(origImage, block_index)

            # I chose 128 for grayscale intensity. This is arbitrary.
            threshold = np.sqrt(3 * np.power(128, 2))

            for img in images:
                img = cv2.imread("mosaics/" + img)
                difference = np.sqrt(np.power(block_avg[0] - averageRGB(img)[0],2)
                                     +np.power(block_avg[1] - averageRGB(img)[1],2)
                                     +np.power(block_avg[2] - averageRGB(img)[2],2))

                if difference < threshold:
                    threshold = difference
                    createNewImage = img

            index = (i, j)
            createMosaic(mosaic_img, createNewImage, index)
    return mosaic_img

sourceImageList = resizeImages(sourceImageList)
mosaic = createNewImage(src_img, sourceImageList)
cv2.imwrite("output.jpg", mosaic)