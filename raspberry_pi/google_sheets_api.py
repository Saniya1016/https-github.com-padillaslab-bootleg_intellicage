import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime
import serial
import json
import serial.tools.list_ports
import csv

## google api framework
# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# google_api_cred = ServiceAccountCredentials.from_json_keyfile_name("data-collection-326915-f0442e68d43b.json", scope)
# client = gspread.authorize(google_api_cred)
##

##sheets
# env_sheet = client.open("RaspberrySensors").sheet1

##

##Serial
ard_ser = []
for ser in serial.tools.list_ports.comports():
    ard_ser.append(serial.Serial(ser.name, 9600))

##data collection
with open('env_output.csv', 'w', newline='') as env_output:
    env_writer = csv.writer(env_output)
    env_writer.writerow(["ID", "Timestamp", "Humidity", "Temperature", "Light Status"])
    with open('PIR_output.csv', 'w') as PIR_output:
        PIR_writer = csv.writer(PIR_output)
        PIR_writer.writerow(["ID", "Timestamp", "Count 1", "Count 2", "Count 3", "Count 4", "Count 5", "Count 6", "Count 7", "Count 8", "Count 9", "Count 10"])
        with open('HX711_output.csv', 'w') as HX711_output:
            HX711_writer = csv.writer(HX711_output)
            HX711_writer.writerow(["ID", "Timestamp", "Weight 1", "Weight 2", "Weight 3", "Weight 4", "Weight 5", "Weight 6", "Weight 7", "Weight 8", "Weight 9", "Weight 10"])
            with open('HE_output.csv', 'w') as HE_output:
                HE_writer = csv.writer(HE_output)
                HE_writer.writerow(["ID", "Timestamp", "Count 1", "Count 2", "Count 3", "Count 4", "Count 5", "Count 6", "Count 7", "Count 8", "Count 9", "Count 10"])
                while 1:
                    for ard in ard_ser:
                        json_output = json.loads(ard.readline().strip())
                        
                        if(json_output["type"]=="env"):
                            data_arr = [json_output["ID"], datetime.now(), json_output["humidity"], json_output["temperature"], json_output["photo"]]
                            env_writer.writerow(data_arr)

                        if(json_output["type"]=="PIR"):
                            data_arr = [json_output["ID"], datetime.now()]
                            for data in range(10):
                                data_arr.append(json_output['data'][data])
                            PIR_writer.writerow(data_arr) 

                        if(json_output["type"]=="HX711"):
                            data_arr = [json_output["ID"], datetime.now()]
                            for data in json_output['data']:
                                data_arr.append(data)
                            HX711_writer.writerow(data_arr) 
                        
                        if(json_output["type"]=="HE"):
                            data_arr = [json_output["ID"], datetime.now(), json_output["count"]]
                            PIR_writer.writerow(data_arr) 
                
# ard2_ser = serial.Serial('/dev/ttyUSB0', 9600)

# def insert_DHT11_data(date, time, date2, time2):
#     insertRow = [[date, time], [date2, time2]]
#     DHT11_sheet.insert_rows(insertRow, 2)

# i = 0;
# while i<10:
#     ard1_json = json.loads(ard1_ser.readline().strip())
#     ard2_json = json.loads(ard2_ser.readline().strip())
#     insert_DHT11_data(ard1_json['car'], ard1_json['kid'], ard2_json['car2'], ard2_json['kid2'])
#     print("inserted")
