from datetime import datetime
import serial
import json
import serial.tools.list_ports
import csv
import sys

ard = serial.Serial(sys.argv[1], 9600)

rec_start_time = datetime.now()
csv_name = 'weight_output' ##csv name
csv_name += '_' + str(rec_start_time.year) + '_' + str(rec_start_time.month) + '_' + str(rec_start_time.day) + '_' + str(rec_start_time.hour) + '_' + str(rec_start_time.minute) ##dating csv file
csv_name += '.csv'

with open(csv_name, 'w') as weight_output:
        weight_writer = csv.writer(weight_output)
        weight_writer.writerow(["ID", "Timestamp", "Weight 1", "Weight 2", "Weight 3", "Weight 4", "Weight 5", "Weight 6", "Weight 7", "Weight 8", "Weight 9", "Weight 10"])
        while 1:
            json_output = json.loads(ard.readline().strip())

            data_arr = [json_output["ID"], datetime.now()]
            for data in json_output['data']:
                data_arr.append(data)
            weight_writer.writerow(data_arr) 