#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
sys.path.append("../MFRC522-python/")
import RPi.GPIO as GPIO
import MFRC522
import signal
import requests

GPIO.setwarnings(False)

def get_ID(name):
    URL = "http://10.41.143.40/main.php"
    PARAMS = {'name':name}
    r = requests.get(url = URL, params = PARAMS)
    return r.content

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def write_id(id):
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()

    while True:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            MIFAREReader.MFRC522_SelectTag(uid)

            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            print "\n"

            if status == MIFAREReader.MI_OK:

                data = [int(id[i:i+2], 16) for i in range(0, len(id), 2)]
                for i in range(0, len(data)):
                    if len(str(data[i])) == 1:
                        data[i] = "0" + str(data[i])
                    elif len(str(data[i])) == 0:
                        data[i] = "00"
                print data
                print "Sector 8 looked like this:"
                MIFAREReader.MFRC522_Read(8)
                print "\n"

                MIFAREReader.MFRC522_Write(8, data)

                print "Sector 8 has data written on it now:"
                MIFAREReader.MFRC522_Read(8)

                MIFAREReader.MFRC522_StopCrypto1()
                break
            else:
                print "Authentication error"


if __name__ == "__main__":
    try:
        name = sys.argv[1]
    except:
        print "[*] Usage: python Write.py username"
    id = get_ID(name)
    write_id(id)