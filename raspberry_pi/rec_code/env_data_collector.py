from datetime import datetime
import serial
import json
import serial.tools.list_ports
import csv
import sys

port = sys.argv[1]
ard = serial.Serial(port, 9600)

rec_start_time = datetime.now()
json_output = json.loads(ard.readline().strip())
csv_name = 'env_output' ##csv name
csv_name += '_' + str(rec_start_time.year) + '_' + str(rec_start_time.month) + '_' + str(rec_start_time.day) + '_' + str(rec_start_time.hour) + '_' + str(rec_start_time.minute) ##dating csv file
csv_name += '.csv'

run = True

def check_operator():
    operator_file = open('operator.json')
    operator = json.load(operator_file)
    operator_file.close()
    if port not in operator:
        return False

##main
with open(csv_name, 'w') as env_output:
        env_writer = csv.writer(env_output)
        env_writer.writerow(["ID", "Timestamp", "Count 1", "Count 2", "Count 3", "Count 4", "Count 5", "Count 6", "Count 7", "Count 8", "Count 9", "Count 10"])
        
        while run:
            json_output = json.loads(ard.readline().strip())
            data_arr = [json_output["ID"], datetime.now(), json_output["humidity"], json_output["temperature"], json_output["photo"]]
            env_writer.writerow(data_arr)

            run = check_operator()