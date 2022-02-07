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
        self.ard_port_arr = []
        self.refresh_operator()

    def add_new_serial(self): ## add all new serials to operator
        ard_port_arr_change = False

        for com in serial.tools.list_ports.comports():
            ard_ser = serial.Serial(com.name, 9600, timeout=self.ser_TOUT)
            ard_output = ard_ser.readline().strip()
            
            if ard_output == "": ##serail test
                continue
            
            try:
                ard_output = json.loads(ard_output) ##serial test
                ard_ser.close()
            except:
                ard_ser.close()
                continue

            if 'type' in ard_output.keys(): ##serail test
                if ard_output['type'] == "PIR":
                    PIR_prmt_str = "python PIR_data_collector.py " + com.name
                    if com.name not in self.ard_port_arr:
                        ard_port_arr_change = True
                        self.start_rec(com.name, PIR_prmt_str)
                ## add for all types of arduinos
                ard_ser.close()
            else:
                ard_ser.close()
                continue
        if ard_port_arr_change: ## refresh operator if ard_port_dict is changed
            self.refresh_operator()

    def start_rec(self, port: str, prmt_str: str) -> None:
        self.ard_port_arr.append(port)
        subprocess.Popen(prmt_str, shell=False)

    def close_rec(self, port: str)-> None:
        if port in self.ard_port_arr:
            self.ard_port_arr.remove(port)
            self.refresh_operator()
    
    def close_all_recs(self):
        self.ard_port_arr = []
        self.refresh_operator()

    def refresh_operator(self):
        with open("operator.json", 'w') as oper:
            json.dump(self.ard_port_arr, oper)