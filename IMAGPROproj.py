import cv2 as cv
import numpy as np

## Default Values
flip = 0
brightness = 0
contrast = 0
zoom = 50
blue = 0
green = 0
red = 0

## Window Variables
window_name = 'VividView'
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

## Elements
cv.createTrackbar("FLIP", window_name, flip, 1, lambda x:x)
cv.createTrackbar("BRIGHTNESS",window_name,brightness,255, lambda x:x)
cv.createTrackbar("CONTRAST",window_name,contrast,255, lambda x:x)
cv.createTrackbar("ZOOM", window_name, zoom, 50, lambda x:x)
cv.setTrackbarMin("ZOOM", window_name,1)
cv.createTrackbar("RED", window_name, red, 255, lambda x:x)
#cv.setTrackbarMin("RED", window_name,-255)
cv.createTrackbar("GREEN", window_name, green, 255, lambda x:x)
#.setTrackbarMin("GREEN", window_name,-255)
cv.createTrackbar("BLUE", window_name, blue, 255, lambda x:x)
#cv.setTrackbarMin("BLUE", window_name,-255)

## Chosen camera
vid = cv.VideoCapture(0)

## Main Function
while (True):
    ret, frame = vid.read()

    # Operations
    f = cv.getTrackbarPos("FLIP", window_name)
    b = cv.getTrackbarPos("BRIGHTNESS", window_name)
    c = cv.getTrackbarPos("CONTRAST", window_name)
    z = cv.getTrackbarPos("ZOOM", window_name)
    re = cv.getTrackbarPos("RED", window_name)
    gr = cv.getTrackbarPos("GREEN", window_name)
    bl = cv.getTrackbarPos("BLUE", window_name)

    # Zoom
    height, width = frame.shape[:2]
    midX, midY = int(height / 2), int(width / 2)
    scaleX, scaleY = int(z * height / 100), int(z * width / 100)
    minX, maxX = midX - scaleX, midX + scaleX
    minY, maxY = midY - scaleY, midY + scaleY
    adjusted = frame[minX:maxX, minY:maxY]
    adjusted = cv.resize(adjusted, (width, height))

    # Brightness
    cv.normalize(adjusted, adjusted, (0-c)+b, 255+b, cv.NORM_MINMAX)

    # RGB
    img_bl, img_gr, img_re = cv.split(adjusted)
    adjusted = cv.merge([img_bl+bl, img_gr+gr, img_re+re])

    # Flip
    if f == 1:
        adjusted = cv.flip(adjusted, 1)

    # Original text
    cv.putText(frame, "Original", (10,30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show specific changes through text
    cv.putText(adjusted, "b={}".format(b), (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(adjusted, "c={}".format(c), (10, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(adjusted, "z={}".format(z), (10, 90),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(adjusted, "R={}".format(re), (100, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(adjusted, "G={}".format(gr), (100, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(adjusted, "B={}".format(bl), (100, 90),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Put videos side by side
    cv.imshow(window_name, np.hstack([frame, adjusted]))

    # Quit program if 'Q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()