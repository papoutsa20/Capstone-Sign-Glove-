import random
import os
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

## parameters for data
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data') 
FILE_NAME = 'RANDOM.csv'
FLEX_SENSOR_MIN = 0
FLEX_SENSOR_MAX = 1023
GYRO_MIN = 0.0
GYRO_MAX = 1.0
NUMBER_OF_ITER_PER_LETTER = 100
## Start random data
for i in range(len(LETTERS)):
    letter = LETTERS[i]
    LETTER_DIR = os.path.join(DATA_PATH, letter)
    if not os.path.isdir(LETTER_DIR):
        os.mkdir(LETTER_DIR)
            
    binary = '{0:08b}'.format(i)
    values = []
    for x in range(NUMBER_OF_ITER_PER_LETTER):
        row = []
        row = list(binary)
        row = [float(i) for i in row]
        for y in range(8):
            rand = random.randint(0, 50) / 100.0
            print(rand)
            if row[y] == 0:
                row[y] += rand
            else:
                row[y] -= rand
        row = [str(i) for i in row]
        #for y in range(8):
        #    dif = x % 2
        #    row.append(dif)
        #    x/=2
        #for _ in range(5):
        #    row.append(str(random.randint(FLEX_SENSOR_MIN, FLEX_SENSOR_MAX)))
        #for _ in range(3):
        #    row.append(str(random.uniform(GYRO_MAX, GYRO_MIN)))
        values.append(','.join(row))
    with open(os.path.join(DATA_PATH, letter, FILE_NAME), 'w') as f:
        f.write('\n'.join(values))
