#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
import time
import sys
import pypyodbc
sys.path.append("../MFRC522-python/")
import RPi.GPIO as GPIO
import MFRC522
import signal
import MySQLdb

pwd = "root"
user = "root"
port = 80
host = "localhost"
continue_reading = True

def send_id(id, host, port, user, pwd):
    db = MySQLdb.connect(host=host,port=port,user=user,passwd=pwd)
    cursor=db.cursor()
    cursor.execute("SELECT name FROM coreData WHERE id={}".format(id))
    results=cursor.fetchall()
    if len(results) == 0: return -1
    for result in results:
        print row
    return 1

def light_green():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(12,GPIO.LOW)

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
                    int_data.append(str(hex(data[i]))[2:])
                id = "".join(int_data)
                #send_id(id, host, port, user, pwd)
                #if send_id == 1:
                light_green()
                #   time.sleep(8)
                #else:
                #   light_red()
                #   time.sleep(2)
            else:
                print "Authentication error"
                time.sleep(2)
            print "\n---------------------\n"

if __name__ == "__main__":
    #read()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(18,GPIO.LOW)
