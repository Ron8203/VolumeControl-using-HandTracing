import cv2
import mediapipe as mp
import time
import HandtrackingModule as htm
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)  # used to run a webcam
detector = htm.handDetector()
while True:  # used to run a webcam
    success, img = cap.read()  # used to run a webcam
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[0])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow("Image", img)  # used to run a webcam
    cv2.waitKey(1)  # used to run a webcam