import serial
import time

ser = serial.Serial("COM10", 9600)
time.sleep(3)
ser.write(b"G")
print("G")
time.sleep(1)
ser.write(b"Y")
print("Y")
time.sleep(1)
ser.write(b"R")
print("R")
time.sleep(1)
ser.close()
