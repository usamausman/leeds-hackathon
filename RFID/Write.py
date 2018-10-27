#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import pypyodbc
sys.path.append("../MFRC522-python/")
import RPi.GPIO as GPIO
import MFRC522
import signal

GPIO.setwarnings(False)

def get_ID(name):
    server = "localhost"
    database = "test"
    pwd = "1"
    table = "tablename"

    query = "Driver={{SQL Server}};Server={};Database={};uid=sa;pwd={}".format(server, database, pwd)

    connection = pypyodbc.connect(query)
    cursor = connection.cursor()
    command = "SELECT id FROM {} WHERE name={}".format(table,name)
    cursor.execute(command)
    results = cursor.fetchone()
    connection.close()

    return results[0]

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

                hex_data = hex(id)[2:-1]

                data = [int(hex_data[i:i+2],16) for i in range(0, len(hex_data), 2)]

                print "Sector 8 looked like this:"
                MIFAREReader.MFRC522_Read(8)
                print "\n"

                MIFAREReader.MFRC522_Write(8, data)

                print "Sector 8 has data written on it now:"
                MIFAREReader.MFRC522_Read(8)
                print "\n"

                MIFAREReader.MFRC522_StopCrypto1()
                break
            else:
                print "Authentication error"


if __name__ == "__main__":
    try:
        name = sys.argv[1]
    except:
        print "[*] Usage: python Write.py username"
        sys.exit(1)
    id = get_ID(name)
    write_id(id)
