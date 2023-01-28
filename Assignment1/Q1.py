import matplotlib.pyplot as plt
from math import log, exp, pi


def logStirling(n: int) -> float:
    # Function to compute Stirling's Approximation
    return ((1 / 2) * (log(2 * pi) + log(n))) + (n * (log(n) - 1))


def logFactorial(n: int):
    # Function to compute actual log values
    lF = []
    currLog = 0
    for i in range(1, n+1):
        currLog += log(i)
        lF.append(currLog)
    return lF


def factorials(n: int):
    sF = []  # Approximation
    logF = logFactorial(n)  # Log of factorial
    for i in range(1, n+1):
        sF.append((logStirling(i)))
    return sF, logF


def main():
    N = 1000000
    sF, logF = factorials(N)
    x = list(range(1, N+1))
    y1 = list(sF)
    y2 = list(logF)
    # Plot details
    plt.title("Visualizing Stirling's Approximation")
    plt.xlabel("n")
    plt.ylabel("Logarithm values")

    plt.plot(x, y1, "r", lw=3, label="Stirling's Approximation")
    plt.plot(x, y2, "black", lw=1.5, label="Log of Factorial")
    plt.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    main()
