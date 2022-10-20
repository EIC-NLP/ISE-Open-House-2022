#%%
# Importing all the library that are needed
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cv2
import cvzone
import random
import math



# Video capture configuration
[X_RESOLUTION, Y_RESOLUTION, VIDEO_FPS] = [1280, 720, 30]
CAMERA_PORT = 0

# Theme color configuration
POLYLINE_COLOR = (33, 28, 206)   # Light Red
LINE_COLOR     = (189, 192, 38)  # Turquiose
CIRCLE_COLOR   = (67, 227, 185)  # Light Green
TEXT_COLOR     = (255, 255, 255) # White
TEXTBOX_COLOR  = (243, 167, 43)  # Light Orange

#%%
# Previous decleared constants
[X_RESOLUTION, Y_RESOLUTION, VIDEO_FPS] = [1280, 720, 30]
CAMERA_PORT = 0

# A function to config the camera
def initialise_video_capture():
    global cap
    cap = cv2.VideoCapture(CAMERA_PORT)
    cap.set(3, X_RESOLUTION)
    cap.set(4, Y_RESOLUTION)
    cap.set(5, VIDEO_FPS)


initialise_video_capture()