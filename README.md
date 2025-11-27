# OSoFaTraBImISoFaCROLVARP
<h3>Open Source Facial Tracking Based Image Interchange Software for Fantasy Character Roleplay and Other Live Video And Related Purposes</h3>
This is a simple program that can be used to indirectly replace a live image feed of your face with a live "animated" version. The main reason you would want to use this software would be to keep your face hidden while still providing a video feed. Any set of eight PNG images can be used but for the best results you might want to use eight images of a character with each one of these combinations:

* ooo.png -> left eye opened, right eye opened, mouth opened
* coo.png -> left eye closed, right eye opened, mouth opened
* oco.png -> left eye opened, right eye closed, mouth opened
* ooc.png -> left eye opened, right eye opened, mouth closed
* cco.png -> left eye closed, right eye closed, mouth opened
* coc.png -> left eye closed, right eye opened, mouth closed
* occ.png -> left eye opened, right eye closed, mouth closed
* ccc.png -> left eye closed, right eye closed, mouth closed

## Features
### Virtual camera
With the help of the pyvirtualcam library, this software can act as a virtual camera and completely replace the live feed from your webcam. This means that you can use this software with most other programs, even if they aren't explicitly compatible with OSoFaTraBImISoFaCROLVARP.
### Background support
If the eight PNG images have transparency, you can add a background. It has to have the same resolution as the eight images and be a PNG.

To enable this function, edit the config.txt file and add the line `bg: path/to/background.png`. Replace path/to/background.png with the path to your image. Animated backgrounds are not yet supported.
## If you want to try out this software...
You can use the example images provided in the example_images.zip file. Just unzip the file and copy the contents along side the binary.

The images are of an original character created by my friend, who also drew the images.
## How to setup and install
### Linux
Before you begin, you are going to need:
#### Software:
* A copy of the binary version of OSoFaTraBImISoFaCROLVARP (you can get it from Releases)
* A copy of face_landmarker.task from Google (you can get it [here](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task))
* The eight PNG images with the same resolution
* v4l2loopback installed and loaded (run `sudo modprobe v4l2loopback`)
#### Hardware:
* Computer
* Webcam (If you don't have one, you can connect your phone and use it as a camera using something like DroidCam)

Make sure all files are in the same directory. If necessary, chmod the OSoFaTraBImISoFaCROLVARP binary.

Now, all you're going to need to do is run the binary and calibrate the software. Calibration usually takes less than a minute and only has to be done once.
### Windows
Before you begin, you're going to need:
#### Software
* A copy of the binary EXE version of OSoFaTraBImISoFaCROLVARP (you can get it from Releases)
* A copy of face_landmarker.task from Google (you can get it [here](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task))
* The eight PNG images with the same resolution
* A copy of OBS installed
#### Hardware:
* Computer
* Webcam (If you don't have one, you can connect your phone and use it as a camera using something like DroidCam)

Make sure that the exe file is in the same folder as the images and as face_landmarker.task. Open the properties of the exe file and unblock it. Run the exe file and do the calibration procedure, which should last less than a minute and only has to be done once.

If you want to make a shortcut to the OSoFaTraBImISoFaCLORVARP binary, make sure to also add the program direcory's path into the Start in textbox.

## Different problems that might arise and how to fix them
### Program closes quickly before being opened
The most common cause is that no camera is plugged in, recognized, or matches the stream index

If a camera is plugged in and recognized (you can see work it in a camera app) the issue might be that it has a different stream id than expected. Edit the config.txt file located in the software's folder and change the number in the line `stream: 0` to something else, like 1 or 2. Restart the software and see if it now works.

### Program is running very slowly
This issue is usually caused by:
* Insufficiently powerful hardware
* PNG images with too high of a resolution

The only issue that you can easily fix is the images one. Make sure that your images' resolution is smaller or equal to 1920x1080 or 1080x1920. In testing, anything more than that causes severe performance issues.
### Calibration result is not satisfactory
Delete the .cal file located in the executable's directory and redo calibration.

## How to build from source
### Linux
Make sure that you have installed python3-pip, python3-tk, pyinstaller and all the libraries from requirements.txt.

To make the binary, clone this repo and, in the resulting directory, run the command `pyinstaller main.py -F --hidden-import='PIL._tkinter_finder'`.

You can find the finished file in ./dist with the name main.
### Windows
Make sure that you have installed Python and pyinstaller.

To make the binary, clone this repo and, in the resulting directory, run the command `pyinstaller main.py -F`.

The resulting exe can be found in the dist folder.