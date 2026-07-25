#!/usr/bin/env python3

import sys

import mysql.connector

try:
    connection = mysql.connector.connect(
        host='mysql-dj-alustudent-dj.i.aivencloud.com',
        port=16865,
        user='avnadmin',
        password='AVNS_HmRG-kI36oO_dv4ELa-',
        database='defaultdb',
        ssl_disabled=False
    )
except mysql.connector.Error as e:
    print("Error: could not connect to the TranzGo database.")
    print(f"    {e}")
    sys.exit(1)

