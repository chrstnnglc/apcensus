# -*- coding: utf-8 -*-
import sqlite3
import os.path

def startconn(filename):
    global conn
    global cur
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("CREATE TABLE test (DATETIME CHAR, MAC CHAR, RSSI CHAR, LATITUDE CHAR, LONGITUDE CHAR)")
    conn.commit()

def endconn():
    conn.close()

def saveData(line):
    global conn
    global cur
    datetime = line.split(">>")[0]
    mac = line.split("---")[0].split(">>")[1]
    mac = mac.upper();
    rssi = line.split("---")[1].split("@")[0]

    if "@" not in line:
        latitude = "NULL"
        longitude = "NULL"
    else: 
        latitude = line.split("@")[1].split(",")[0]
        longitude = line.split("@")[1].split(",")[1].split(" ")[0]

    cur.execute("INSERT INTO test VALUES (?, ?, ?, ?, ?)", (datetime, mac, rssi, latitude, longitude))
    conn.commit()
