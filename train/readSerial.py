import serial
ser = serial.Serial('COM4', 9600, timeout=1)
while(True):
    print(ser.readline())
