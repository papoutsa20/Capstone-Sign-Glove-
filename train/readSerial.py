import serial
ser = serial.Serial('/dev/cu.usbmodem1432301', 9600, timeout=1)
while(True):
    print(ser.readline())
