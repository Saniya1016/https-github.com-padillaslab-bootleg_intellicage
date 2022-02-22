from ctypes import alignment
from distutils import command
from tracemalloc import start
from turtle import back, left, width

from matplotlib.font_manager import json_load
from numpy import pad
from rec_interface import DATA_REC_INTERFACE as recorder
from tkinter import *
import json


rec = recorder() ## start recorder
UI_wdw = Tk() ##initiate UI
UI_wdw['background']='black'
UI_wdw.geometry("1300x700")

## Action Bar
action_bar = Frame(UI_wdw, background='black', width=1024)
action_bar.grid(row=0, column=0)
## start button
start_button = Button(action_bar, text="Start Rec", width=25, command=rec.add_new_serial, background='white')
start_button.grid(row=0, column=0,padx=13, pady=10)

## stop button
stop_button = Button(action_bar, text="Stop Rec", width=25, command=rec.close_all_recs, background='white')
stop_button.grid(row=0, column=1, padx=13, pady=10)

## Arduino table
ARD_TBL_LEN = 10
ARD_TBL_WIDTH = 12

arduino_table = Frame(UI_wdw, background="black")
arduino_table.grid(row=1, column=0)

##create and grid labels and buttons
rows = []
for row_num in range(ARD_TBL_LEN):
    row = []
    for col_num in range(ARD_TBL_WIDTH):
        if col_num == ARD_TBL_WIDTH-1:
            stop_button = Button(arduino_table, width=12, text="Stop", background='white')
            stop_button.grid(row=row_num, column=11, padx=5, pady=5)
            row.append(stop_button)
        else:
            label = Label(arduino_table, width=12)
            if col_num == 0:
                label['background'] = 'yellow'
            else:
                label['background'] = 'white'
            row.append(label)
            label.grid(row=row_num, column=col_num, padx=5, pady=5)
    rows.append(row)

## updates information and button controls in arduino table
def upd_ard_win():
    with open("operator.json", 'r') as f:
        operator = json.load(f)
    with open("recent_data.json", 'r') as f:
        recent_data = json.load(f)
    for i in range(len(operator)):
        if operator[i] not in recent_data.keys():
            continue
        if recent_data[operator[i]] == []:
            continue
        for j in range(12):
            if j==11:
                rows[i][j]['text'] = "Stop " + recent_data[operator[i]][0]
                rows[i][j]['command'] = rec.close_rec(operator[i])
                continue
            elif j < len(recent_data[operator[i]]):
                rows[i][j]['text'] = recent_data[operator[i]][j]
            else:
                rows[i][j]['text'] = ""
    
    if len(operator) != 10:
        for i in range(len(operator), 10):
            for j in range(12):
                if j==11:
                    rows[i][j]['text'] = "Stop"
                    rows[i][j]['command'] = None
                    continue
                rows[i][j]['text'] = ""
        
    UI_wdw.after(1000, upd_ard_win)

UI_wdw.after(1000, upd_ard_win())
UI_wdw.mainloop()