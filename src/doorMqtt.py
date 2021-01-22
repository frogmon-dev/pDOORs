#-*- coding:utf-8 -*-

# 중복 실행 방지
from tendo import singleton
try:
    me = singleton.SingleInstance()
except :
    print("another process running!")
    exit()

#프로그램 시작
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json

from frogmon.uCommon  import COM
from frogmon.uGlobal  import GLOB
from frogmon.uRequest import REQUEST
from frogmon.uLogger  import LOG

def DoorOpen():
    led_pin = 21
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, 0)
    time.sleep(1)
    GPIO.output(led_pin, 1)
    GPIO.cleanup(led_pin)

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
GLOB.setUpdateTime()

#from frogmon.ulogger import LOG
configFileNM = COM.gHomeDir+COM.gSetupFile
controlFileNM = COM.gHomeDir+COM.gControlFile

mSvr_addr = GLOB.readConfig(configFileNM, 'MQTT', 'host_addr', 'frogmon.synology.me')
mSvr_port = GLOB.readConfig(configFileNM, 'MQTT', 'host_port', '8359')

user_id   = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id    = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

mSub_nm   = "DIYs/%s/%s" % (user_id, dev_id)

#서버로부터 CONNTACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, flags, rc):
    LOG.writeLn("[MQTT] Connected with result code "+str(rc))
    client.subscribe("%s" % mSub_nm) #구독 "nodemcu"

#서버로부터 publish message를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
    GLOB.setUpdateTime()
    strJson = msg.payload.decode()
    LOG.writeLn("[MQTT] "+ msg.topic+" "+ strJson) #토픽과 메세지를 출력한다.
    try:
        act = GLOB.getJsonVal(strJson, 'door', '99')
        if (act == '1') :
            if GLOB.betweenNow(COM.gLastOpenTime) > 10:
                LOG.writeLn("[MQTT] : Door Open from remote")
                #todo Open the Door 
                DoorOpen()
                jsonAppend(COM.gJsonDir+"device.json", "원격")
                COM.gLastOpenTime = COM.gstrYMDHMS
                REQUEST.updateDIYs(user_id, dev_id)

    except Exception as e :
        LOG.writeLn("[MQTT] : error : %s" % e)

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s' % user_id)
print('**  PRODUCT = %s' % dev_id)
print('**  CHNNEL_ID = %s' % mSub_nm)
print('--------------------------------------------------')
print('')

client = mqtt.Client() #client 오브젝트 생성
client.on_connect = on_connect #콜백설정
client.on_message = on_message #콜백설정

try:
    client.connect(mSvr_addr, int(mSvr_port), 60) #라즈베리파이3 MQTT 브로커에 연결
    client.loop_forever()
except Exception as e :
    LOG.writeLn("[MQTT] : error : %s" % e)
