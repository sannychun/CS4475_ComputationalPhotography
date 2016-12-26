import cv2


# downsample image using Gaussian pyramid
def downsample(image):
    downscaleSteps = 1  # number of downscaling steps
    bilatFilters = 50  # number of bilateral filtering steps

    # downsample image by the number of steps given
    for _ in xrange(downscaleSteps):
        image = cv2.pyrDown(image)
    # repeatedly apply small bilateral filter
    for _ in xrange(bilatFilters):
        image = cv2.bilateralFilter(image, 15, 15, 15)
    # upsample image to original size
    for _ in xrange(downscaleSteps):
        image = cv2.pyrUp(image)
    return image

# convert to grayscale
def grayscale(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return grayImage

# Apply median blur
def medianBlur(grayImage, degree):
    blurImage = cv2.medianBlur(grayImage, degree)
    return blurImage

def render(image):
    # get rows and columns and downscale image to half size
    image = cv2.imread(image)
    rows = image.shape[1]
    cols = image.shape[0]
    # Downscale image to half if either the rows or columns exceed 700 pixels
    if rows > 700 | cols > 700:
        image = cv2.resize(image, (rows / 2, cols / 2))

    # Apply downsampling, grayscaling and median blur to image
    gaussianImage = downsample(image)
    grayImage = grayscale(image)
    blurImage = medianBlur(grayImage, 3)

    # detect and enhance edges
    edgeMask = cv2.adaptiveThreshold(blurImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # convert image back to color and add it with edge mask
    (x,y,z) = gaussianImage.shape
    edgeMask = cv2.resize(edgeMask,(y,x))
    edgeMask = cv2.cvtColor(edgeMask, cv2.COLOR_GRAY2RGB)
    cv2.imwrite("mask.jpg",edgeMask)
    return cv2.bitwise_and(gaussianImage, edgeMask)

sourceImage = "source.jpg"
output = render(sourceImage)
cv2.imwrite("cartoon.jpg", output)
cv2.imshow("Cartoon Effect", output)

cv2.waitKey(0)
cv2.destroyAllWindows()