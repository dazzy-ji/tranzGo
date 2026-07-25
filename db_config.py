#!/usr/bin/env python3

import sys

import mysql.connector

try:
    connection = mysql.connector.connect(
        host='',
        port=,
        user='',
        password='',
        database='',
        ssl_disabled=
    )
except mysql.connector.Error as e:
    print("Error: could not connect to the TranzGo database.")
    print(f"    {e}")
    sys.exit(1)

