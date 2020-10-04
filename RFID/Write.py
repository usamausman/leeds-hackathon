#!/usr/bin/env python
# -*- coding: utf8 -*-

import MFRC522
import RPi.GPIO as GPIO

import requests
import signal
import sys

sys.path.append("../MFRC522-python/")

GPIO.setwarnings(False)


def get_ID(name):
    url = "http://10.41.143.40/main.php"
    r = requests.get(url=url, params={'name': name})
    return r.content


def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


def write_id(id):
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()

    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print "Card detected"

        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:

            print "Card read UID: %s,%s,%s,%s\n" % (uid[0], uid[1], uid[2], uid[3])

            key = [0xFF for i in range(6)]
            MIFAREReader.MFRC522_SelectTag(uid)
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            if status == MIFAREReader.MI_OK:

                data = [int(id[i:i + 2], 16) for i in range(0, len(id), 2)]

                for i in range(0, len(data)):
                    if len(str(data[i])):
                        data[i] = "0" + str(data[i])
                    else:
                        data[i] = "00"

                print "Sector 8 looked like this:"
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_Write(8, data)

                print "\nSector 8 has data written on it now:"
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                break
            else:
                print "Authentication error"


if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "[*] Usage: python Write.py username"

    id = get_ID(name)
    write_id(id)
