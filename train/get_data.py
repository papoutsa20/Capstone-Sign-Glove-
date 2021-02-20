from tkinter import ttk
import tkinter as tk
import random
import os
import serial
import subprocess
import keyboard
import time

def run_collection(name, num_times, letters_to_sign):
    port_name = '/dev/cu.usbmodem1432301'#changed by Spencer for arduino port
    ser = serial.Serial(port_name, 9600, timeout=1)
    size = len(letters_to_sign)

    # change this variable if display doesn't work on windows
    img_opening_program = 'open'    #changed by Spencer for Mac

    # add additional letters to list if repeats is greater than 1
    for letter_index in range(size):
        letters_to_sign += [letters_to_sign[letter_index]]*(num_times-1)
        data_path = os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letters_to_sign[letter_index]))

        # if dir doesn't exist, create it
        if not os.path.exists(data_path):
            os.makedirs(data_path)

    random.shuffle(letters_to_sign)
    count = 0

    print(letters_to_sign)
    # start the collection
    for letter in letters_to_sign:
        #displaying image to user using 'display' linux call, may need to change for windows
        p = subprocess.Popen([img_opening_program,os.path.join(os.path.dirname(__file__), 'data_collection_img', '{}.jpg'.format(letter))], stdout=subprocess.PIPE, preexec_fn=os.setsid)

        # wait for enter to be pressed
        while True:
            if keyboard.is_pressed('space'):
                break

        # store data from ardunio
        ser.reset_output_buffer()
        try:
            data = ser.readline()
        except ArduinoConnectError:
            print("Arduino fucked up")

        while(keyboard.is_pressed('space')):
             pass
        p.kill()
        #os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups
        #p2 = subprocess.Popen(["pkill", "-P", '{}'.format(p.pid)])
        #os.kill(p.pid, 9)
        count+=1
        print(count)

        with open(os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letter), '{}.csv'.format(name.replace(' ','_'))), 'a', 777) as f:
            f.write(data.decode("utf-8"))

def init_collection():
    # functions to select and deselect check boxes
    def select_all():
        for i in letters_to_sign:
            i.set(1)

    def deselect_all():
        for i in letters_to_sign:
            i.set(0)
    def start_collecting_func():
        nonlocal start_collecting
        start_collecting = True
        window.destroy()


    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters_to_sign = []
    start_collecting = False

    # build window
    window = tk.Tk()
    window.title('Data collection')

    # create name input
    label = ttk.Label(window, text='Name:')
    label.grid(column=0,row=0)
    name = tk.StringVar()
    nameEntered = ttk.Entry(window, textvariable = name)
    nameEntered.grid(column = 0, row = 1, pady=(10,10), padx=(5,5))

    # create check boxes
    for i,letter in enumerate(letters):
         letter_var = tk.IntVar()
         letter_var.set(1)
         check_box = ttk.Checkbutton(window, text=letter, variable=letter_var)
         if i % 2 == 0:
            check_box.grid(column=0, row = 2 + i, sticky='W')
         else:
            check_box.grid(column=1, row = 1 + i, sticky='W')
         letters_to_sign.append(letter_var)

    # select and deselect all button
    button = ttk.Button(window, text = "Deselect All", command = deselect_all)
    button.grid(column= 0, row = 29, padx=(10,5), pady=(20,20), sticky='W')
    button = ttk.Button(window, text = "Select All", command = select_all)
    button.grid(column= 1, row = 29, padx=(5,10), pady=(20,20), sticky='E')
    # number of times input
    label = ttk.Label(window, text='# of repeats:')
    label.grid(column=0,row=30, sticky='W')
    num_times = tk.IntVar(value=1)
    num_entered = ttk.Entry(window, textvariable = num_times)
    num_entered.grid(column = 1, row = 30, pady=(10,10), padx=(5,5), sticky='W')
    # button to start data collection
    button = ttk.Button(window, text = "Start!", command = start_collecting_func)
    button.grid(column= 0, row = 31, pady=(20,20))

    window.mainloop()
    if start_collecting:
        return name.get(), num_times.get(), [letters[i] for i,x in enumerate(letters_to_sign) if x.get()]
    else:
        return None, None, None

if __name__ == '__main__':
    name, num_times, letters_to_sign = init_collection()
    if name and num_times and letters_to_sign:
        run_collection(name, num_times, letters_to_sign)
