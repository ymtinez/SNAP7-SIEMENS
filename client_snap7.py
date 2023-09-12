# from tkinter import ttk
# from tkinter import *
import time
import random
import snap7


def write_bool(client: snap7.client.Client, db_number: int, start_byte: int, boolean_index: int, bool_value): #Bool 
    data = client.db_read(db_number, start_byte, 1)
    snap7.util.set_bool(data, 0, boolean_index, bool_value)
    client.db_write(db_number, start_byte, data)


def write_byte(client: snap7.client.Client, db_number: int, start_byte: int, byte_value): #Byte 
    data = client.db_read(db_number, start_byte, 1)
    snap7.util.set_byte(data, 0, byte_value)
    client.db_write(db_number, start_byte, data)


def write_int(client: snap7.client.Client, db_number: int, start_byte: int, int_value: int): #Integer 
    data = client.db_read(db_number, start_byte, 2)
    snap7.util.set_int(data, 0, int_value)
    client.db_write(db_number, start_byte, data)  


def write_real(client: snap7.client.Client, db_number: int, start_byte: int, real_value: float): #Real 
    data = client.db_read(db_number, start_byte, 4)
    snap7.util.set_real(data, 0, real_value)
    client.db_write(db_number, start_byte, data)


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
    DB1 = {
        "xStart_PB": False,
        "iCounter": 0,
        "rLevel": 0.0,
        "rTemp": 0.0
    }
    if plc.get_connected():
        print(f"Connected with PLC {IP}")

        plc_info = plc.get_cpu_info()
        print(f"Module Type: {plc_info.ModuleTypeName}")

        state = plc.get_cpu_state()
        print(f"State: {state}")
        # print(db)
        while True:
            db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)
            # TO WRITE VALUES
            DB1["xStart_PB"] = snap7.util.get_bool(db[0:2], 0, 0)
            DB1["iCounter"] = snap7.util.get_int(db[2:4], 0)
            DB1["rLevel"] = round(snap7.util.get_real(db[4:8], 0), 2)
            DB1["rTemp"] = round(snap7.util.get_real(db[8:12], 0), 2)
            print(f"xStartPB: {DB1}")
            write_bool(plc, DB_NUMBER, 0, 0, random.choice([0, 1]))
            write_int(plc, DB_NUMBER, 2, (DB1["iCounter"]+1) if DB1["iCounter"] <= 10000 else 0)
            write_real(plc, DB_NUMBER, 4, round(random.random()*10 + random.randint(30, 60), 2))
            write_real(plc, DB_NUMBER, 8, round(random.random()*10 + random.randint(200, 500), 2))
            time.sleep(3)
    else:
        print("Error during connection")
except Exception as e:
    print('No connection possible - program is terminated:', e)
