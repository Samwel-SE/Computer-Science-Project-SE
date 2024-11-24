import random

# THIS SCRIPT IS COMPLETELY ORIGINAL --------------------------------------------------------------------------------------

def randomise(terms):
    for i in range(len(terms)):
        # these arguments control range of values for y variable of terrain
        terms[i] = random.randint(450, 700)  


def smooth(terms):  # smooths terrain by setting y variable equal to average of itself and adjacent y variables in list
    terms[0] = (terms[0] + terms[1]) // 2

    for i in range(1, len(terms) - 2):
        terms[i] = (terms[i - 1] + terms[i] + terms[i + 1]) // 3
    
    terms[len(terms) - 1] = (terms[len(terms) - 2] + terms[len(terms) - 3]) // 2


def generate(width, smoothness): #width: controls length of list, smoothness: how many times smooth function is run over the list
    terr = [0] * width
    randomise(terr)
    for i in range(smoothness):
        smooth(terr)
    return terr
