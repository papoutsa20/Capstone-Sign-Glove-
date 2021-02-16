from train import LETTERS
import numpy as np

def predictValues(model):
    while True:
        inputStr = input("Enter an input string: {d1, d2, d3, d4, d5, gx, gy, gz}\n" +
                         "Enter (q) to quit. {1000, 800, 500, 200, 300, .23, .45, .50}\n\n> ")
        if inputStr == "q" or inputStr == "quit": return 0
        
        inputs = inputStr.strip("{}()[]").split(',')
        inputs = [float(i) for i in inputs]
        inputs = np.array([inputs], dtype=float)
        print(inputs)        
        modelGuess = predictValue(inputs, model)
        #print(modelGuess)
        printPrediction(modelGuess)
        print("\n")
    return 1 

#Takes input (d1, d2, d3, d4, d5, gx, gy, gz) as input
def predictValue(inputs, model):
    if type(inputs) is not list and False:
        print("Error: Input (inputs) for predictValue is not a list")
        return 0
    if len(inputs) != 8 and False:
        print(f"Error: Input (inputs) for predictValues has incorrect length.\n" +
              "(8) expected and ({}) given.".format(len(inputs)))
        return 0
    guessWeights = []
    if model == None:
        print("Warning: Model given was invalid, printing default output instead")
        guessWeights = [0.0] * 26;
    else:
        guessWeights = model.predict(inputs)[0]
    return guessWeights

def printPrediction(guessWeights):
    if type(guessWeights) is not list and False:
        print("Error: Input (inputs) for printPrediction is not a list")
        return 0
    elif len(guessWeights) != 26 and False:
        print(f"Error: Input (guessWeights) for printPrediction has incorrect length.\n" +
              "(26) expected and ({}) given.".format(len(inputs)))
        return 0
    str = '' 
    max_index = np.argmax(guessWeights)
    print("I believe that is a {}".format(LETTERS[max_index]))
    for i in range(26):

        str += LETTERS[i]
        str += ' '
        str += "{:10.4f}".format(float(guessWeights[i]))
        str += '\n'
    print(str)
