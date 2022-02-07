from tracemalloc import start
from rec_interface import DATA_REC_INTERFACE as recorder
import tkinter as tk


rec = recorder() ## start recorder
UI_wdw = tk.Tk() ##initiate UI

start_button = tk.Button(UI_wdw, text="Start Rec", width=25, command=rec.add_new_serial)
start_button.pack()
stop_button = tk.Button(UI_wdw, text="Stop Rec", width=25, command=rec.close_all_recs)
stop_button.pack()

UI_wdw.mainloop()