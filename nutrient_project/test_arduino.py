import serial, time

ser = serial.Serial("COM3", 9600)
time.sleep(2)

ser.write(b"1")   # Green
time.sleep(1)
ser.write(b"2")   # Yellow
time.sleep(1)
ser.write(b"3")   # Red
time.sleep(1)
ser.write(b"0")   # All off

ser.close()
print("Done")