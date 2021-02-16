import tensorflow as tf
import numpy as np
import os
from sklearn.utils import shuffle
import predict
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
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
    for letter in range(len(LETTERS)):
        try:
            for data_file in os.listdir(os.path.join(DATA_PATH,LETTERS[letter])):
                if data_file[-4:] == '.csv':
                    with open(os.path.join(DATA_PATH,LETTERS[letter],data_file), 'r') as f:
                        for line in f.readlines():
                            data.append(line.split(','))
                            labels.append(letter)
        except OSError as ex:
            print('ERROR: '+ str(ex))
    
    return np.array(data, dtype=float),np.array(labels, dtype=int)

# any preprocess step done here
def preprocess_data(data):
    max_value = 1023.0
    return data / 1023.0 

def create_model():

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(8,)),
        tf.keras.layers.Dense(30, activation='relu'),
        tf.keras.layers.Dense(26, activation='softmax')
    ])

    model.compile(optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    return model

def split_train_test(data, labels, percent_train=.80):
    cut_off = int(data.shape[0]*.80)
    grades, labels = shuffle(data, labels)
    train_x = grades[:cut_off]
    train_y = labels[:cut_off]
    test_x = grades[cut_off:]
    test_y = labels[cut_off:]
    return train_x, train_y, test_x, test_y

if '__main__' == __name__:
    print('reading data from {}'.format(DATA_PATH))
    data, labels = read_data() 
    print(data)
    print(labels)

    model = create_model()
    train_x, train_y, test_x, test_y = split_train_test(data, labels)

    model.fit(train_x, train_y, epochs=100)

    model.evaluate(test_x, test_y, verbose=2)

    predict.predictValues(model)
