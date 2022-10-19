# %%
# from functools import cache, lru_cache
from turtle import color
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cv2
import cvzone
import random
import math

print("")

CAMERA_PORT = 0  # 2 for external and 0 fo internal
# [X_RESOLUTION, Y_RESOLUTION, VIDEO_FPS] = [1920, 1080, 30]
[X_RESOLUTION, Y_RESOLUTION, VIDEO_FPS] = [1280, 720, 30]

# Colour constants BGR not RGB
# POLYLINE_COLOR = (255, 255, 255)  # White line
# LINE_COLOR = (0, 0, 255) # Red in BGR
# CIRCLE_COLOR = (255, 0, 0) # Blue in BGR

# * Colors to try out
# Light Red   (33,28,206)
# Turquiose   (189,192,38)
# Light Green (67, 227, 185)
# Light Orange (243,167,43)

POLYLINE_COLOR = (33, 28, 206)
LINE_COLOR = (189, 192, 38)
CIRCLE_COLOR = (67, 227, 185)
TEXT_COLOR = (255, 255, 255)
TEXTBOX_COLOR = (243, 167, 43)


def initialise_video_capture():
    global cap
    cap = cv2.VideoCapture(CAMERA_PORT)  # ! change the webcam device
    cap.set(3, X_RESOLUTION)
    cap.set(4, Y_RESOLUTION)
    cap.set(5, VIDEO_FPS)


initialise_video_capture()

detector = HandDetector(detectionCon=0.8, maxHands=2)


# %%
class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain,
                               "Press SpaceBar to restart", [50, 80],
                               scale=3,
                               thickness=3,
                               offset=10,
                               colorT=TEXT_COLOR,
                               colorR=TEXTBOX_COLOR)
            # TODO add a GameOver tracking the finger
            cvzone.putTextRect(imgMain,
                               "Game Over",
                               pos=[300, 400],
                               scale=7,
                               thickness=5,
                               offset=20,
                               colorT=TEXT_COLOR,
                               colorR=TEXTBOX_COLOR)
            cvzone.putTextRect(imgMain,
                               f'Your Score: {self.score}',
                               pos=[300, 550],
                               scale=7,
                               thickness=5,
                               offset=20,
                               colorT=TEXT_COLOR,
                               colorR=TEXTBOX_COLOR)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i],
                                 LINE_COLOR, 20)
                cv2.circle(imgMain, self.points[-1], 20, CIRCLE_COLOR,
                           cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(
                imgMain, self.imgFood,
                (rx - self.wFood // 2, ry - self.hFood // 2))

            cvzone.putTextRect(imgMain,
                               f'Score: {self.score}', [50, 80],
                               scale=3,
                               thickness=3,
                               offset=10,
                               colorT=TEXT_COLOR,
                               colorR=TEXTBOX_COLOR)

            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts],
                          False,
                          color=POLYLINE_COLOR,
                          thickness=3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()

        return imgMain


#! NOTE: The image must be semi-transparent. A mask is required for the image.
# * AKA no sqaure images only circle or other shapes

FOOD_IMAGE = "eic.png"

game = SnakeGameClass(FOOD_IMAGE)
# print(game.imgFood is None)

# %%

print('\033[92m' + "The snake game is currently running......" + '\033[0m')
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord(' '):
        game.score = 0
        game.gameOver = False
    elif pressedKey == ord('q'):
        print('\033[92m' + "The Game is quitting......" + '\033[0m')
        break

cap.release()
cv2.destroyAllWindows()