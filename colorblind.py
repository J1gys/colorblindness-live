import cv2 as cv
import numpy as np


def daltonize(image, level, deficiency_type):
    # DALTONIZATION/COLOR BLINDNESS CORRECTION GOES HERE

    # Notes 4/4/2024 - Tritanomaly matrix values are placeholder atm
    
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


correction_level = 100
correction_types = ["Deuteranomaly", "Protanomaly", "Tritanomaly"]
current_correction_type = "Deuteranomaly"

window_name = 'Daltonization for Color Deficiency Correction'
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
cv.createTrackbar("Correction Level (%)", window_name, correction_level, 200, lambda x: x)
cv.createTrackbar("Correction Type", window_name, 0, len(correction_types) - 1, lambda x: x)

vid = cv.VideoCapture(0)

while True:
    ret, frame = vid.read()

    level = cv.getTrackbarPos("Correction Level (%)", window_name) / 100.0
    correction_type_index = cv.getTrackbarPos("Correction Type", window_name)
    current_correction_type = correction_types[correction_type_index]

    corrected = daltonize(frame, level, current_correction_type)

    cv.putText(corrected, "Correction Level: {:.2f}".format(level), (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv.putText(corrected, "Correction Type: {}".format(current_correction_type), (10, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.imshow(window_name, np.hstack([frame, corrected]))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
