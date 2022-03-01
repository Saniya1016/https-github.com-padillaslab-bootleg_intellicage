import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime
import serial
import json
import time
import csv

## google api framework
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
google_api_cred = ServiceAccountCredentials.from_json_keyfile_name("data-collection-326915-f0442e68d43b.json", scope)
client = gspread.authorize(google_api_cred)
##

##sheets
DHT11_sheet = client.open("RaspberrySensors").sheet1
##

##Serial
ard1_ser = serial.Serial('/dev/ttyACM0', 9600)
ard2_ser = serial.Serial('/dev/ttyUSB0', 9600)

def insert_DHT11_data(date, time, date2, time2):
    insertRow = [[date, time], [date2, time2]]
    DHT11_sheet.insert_rows(insertRow, 2)

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ["Timestamp", "Cage Number", "Photo", "PIR 0 Count", "PIR 1 Count", "Hall Effect Count", "Scale 0", "Scale 1"]
    writer.writerow(header)
    DHT11_sheet.insert_row(header)
    i= 0
    while i<10:
        ard1_json = json.loads(ard1_ser.readline().strip())
        ard2_json = json.loads(ard2_ser.readline().strip())
        ard1_data = [datetime.now(), 1, ard1_json["photo_sensor"], ard1_json["PIR_0_count"], ard1_json["PIR_1_count"], ard1_json["HE_0_count"], ard1_json["scale_0"], ard1_json["scale_1"]]
        ard2_data = [datetime.now(), 2, ard2_json["photo_sensor"], ard2_json["PIR_0_count"], ard2_json["PIR_1_count"], ard2_json["HE_0_count"], ard2_json["scale_0"], ard2_json["scale_1"]]
        DHT11_sheet.insert_rows([ard1_data, ard2_data], 2)

