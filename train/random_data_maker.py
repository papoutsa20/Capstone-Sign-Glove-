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
for letter in LETTERS:
    values = []
    for _ in range(NUMBER_OF_ITER_PER_LETTER):
        row = []
        for _ in range(5):
            row.append(str(random.randint(FLEX_SENSOR_MIN, FLEX_SENSOR_MAX)))
        for _ in range(3):
            row.append(str(random.uniform(GYRO_MAX, GYRO_MIN)))
        values.append(','.join(row))
    with open(os.path.join(DATA_PATH, letter, FILE_NAME), 'w') as f:
        f.write('\n'.join(values))
