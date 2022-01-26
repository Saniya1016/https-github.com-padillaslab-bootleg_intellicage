import serial
import serial.tools.list_ports
import json

ard_ser = []
ard_port = []
for ser in serial.tools.list_ports.comports():
    ard_ser.append(serial.Serial(ser.name, 9600))
    ard_port.append(ser.name)