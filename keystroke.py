import json
import os
import time
from datetime import datetime
from threading import Thread
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox
# DO NOT USE for unethical purposes. 
LOG_FILE = "logs.json"
logging_active = False
listener = None
# stored as Json
def write_log(key):
    log_entry = {
        "key": str(key),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)
# listener onpress
def on_press(key):
    if logging_active:
        try:
            write_log(key.char)
        except AttributeError:
            write_log(key)
def start_logging():
    global logging_active, listener
    if not logging_active:
        consent = messagebox.askyesno(
            "Consent Required",
            "Do you agree to start logging your keyboard inputs for educational purposes?")
        if not consent:
            return
        logging_active = True
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        status_label.config(text="Status: ON", fg="green")
def stop_logging():
    global logging_active, listener
    if logging_active:
        logging_active = False
        if listener:
            listener.stop()
        status_label.config(text="Status: OFF", fg="red")
        path_label.config(text=f"Logs stored at: {os.path.abspath(LOG_FILE)}")
# tkinter based ui
root = tk.Tk()
root.title("Input Logger (Educational Use)")
root.geometry("400x200")
title = tk.Label(root, text="Input Logger", font=("Arial", 15)) 
title.pack(pady=10)
status_label = tk.Label(root, text="Status: OFF", fg="red")
status_label.pack()
start_btn = tk.Button(root, text="Start Logging", command=start_logging)
start_btn.pack(pady=5)
stop_btn = tk.Button(root, text="Stop Logging", command=stop_logging)
stop_btn.pack(pady=5)
path_label = tk.Label(root, text="")
path_label.pack(pady=10)
root.mainloop() # HAH 67
