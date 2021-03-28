"""
Graphs the normailized resister sensor values on a graph
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# use colors for letters here
colors = {
        'K': 'g',
        'V': 'red'
}

# letters to graph
letters = ['K','V']


x = np.arange(8)
y = {}
for letter in letters: 
    y[letter] = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
    for file in os.listdir(os.path.join('./data', letter)):
        if os.path.isfile(os.path.join('./data', letter,file)) and file[-4:] == '.csv': 
            with open(os.path.join('./data', letter ,file), 'r') as f:
                for line in f.readlines():
                    line = line.split(',')
                for i in range(5):
                    y[letter][i].append(int(line[i])/1023) 
                for i in range(3):
                    y[letter][5+i].append(float(line[5+i]))

for x in range(8):
    for letter in letters: 
        plt.scatter([x]*len(y[letter][x]), y[letter][x], color=colors[letter], label=letter if x == 0 else None)

plt.title('Sensor Values Normalized')
plt.legend()
plt.xticks(range(8), ['Thumb','Index','Middle','Ring','Pinky','AccX','AccY','AccZ'])
plt.show()


