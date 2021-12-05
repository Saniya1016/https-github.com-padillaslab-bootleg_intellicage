import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime
import serial
import json

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

i = 0;
while i<10:
    ard1_json = json.loads(ard1_ser.readline().strip())
    ard2_json = json.loads(ard2_ser.readline().strip())
    insert_DHT11_data(ard1_json['car'], ard1_json['kid'], ard2_json['car2'], ard2_json['kid2'])
    print("inserted")
