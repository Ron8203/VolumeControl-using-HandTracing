import cv2
import time
import img as img
import numpy as np
import HandtrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################
wCam, hCam = 640,480
######################


cap =cv2.VideoCapture(0)
cap.set(4, wCam)
cap.set(5, hCam)
cTime = 0
pTime = 0

detector= htm.handDetector(detectionCon= 0.7, trackCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0] #These are our ranges
maxVol = volRange[1]
vol = 0
volbar = 400
volPer = 0


while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
     # print(lmlist[4], lmlist[8])

     #Filter by hand size
     # Reduce resolution to make smoother
     # Check fingers up
     # If pinky is down set the volume



     x1, y1 = lmlist[4][1], lmlist[4][2]
     x2, y2 = lmlist[8][1], lmlist[8][2]
     c1, c2 = (x1+x2)//2, (y1+y2)//2

     cv2.circle(img, (x1, y1), 8, (0, 0, 255), cv2.FILLED)
     cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED)
     cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 3)
     cv2.circle(img, (c1,c2), 8, (0,0,255), cv2.FILLED)

     length = math.hypot(x2-x1, y2-y1)
     print(length)

     # Hand range was 15-150
     #volume Range -63.5 - 0
     #We need to convert Hand range to volume for that we use numpy

     vol = np.interp(length, [15, 148], [minVol,maxVol])
     volbar = np.interp(length, [15, 148], [400, 150])
     volPer = np.interp(length, [15, 148] , [0, 100])
     print(vol)
     volume.SetMasterVolumeLevel(vol, None)

     if length < 17:
        cv2.circle(img, (c1, c2), 8, (0, 255, 0), cv2.FILLED)

     cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
     cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
     cv2.putText(img, f'{int(volPer)}%', (40,450), cv2.FONT_ITALIC,
                 1, (255,250,0), 3)


    cTime= time.time()
    fps=1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (50,70), cv2.FONT_ITALIC, 1, (255,0,0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)