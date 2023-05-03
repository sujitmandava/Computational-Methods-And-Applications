import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x*np.exp(x)


def fd(x):
    return np.exp(x) + x*(np.exp2(x))


def f2(x):
    return x**2


def fd2(x):
    return 2*x


def newtonRaphsonMethod(f, fd, x0=100, N=100):
    x = [x0]
    # print(x[-1])

    for i in range(N):
        # if f(x[-1]) == 0:
        #     return x

        xt = x[-1] - f(x[-1])/fd(x[-1])
        x.append(xt)

    return x


def secantMethod(f, x0=100, x1=101, N=100):
    x = [x0, x1]
    # print(x[-1])

    for i in range(N):
        # if f(x[-1] == 0):
        #     return x

        xt = x[-1] - f(x[-1])*((x[-1] - x[-2])/(f(x[-1]) - f(x[-2])))
        x.append(xt)

    return x


def compareMethods(xN, xS):
    def getROC(x):
        alpha = []
        for i in range(2, len(x) - 1):
            alpha.append(
                np.log(abs((x[i + 1] - x[i]) /
                           (x[i] - x[i - 1])))
                / np.log(abs((x[i] - x[i - 1]) / (x[i - 1] - x[i - 2])))
            )
        return alpha
    
    rN = getROC(xN)
    rS = getROC(xS)

    plt.title("Rate of Convergence")
    plt.ylabel("Alpha")
    plt.xlabel("Iteration")
    plt.plot(list(range(2, len(rS) + 2)), rS, label="Secant Method")
    plt.plot(list(range(2, len(rN) + 2)), rN, label="Newton-Raphson Method")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    xN = newtonRaphsonMethod(f=f2,fd=fd2)
    xS = secantMethod(f=f2)
    # print(xN)
    # print(xS)
    compareMethods(xN, xS)