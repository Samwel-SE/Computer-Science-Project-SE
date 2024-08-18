import random


def randomise(terms):
    for i in range(len(terms)):
        terms[i] = random.randint(
            550, 700
        )  # these parameters control y variable of terrain


def smooth(
    terms,
):  # smooths terrain by setting y variable equal to average of itself and adjacent y variables
    terms[0] = (terms[0] + terms[1]) // 2
    for i in range(1, len(terms) - 2):
        terms[i] = (terms[i - 1] + terms[i] + terms[i + 1]) // 3
    terms[len(terms) - 1] = (terms[len(terms) - 2] + terms[len(terms) - 3]) // 2


def generate(
    width, smoothness
):  # takes parameters of width of screen and how many times they want smoothness function to run
    terr = [0] * width
    randomise(terr)
    for i in range(smoothness):
        smooth(terr)
    return terr
