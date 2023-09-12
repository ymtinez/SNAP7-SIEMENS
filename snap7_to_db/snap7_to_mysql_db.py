"""This app allow to read data from speficic database into the OPCUA and send the data to mysql database"""

import os
from datetime import datetime
import time
from dotenv import load_dotenv, find_dotenv
import mysql.connector
import snap7

load_dotenv(find_dotenv())

values = {
        "xStart_PB": False,
        "iCounter": 0,
        "rLevel": 0.0,
        "rTemp": 0.0
    }

IP = "192.168.0.122"
RACK = 0
SLOT = 1

DB_NUMBER = 1
START_ADDRESS = 0
SIZE = 12

plc = snap7.client.Client()

# Connect to PLC:
try:
    plc.connect(IP, RACK, SLOT)
    if plc.get_connected():
        mysql_db = mysql.connector.connect(
                host="192.168.0.99",
                user=os.getenv('MYSQL_USER'),
                passwd=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE'),
            )
        mycursor = mysql_db.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS Data (dataID int PRIMARY KEY AUTO_INCREMENT, xStart_PB boolean NOT NULL, iCounter int NOT NULL, rLevel real NOT NULL, rTemp real NOT NULL, created datetime NOT NULL)")
        print("Connected with MySQL Server")
            
        while True:
            db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
            # TO WRITE VALUES
            values["xStart_PB"] = snap7.util.get_bool(db[0:2], 0, 0)
            values["iCounter"] = snap7.util.get_int(db[2:4], 0)
            values["rLevel"] = round(snap7.util.get_real(db[4:8], 0), 2)
            values["rTemp"] = round(snap7.util.get_real(db[8:12], 0), 2)
            mycursor.execute("INSERT INTO Data (xStart_PB, iCounter, rLevel, rTemp, created) VALUES(%s, %s, %s, %s, %s)", (values["xStart_PB"], values["iCounter"], values["rLevel"], values["rTemp"], datetime.now()))
            mysql_db.commit()
            print(f"Info saved in the database: {values}")
            time.sleep(3)
    else:
        pass
except Exception as e:
    print('No connection possible - program is terminated:', e)