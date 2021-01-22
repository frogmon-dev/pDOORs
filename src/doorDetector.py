# -*- coding: utf-8 -*- 

# 중복 실행 방지
from tendo import singleton
try:
	me = singleton.SingleInstance()
except :
	print("another process running!")
	exit()

import face_recognition
import cv2
#import numpy as np
#import platform
import os
import json
import RPi.GPIO as GPIO
import time

from frogmon.uCommon import COM
from frogmon.uLogger import LOG
from frogmon.uGlobal import GLOB

def DoorOpen():
    door_pin = 21
    GPIO.setup(door_pin, GPIO.OUT)
    GPIO.output(door_pin, 0)
    time.sleep(1)
    GPIO.output(door_pin, 1)
    GPIO.cleanup(door_pin)

def jsonAppend(fileNM, name):
    rc = -1
    try :
        if GLOB.fileExist(fileNM):
            with open(fileNM, 'a', encoding='utf-8') as f:
                data = ', {"DOOR_OPEN_TIME" : "%s", "NAME" : "%s" }' % (COM.gstrYMDHMS, name)
                f.write(data)

        else:
            with open(fileNM, 'w', encoding='utf-8') as f:
                data = '{"DOOR_OPEN_TIME" : "%s", "NAME" : "%s" }' % (COM.gstrYMDHMS, name)
                f.write(data)
        rc = 0
    except Exception as e :
        LOG.writeLn("[jsonAppend ERROR]: %s" % e)
    return rc     

# 프로그램 시작
GLOB.directoryInit('pi', "DOORs")

path = COM.gHomeDir + "faces/"
faceLogPath = COM.gHomeDir + "facelog/"
metrixImg = COM.gHomeDir + "metrix.png"


GLOB.folderMaker(path)
GLOB.folderMaker(faceLogPath)
GLOB.folderMaker(COM.gJsonDir)

#from frogmon.ulogger import LOG
configFileNM  = COM.gHomeDir+COM.gSetupFile
controlFileNM = COM.gHomeDir+COM.gControlFile
user_id       = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id        = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

file_list = os.listdir(path)

known_face_names = []
known_face_encodings = []

for i in file_list:
    known_face_names.append(os.path.splitext(i)[0])
    face_image = face_recognition.load_image_file(path+i)
    known_face_encodings.append(face_recognition.face_encodings(face_image)[0])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Delete json logs
if GLOB.fileExist(COM.gJsonDir+"device.json") :
    os.remove(COM.gJsonDir+"device.json")

led_pin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

mLstImgFileSize = 1
aMin = 601

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print("**  face      path check : %s" % path)
print("**  faceLog   Path check : %s" % faceLogPath)
print("**  metrixImg path check : %s" % metrixImg)
print(file_list)
print('--------------------------------------------------')
print('')

timer = 0

LOG.writeLn("[doorDetector] process run")
while True:
    time.sleep(0.1)
    if GLOB.fileExist(metrixImg):
        timer = timer + 1
        if timer > 600 :
            LOG.writeLn("[doorDetector] Alive Check (%d)" % mLstImgFileSize)
            timer = 0
            
        curntImgFileSize = os.path.getsize(metrixImg)
        if (curntImgFileSize > 0) and (mLstImgFileSize != curntImgFileSize):
            mLstImgFileSize = curntImgFileSize
            GLOB.setUpdateTime()
            GPIO.output(led_pin, 0)
            try:
                detectFace = 0
                rgb_small_frame = face_recognition.load_image_file(metrixImg)
                face_locations = face_recognition.face_locations(rgb_small_frame)
                if face_locations:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)                   
                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.4)
                        name = "Unknown"
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                            face_names.append(name)
                            detectFace = 1
                            break
                    if detectFace == 1:
                        for (top, right, bottom, left), name in zip(face_locations, face_names):

                            x = left
                            y = top
                            w = right-left
                            h = bottom-top

                            detectFace = rgb_small_frame[y:y+h, x:x+w].copy()
                            cv2.imwrite("%s%s_%s.png" % (faceLogPath, COM.gstrYMDHMS, name), detectFace)
                            jsonAppend(COM.gJsonDir+"device.json", name)
                            LOG.writeLn("Door Open with %s" % name)      
                            #todo Open Door and Send status to server
                            DoorOpen()
                            time.sleep(1)
                            GPIO.output(led_pin, 0)
                            time.sleep(1)
                            GPIO.output(led_pin, 1)
                            time.sleep(1)
                    else :
                        LOG.writeLn("[doorDetector] Unknown face Detected")
                        detectFace = rgb_small_frame[y:y+h, x:x+w].copy()
                        cv2.imwrite("%s%s_unknown.png" % (faceLogPath, COM.gstrYMDHMS), detectFace)
                        GPIO.output(led_pin, 0)
                        time.sleep(0.1)
                        GPIO.output(led_pin, 1)
            except Exception as e :
                LOG.writeLn("[doorDetector]: %s" % e)
        #else:
            #LOG.writeLn("[doorDetector] file size error (%d/%d)" % (curntImgFileSize, mLstImgFileSize))


# Release handle to the webcam
GPIO.cleanup(led_pin)
cv2.destroyAllWindows()