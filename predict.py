def predictValues(model):
    while True:
        inputStr = input("Enter an input string: {d1, d2, d3, d4, d5, gx, gy, gz}\n" +
                         "Enter (q) to quit. {1000, 800, 500, 200, 300, .23, .45, .50}\n\n> ")
        if inputStr == "q" or inputStr == "quit": return 0
        
        inputs = inputStr.strip("{}()[]").split(',')

        print(inputs)
        modelGuess = predictValue(inputs, model)
        print(modelGuess)
        print("\n")
    return 1 

#Takes input (d1, d2, d3, d4, d5, gx, gy, gz) as input
def predictValue(inputs, model):
    if type(inputs) is not list:
        print("Error: Input (inputs) for predictValue is not a list")
        return 0
    elif len(inputs) != 8:
        print(f"Error: Input (inputs) for predictValues has incorrect length.\n" +
              "(8) expected and ({}) given.".format(len(inputs)))
        return 0
    guessWeights = []
    if model == None:
        print("Warning: Model given was invalid, printing default output instead")
        guessWeights = [0.0] * 26;
    else:
        guessWeights = model.predict(inputs)[0][:]
    return guessWeights

def printPrediction(guessWeights):
    if type(guessWeights) is not list:
        print("Error: Input (inputs) for printPrediction is not a list")
        return 0
    elif len(guessWeights) != 26:
        print(f"Error: Input (guessWeights) for printPrediction has incorrect length.\n" +
              "(26) expected and ({}) given.".format(len(inputs)))
        return 0

predictValues(None)
