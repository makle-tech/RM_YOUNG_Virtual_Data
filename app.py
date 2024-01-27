from flask import Flask, render_template
from threading import Thread
import serial
import datetime
import time
import os

app = Flask(__name__)

# Replace with your serial port and baud rate
serial_port = 'COM3'
baud_rate = 9600

# Global variable to store the latest data
latest_data = ""

def read_serial_data():
    global latest_data
    try:
        ser = serial.Serial(serial_port, baud_rate)
        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if line:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                latest_data = f"{timestamp}: {line}"
    except serial.SerialException:
        print(f"Unable to open serial port {serial_port}")

# Start the thread that reads serial data
serial_thread = Thread(target=read_serial_data, daemon=True)
serial_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return latest_data

if __name__ == '__main__':
    app.run(debug=True)
