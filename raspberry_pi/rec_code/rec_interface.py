from concurrent.futures import process
from itertools import chain
from time import sleep
from rsa import sign
import serial
import serial.tools.list_ports
import json
import subprocess

class DATA_REC_INTERFACE:

    def __init__(self, time_out=10):
        self.ser_TOUT = time_out
        with open("operator.json", 'r') as f:
            self.ard_port_arr = json.load(f)
        self.refresh_recent_data_json()

    def add_new_serial(self): ## add all new serials to operator
        ard_port_arr_change = False

        for com in serial.tools.list_ports.comports():
            try:
                ard_ser = serial.Serial(com.name, 9600, timeout=self.ser_TOUT)
                ard_output = ard_ser.readline().strip()
            except:
                continue
            
            if ard_output == "": ##serail test
                ard_ser.close()
                continue
            
            try:
                ard_output = json.loads(ard_output) ##serial test
                ard_ser.close()
            except:
                ard_ser.close()
                continue

            if 'type' in ard_output.keys(): ##serail test
                if ard_output['type'] == "PIR":
                    if com.name not in self.ard_port_arr:
                        ard_port_arr_change = True
                        PIR_prmt_str = "python PIR_data_collector.py " + com.name
                        self.start_rec(com.name, PIR_prmt_str)
                elif ard_output['type'] == "TS":
                    if com.name not in self.ard_port_arr:
                        ard_port_arr_change = True
                        PIR_prmt_str = "python touch_sensor_data_collector.py " + com.name
                        self.start_rec(com.name, PIR_prmt_str)
                ## add for all types of arduinos
        if ard_port_arr_change: ## refresh operator if ard_port_dict is changed
            self.refresh_operator()
            self.refresh_recent_data_json()

    def start_rec(self, port: str, prmt_str: str) -> None:
        self.ard_port_arr.append(port)
        subprocess.Popen(prmt_str, shell=False)

    def close_rec(self, port: str)-> None:
        def close_rec_func():
            if port in self.ard_port_arr:
                self.ard_port_arr.remove(port)
                self.refresh_operator()
                self.refresh_recent_data_json()
        return close_rec_func
    
    def close_all_recs(self):
        self.ard_port_arr = []
        self.refresh_operator()
        self.refresh_recent_data_json()

    def refresh_recent_data_json(self):
        with open("recent_data.json", 'r') as f:
            cur_recent_data = json.load(f)
        with open("recent_data.json", 'w') as f:
            if len(self.ard_port_arr) == 0:
                json.dump({} , f)
                return
            else:
                temp_json = {}
                for port in self.ard_port_arr:
                    if port in cur_recent_data.keys():
                        temp_json[port] = cur_recent_data[port]
                    else:
                        temp_json[port] = []
            json.dump(temp_json, f)


    def refresh_operator(self):
        with open("operator.json", 'w') as f:
            json.dump(self.ard_port_arr, f)