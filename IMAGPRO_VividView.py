##########################
##      VIVIDVIEW       ##
##  Javier, Juan Diego  ##
##  Kho, John           ##
##  La’O, Erin Denise   ##
##  Reyes, Cyril Sam    ##
##########################

## Libraries
import cv2 as cv
import numpy as np

## Color Blindness Correction Function
def daltonize(image, level, deficiency_type):
    daltonization_matrices = {
        "Deuteranomaly": np.array([[1, 0, 0],
                                   [0.4942, 0, 1.2483],
                                   [0, 0, 1]]),
        "Protanomaly": np.array([[0, 2.0234, -2.5258],
                                 [0, 1, 0],
                                 [0, 0, 1]]),
        "Tritanomaly": np.array([[0.967, 0.033, 0],
                                 [0, 0.733, 0.267],
                                 [0, 0.183, 0.817]])
    }

    daltonization_matrix = daltonization_matrices.get(deficiency_type, None)

    if daltonization_matrix is None:
        raise ValueError("Invalid deficiency type. Supported types are: Deuteranomaly, Protanomaly, Tritanomaly")

    corrected_image = cv.transform(image, daltonization_matrix * level)
    return corrected_image


## Default Values
flip = 0
brightness = 0
contrast = 0
zoom = 1
blue = 255
green = 255
red = 255
correction_level = 100
correction_types = ["Deuteranomaly", "Protanomaly", "Tritanomaly"]
current_correction_type = "Deuteranomaly"

## Window Variables
window_name = 'VividView: Daltonization for Color Deficiency Correction'
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

## Elements
cv.createTrackbar("Correction Level (%)", window_name, correction_level, 200, lambda x: x)
cv.createTrackbar("Correction Type", window_name, 0, len(correction_types) - 1, lambda x: x)
cv.createTrackbar("FLIP", window_name, flip, 1, lambda x: x)
cv.createTrackbar("BRIGHTNESS", window_name, brightness, 255, lambda x: x)
cv.createTrackbar("CONTRAST", window_name, contrast, 255, lambda x: x)
cv.createTrackbar("ZOOM", window_name, zoom, 50, lambda x: x)
cv.setTrackbarMin("ZOOM", window_name, 1)
cv.createTrackbar("RED", window_name, red, 510, lambda x: x)
cv.createTrackbar("GREEN", window_name, green, 510, lambda x: x)
cv.createTrackbar("BLUE", window_name, blue, 510, lambda x: x)

## Chosen camera
vid = cv.VideoCapture(0)

## Main function
while True:
    ret, frame = vid.read()

    # Operations
    level = cv.getTrackbarPos("Correction Level (%)", window_name) / 100.0
    correction_type_index = cv.getTrackbarPos("Correction Type", window_name)
    f = cv.getTrackbarPos("FLIP", window_name)
    b = cv.getTrackbarPos("BRIGHTNESS", window_name)
    c = cv.getTrackbarPos("CONTRAST", window_name)
    z = cv.getTrackbarPos("ZOOM", window_name)
    re = cv.getTrackbarPos("RED", window_name)
    gr = cv.getTrackbarPos("GREEN", window_name)
    bl = cv.getTrackbarPos("BLUE", window_name)

    # Zoom
    numbers = list(range(1, 51))
    height, width = frame.shape[:2]
    midX, midY = int(height / 2), int(width / 2)
    scaleX, scaleY = int(numbers[50 - z] * height / 100), int(numbers[50 - z] * width / 100)
    minX, maxX = midX - scaleX, midX + scaleX
    minY, maxY = midY - scaleY, midY + scaleY
    corrected = frame[minX:maxX, minY:maxY]
    corrected = cv.resize(corrected, (width, height))

    # Brightness
    cv.normalize(corrected, corrected, (0 - c) + b, 255 + b, cv.NORM_MINMAX)

    # RGB
    img_bl, img_gr, img_re = cv.split(corrected)
    cv.normalize(img_bl, img_bl, 0, bl, cv.NORM_MINMAX)
    cv.normalize(img_gr, img_gr, 0, gr, cv.NORM_MINMAX)
    cv.normalize(img_re, img_re, 0, re, cv.NORM_MINMAX)
    corrected = cv.merge([img_bl, img_gr, img_re])

    # Flip
    if f == 1:
        corrected = cv.flip(corrected, 1)

    # Correction
    current_correction_type = correction_types[correction_type_index]
    corrected = daltonize(corrected, level, current_correction_type)

    # Original text
    cv.putText(frame, "Original", (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show specific changes through text
    cv.putText(corrected, "Correction Level: {:.2f}".format(level), (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "Correction Type: {}".format(current_correction_type), (10, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "b={}".format(b), (10, 90),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "c={}".format(c), (10, 120),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "z={}".format(z), (10, 150),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "R={}".format(re), (100, 90),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "G={}".format(gr), (100, 120),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "B={}".format(bl), (100, 150),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Put videos side by side
    cv.imshow(window_name, np.hstack([frame, corrected]))

    # Quit program if 'Q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
