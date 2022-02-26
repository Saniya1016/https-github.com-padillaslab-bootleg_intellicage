from datetime import datetime
from tabnanny import check
from xmlrpc.client import Boolean
import serial
import json
import serial.tools.list_ports
import csv
import sys

##ard serialization
port = sys.argv[1]
ard = serial.Serial(port, 9600)

rec_start_time = datetime.now()

#json file name
json_output = json.loads(ard.readline().strip())
csv_name = '../rec_data/touch_sensor_output' ##csv name
csv_name += '_' + str(json_output['ID']) + '_' + str(rec_start_time.year) + '_' + str(rec_start_time.month) + '_' + str(rec_start_time.day) + '_' + str(rec_start_time.hour) + '_' + str(rec_start_time.minute) ##dating csv file
csv_name += '.csv'

## checks operator json
def check_operator() -> Boolean:
    operator_file = open('operator.json')
    operator = json.load(operator_file)
    operator_file.close()
    if port not in operator:
        return False
    return True

with open(csv_name, 'w', newline='') as touch_sensor_output:
        ##writer
        touch_sensor_writer = csv.writer(touch_sensor_output)
        touch_sensor_writer.writerow(["ID", "Timestamp", "Count 1", "Count 2", "Count 3", "Count 4", "Count 5", "Count 6", "Count 7", "Count 8", "Count 9", "Count 10"])
        
        run = True
        while run:
            ## load data
            json_output = json.loads(ard.readline().strip())

            ##write data onto CSV
            data_arr = [json_output['ID'], datetime.now()]
            for data in json_output['data']:
                data_arr.append(data)
            touch_sensor_writer.writerow(data_arr)

            ##write data onto recent data
            with open('recent_data.json', 'r') as f:
                temp_data = json.load(f) 
            temp_data[port] = data_arr[2:12] ## add data
            temp_data[port].insert(0, "TS " + str(data_arr[0])) ## add name of touch_sensor
            with open('recent_data.json', 'w') as f:
                json.dump(temp_data, f)

            ##check operator json
            run = check_operator()
        
        ard.close()