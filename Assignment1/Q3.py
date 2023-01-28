from math import pi
from random import uniform
import matplotlib.pyplot as plt


def estimatePi(n):
    pointsInCircle = 0
    pointsGenerated = []
    fraction4List = []
    for i in range(n):
        # Generating n points
        x = uniform(-1, +1)
        y = uniform(-1, +1)
        # Check whether point lies in unit circle
        if x*x + y*y <= 1.0: 
            pointsInCircle += 1
        fraction4List.append((4*(pointsInCircle))/(i+1))
        pointsGenerated.append(i+1)

    # Plot details
    plt.title("Estimates π using Monte Carlo Method")
    plt.xlabel("No. of points generated")
    plt.ylabel("4 x fraction of points within the circle")

    plt.ylim(bottom=3.10, top=3.20)
    plt.axhline(y=pi, color="r", label="Value of math.pi")
    plt.plot(pointsGenerated, fraction4List,
             color="#1784bf", label="Monte Carlo Method")
    plt.legend(loc="lower right")
    plt.show()


def main():
    estimatePi(2000000)


if __name__ == "__main__":
    main()
