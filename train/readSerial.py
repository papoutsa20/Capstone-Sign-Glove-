import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1432301', 9600, timeout=1)

time.sleep(1)
print(ser.read(ser.in_waiting))
ser.reset_input_buffer()
#while(True):
    #time.sleep(1)
    #print(ser.read(ser.in_waiting))
    #print("\n")



time.sleep(6)
print(ser.read(ser.in_waiting))
print("\n")
time.sleep(3)
print(ser.read(ser.in_waiting))
print("\n")
time.sleep(3)
print(ser.read(ser.in_waiting))
print("\n")
