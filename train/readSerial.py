import serial
import time
import keyboard
import os

ser = serial.Serial('COM4', 9600, timeout=2)


#ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=2)
ser.reset_input_buffer()
amount = 50
letters = 'Z' # = is a neutral hand position
letters = letters * amount
#letters = 'W'
results = []
count = 0
while(count < len(letters)):
    data = ser.readline()
    print(letters[count])
    print(data)
    #print(ser.in_waiting)
    if keyboard.is_pressed('space'):
        print("got it")
        count +=1
        results.append(data)




print(results)
name = "Jason4"
for i,letter in enumerate(letters):
    data_path = os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letter))
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    with open(os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letter), '{}.csv'.format(name.replace(' ','_'))), 'a', 777) as f:
        f.write(results[i].decode('utf-8'))







#time.sleep(1)
#print(ser.read(ser.in_waiting))
#ser.reset_input_buffer()
#while(True):
    #time.sleep(1)
    #print(ser.read(ser.in_waiting))
    #print("\n")



#time.sleep(6)
#print(ser.read(ser.in_waiting))
#print("\n")
#time.sleep(3)
#print(ser.read(ser.in_waiting))
#print("\n")
#time.sleep(3)
#print(ser.read(ser.in_waiting))
#print("\n")
