# IMAGPRO - S12
## Guided Research Project Final Code
### Group 2
- Javier, Juan Diego
- Kho, John
- La’O, Erin Denise
- Reyes, Cyril Sam

### Purpose of the Project
**VividView** is a real-time color blind accessibility enhancement tool through Daltonization. We aim to improve accessibility in visual content such that people with colorblindness may be able to view live camera feed in a manner that caters to their needs. Capabilities of the tool include presets for Deuteranomaly, Protanomaly, and Tritanomaly, as well as different ways to adjust the level of the correction & intensities of different color channels. There are also various video modifications such as zoom, flip, brightness, and contrast.

### Packages and Dependencies
- `cv2`
- `numpy`

### General Use of Project
This project is a Python file originally developed and ran in `PyCharm Community Edition 2023.3.5`.

#### To install and deploy the project in PyCharm:
1. Click `File` in the Main Menu
2. Click `Open...`
3. Navigate to the directory you downloaded the Python file to
4. Select `IMAGPRO_VividView.py` in the Open File or Project menu
5. Run the file

#### To use the project:
1. Upon running the file, a new window will open titled `VividView: Daltonization for Color Deficiency Correction`
2. The video on the left is the raw video being picked up by your webcam and the video on the right is the adjusted video
3. Change the sliders above the side-by-side videos to see the different modifications
4. Press `Q` on your keyboard to exit
5. If you want to use a different webcam, go to Line 65 (`vid = cv.VideoCapture(0)`) and change the parameter (0 in the file) to a different value.

### Expected Outputs
- Opened code in PyCharm
![Screenshot 2024-04-18 234847](https://github.com/J1gys/colorblindness-live/assets/57384457/17ec9a9b-0cc6-48e0-9f62-1c87407dbf1c)

- Running project
![Screenshot 2024-04-18 234320](https://github.com/J1gys/colorblindness-live/assets/57384457/8f410c56-7c06-46f3-bb65-dc74c52c969a)

