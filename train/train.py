import tensorflow as tf
import numpy as np
import os
from sklearn.utils import shuffle
import predict
import time
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
'''
LETTERS = (
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z'
)
'''


LETTERS = (
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z'
)


# import data from folders
# looks for folders by letter in DATA_PATH (ex DATA_PATH/A)
# returns np arrays of values and labels

def read_data():
    data = []
    labels = []
    poi = ('Jason3.csv', 'Spencer2.csv', 'Stelios2.csv')#, 'Spencer2.csv', 'Stelios2.csv')
    for letter in range(len(LETTERS)):
        try:
            for data_file in [x for x in os.listdir(os.path.join(DATA_PATH,LETTERS[letter])) if x in poi]:
                if data_file[-4:] == '.csv':
                    with open(os.path.join(DATA_PATH,LETTERS[letter],data_file), 'r') as f:
                        for line in f.readlines():
                            data.append(line.split(','))
                            #data.append(line.split(',')[:5] + [0,0,0])
                            labels.append(letter)
        except OSError as ex:
            print('ERROR: '+ str(ex))
    
    return np.array(data, dtype=float),np.array(labels, dtype=int)

# any preprocess step done here
def preprocess_data(data, maxes, mins):
    max_value = 1023.0
    #print(maxes.shape)

    for i in range(8):
        data[:,i:i+1] = data[:,i:i+1] - mins[i]
        data[:,i:i+1] = data[:,i:i+1] / (maxes[i] - mins[i])
     
    '''
    data[:,:5] = data[:,:5] / max_value
    data[:,5:] = data[:,5:] / 2.0 
    print(data.shape)
    '''
    '''
    exit()
    left_side = data[:,:5] / max_value
    #print(left_side)
    print(left_side.shape)
    right_side = data[:,5:] / 2.0
    #print(right_side)
    print(right_side.shape)
    final = np.append(left_side, right_side)
    print(final.shape)
    #temp.append(data[6:9] / 2.0)
    print(final)
    '''
    return data

def create_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(8,)),
        tf.keras.layers.Dense(len(LETTERS)+10, activation='relu'),
        tf.keras.layers.Dense(len(LETTERS), activation='softmax')
    ])


    model.compile(optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    return model

def split_train_test(data, labels, percent_train=.95):
    cut_off = int(data.shape[0]*.80)
    grades, labels = shuffle(data, labels)
    train_x = grades[:cut_off]
    train_y = labels[:cut_off]
    test_x = grades[cut_off:]
    test_y = labels[cut_off:]
    return train_x, train_y, test_x, test_y

def find_maxes(data):
    
    data0 = np.amax(data[:,0:1])
    data1 = np.amax(data[:,1:2])
    data2 = np.amax(data[:,2:3])
    data3 = np.amax(data[:,3:4])
    data4 = np.amax(data[:,4:5])
    
    data5 = np.amax(data[:,5:6])
    data6 = np.amax(data[:,6:7])
    data7 = np.amax(data[:,7:8])
    
    return (data0, data1, data2, data3, data4, data5, data6, data7)

def find_mins(data):

    data0 = np.amin(data[:,0:1])
    data1 = np.amin(data[:,1:2])
    data2 = np.amin(data[:,2:3])
    data3 = np.amin(data[:,3:4])
    data4 = np.amin(data[:,4:5])
    
    data5 = np.amin(data[:,5:6])
    data6 = np.amin(data[:,6:7])
    data7 = np.amin(data[:,7:8])
    
    return (data0, data1, data2, data3, data4, data5, data6, data7)


if '__main__' == __name__:
    #model = load_model();
    #predict.predictValues(model)
    model = create_model()
    print('reading data from {}'.format(DATA_PATH))
    data, labels = read_data() 
    print(data)
    maxes = find_maxes(data)
    mins = find_mins(data)

    for i in range(8):
        print(maxes[i])
        print(mins[i])


    print(labels)
    #exit()
    data = preprocess_data(data, maxes, mins)
    #print(data)
    print(data.shape)
    print(labels.shape)
    #exit()
    model = create_model()
    train_x, train_y, test_x, test_y = split_train_test(data, labels)
    #print(train_x.shape)
    #print(test_x.shape)
    model.fit(train_x, train_y, epochs=500)

    model.evaluate(test_x, test_y, verbose=2)
    #model.save('jason_model{}.h5'.format(time.time()))
    model.save('three_model.h5')

    predict.predictValues(model)
