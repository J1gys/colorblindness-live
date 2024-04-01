import cv2 as cv
import numpy as np


def daltonize(image, level):
    # DALTONIZATION/COLOR BLINDNESS CORRECTION GOES HERE
    daltonization_matrix = np.array([[1, 0, 0],
                                     [0.4942, 0, 1.2483],
                                     [0, 0, 1]])
    
    corrected_image = cv.transform(image, daltonization_matrix * level)
    return corrected_image


correction_level = 100
window_name = 'Daltonization for Deuteranomaly Correction'
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
cv.createTrackbar("Correction Level (%)", window_name, correction_level, 200, lambda x:x)
vid = cv.VideoCapture(0)

while (True):
    ret, frame = vid.read()
    level = cv.getTrackbarPos("Correction Level (%)", window_name) / 100.0
    corrected = daltonize(frame, level)
    cv.putText(corrected, "Correction Level: {:.2f}".format(level), (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.imshow(window_name, np.hstack([frame, corrected]))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
