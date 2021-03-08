"""
Graphs the normailized resister sensor values on a graph
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# use colors for letters here
colors = {
        'A': 'r',
        'C': 'b',
        'G': 'g',
        'V': 'red',
        'W': 'purple'
}

# letters to graph
letters = ['A','C','G']


x = np.arange(8)
y = {}
for letter in letters: 
    with open(os.path.join('./data', letter ,'Jason.csv'), 'r') as f:
        y[letter] = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
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


