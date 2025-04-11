import random

def randomise(terms):
    for i in range(len(terms)):
        # these arguments control range of values for y variable of terrain
        terms[i] = random.randint(375, 625)  


# smooths terrain by setting y variable equal to average of itself and adjacent y variables in list
def smooth(terms):  
    terms[0] = (terms[0] + terms[1]) // 2

    for i in range(1, len(terms) - 2):
        terms[i] = (terms[i - 1] + terms[i] + terms[i + 1]) // 3
    
    terms[-1] = (terms[-1] + terms[-2]) // 2

#width: controls length of list, smoothness: how many times smooth function is run over the list
def generate(width, smoothness): 
    terr = [0] * width
    randomise(terr)
    
    # then smooths terrain for smoothness No. times
    for i in range(smoothness): 
        smooth(terr)
    return terr






