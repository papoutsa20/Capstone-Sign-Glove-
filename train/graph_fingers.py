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
letters = ['V','W']



x = np.arange(5)
y = {}
for letter in letters: 
    with open(os.path.join('./data', letter ,'Jason.csv'), 'r') as f:
        y[letter] = {0:[],1:[],2:[],3:[],4:[]}
        for line in f.readlines():
            line = line.split(',')
            for i in range(5):
                y[letter][i].append(int(line[i])/1023) 


for x in range(5):
    for letter in letters: 
        plt.scatter([x]*len(y[letter][x]), y[letter][x], color=colors[letter])

plt.show()


