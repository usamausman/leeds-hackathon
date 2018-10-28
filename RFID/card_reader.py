#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
import time
import sys
sys.path.append("../MFRC522-python/")
import RPi.GPIO as GPIO
import MFRC522
import signal
import requests

continue_reading = True

GPIO.setwarnings(False)

def get_name(id):
    URL = "http://10.41.143.40/main.php"
    PARAMS = {'id':id}
    r = requests.get(url = URL, params = PARAMS)
    print r.content
    if r.content != "0":
        return 1
    return 0

def light(val = 1):
    pin = 12
    if val!=1:
	       pin = 16
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def read():
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()

    print "\n"

    while continue_reading:

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print "Card detected"

        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:

            print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            MIFAREReader.MFRC522_SelectTag(uid)

            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            if status == MIFAREReader.MI_OK:
                data = MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                int_data = []
                for i in range(0, len(data)):
                    int_data.append(str(format(data[i], '02x')))
                    print len(int_data[i])
                    if len(int_data[i]) == 1:
                        print "AAAA ---- ","0" + str(data[i])
                        data[i] = "0" + str(data[i])
                    elif len(int_data[i]) == 0:
                        data[i] = "00"
                print int_data
                id = "".join(int_data)
                print id
                name_found = get_name(id)
                if name_found == 1:
                    light(0)
                    time.sleep(2)
                else:
                   light(1)
                   time.sleep(2)
            else:
                print "Authentication error"
                time.sleep(2)
            print "\n---------------------\n"

if __name__ == "__main__":
    read()