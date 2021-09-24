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
wCam, hCam = 640, 480
######################


cap = cv2.VideoCapture(0)
cap.set(4, wCam)
cap.set(5, hCam)
cTime = 0
pTime = 0

detector= htm.handDetector(detectionCon= 0.7, trackCon=0.7, maxHands=1)
# We use maxhand=1 for removing the flickering



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
area = 0

while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=True)
    if len(lmlist) != 0:
     # print(lmlist[4], lmlist[8])

     #Filter by hand size
     wB,hB = bbox[2]-bbox[0], bbox[3]-bbox[1]
     area = (wB*hB)//100
     # print(area)
    if 200<area<700:
         # Find distance between fingre and thumb
          length, img, lineinfo =detector.findDistance(4, 8, img)
          # print(length)



          # Hand range was 15-150
          #volume Range -63.5 - 0
          #We need to convert Hand range to volume for that we use numpy

          #Convert Volume

          volbar = np.interp(length, [35, 170], [400, 150])
          volPer = np.interp(length, [35, 170] , [0, 100])
          #Reduce resoltion to make it smother
          smoothness = 10
          volPer = smoothness*round(volPer/smoothness) #Now our volume will be incremented by 10

          # Check fingers up

          fingers = detector.fingersUp()
          print(fingers)

         # If pinky is down set the volume

          if not fingers[4]:
             volume.SetMasterVolumeLevelScalar(volPer / 100, None)
             cv2.circle(img, (lineinfo[4], lineinfo[5]), 8, (0, 255, 0), cv2.FILLED)



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