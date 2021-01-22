# -*- coding: utf-8 -*- 

# 중복 실행 방지
from tendo import singleton
try:
	me = singleton.SingleInstance()
except :
	print("another process running!")
	exit()

from picamera import PiCamera
from time import sleep

from frogmon.uCommon import COM
from frogmon.uLogger import LOG
from frogmon.uGlobal import GLOB

GLOB.directoryInit('pi', "DOORs")
metrixImg = COM.gHomeDir + "metrix.png"

camera = PiCamera()
camera.resolution = (320, 180)
camera.rotation = 180

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  Image File = %s' % metrixImg)
print('--------------------------------------------------')
print('')

LOG.writeLn("[doorImage] process run")
while True:
    try:
        camera.start_preview()
        sleep(0.5)
        camera.capture(metrixImg)
        #LOG.writeLn("[doorImage] get picture")
        camera.stop_preview()
    except Exception as e :
        LOG.writeLn("[doorImage] Error : %s" % e)

