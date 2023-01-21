import matplotlib.pyplot as plt
from random import random


class Dice():
    # Attributes
    numSides = 6
    probSides = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
    cdf = []

    def checkProbability(self, pSides):
        totalProb = 0

        if len(pSides) != self.numSides:
            raise Exception("Invalid probability distribution")

        for pSide in pSides:
            totalProb += pSide

        if totalProb != 1:
            raise Exception("Invalid probability distribution")

    def __init__(self, sides=6) -> None:
        if (sides < 4):
            raise Exception("Cannot construct the dice")

        if type(sides) == float:
            raise Exception("Cannot construct the dice")

        self.numSides = sides
        pSide = 1/sides
        pSides = [pSide]*sides
        self.setProb(pSides)

    def setProb(self, pSides):
        self.checkProbability(pSides)
        self.probSides = pSides
        self.cdf.clear()

        tcdf = 0.0
        for pSide in pSides:
            tcdf += pSide
            self.cdf.append(tcdf)

    def __str__(self):
        sides = self.numSides
        pDist = self.probSides

        return "Dice with " + str(sides) + " faces and probability distribution " + str(pDist)

    def roll(self, n):
        currRolls = [0]*self.numSides
        for i in range(n):
            currRoll = random()
            for p in range(len(self.cdf)):
                if currRoll < self.cdf[p]:
                    currRolls[p] += 1
                    break
        x = list(range(1, self.numSides+1))
        yRolls = list(currRolls)
        yPreds = [i*n for i in self.probSides]

        plt.title(
            "Outcome of {n} throws of a {numSides}-faced dice".format(
                n=n, numSides=self.numSides)
        )
        plt.xlabel("Sides")
        plt.ylabel("Occurences")
        plt.bar([i-0.15 for i in x], yRolls, color="red", width = 0.3, label="Actual Rolls")
        plt.bar([i+0.15 for i in x], yPreds, color="blue", width = 0.3, label="Predicted Rolls")
        plt.legend(loc="best")
        plt.show()


def main():
    N = 12
    d1 = Dice(N)
    print(d1)
    # d1.setProb([0,0,0,0,0,0,0.1,0.2,0.3,0.4,0,0])
    d1.roll(1000000)


if __name__ == "__main__":
    main()
