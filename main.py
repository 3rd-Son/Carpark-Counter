import cv2
import numpy as np
import cvzone
import pickle


cap = cv2.VideoCapture("carPark.mp4")

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)
width, height = (158 - 50), (240 - 192)


def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        # cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
        cv2.imshow("Image", img)

        imgCrop = imgPro[y : y + height, x : x + width]
        cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(
            img,
            str(count),
            (x, y + height - 2),
            scale=1,
            thickness=2,
            offset=0,
            colorR=(0, 0, 255),
        )
        if count < 500:
            color = (0, 255, 0)  # BGR
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(
        img,
        f"FREE{str(spaceCounter)}/{len(posList)}",
        (450, 50),
        scale=2,
        thickness=5,
        offset=20,
        colorR=(0, 200, 0),
    )


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
    )

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.zeros((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    # for pos in posList:
    #
    #     x,y = pos

    cv2.imshow("Image", img)
    # cv2.imshow('ImageBlur', imgBlur)
    # cv2.imshow('ImageThreshold', imgThreshold)
    # cv2.imshow('ImageMedian', imgMedian)
    # cv2.imshow('ImageDilate', imgDilate)
    cv2.waitKey(1)
