import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    x1, x2, x3 = x
    f1 = 3*x1 - np.cos(x2*x3) - 1.5
    f2 = 4*x1*x1 - 625*x2*x2 + 2*x3 - 1
    f3 = 20*x3 + np.exp(-1*x1*x2) + 9

    return [f1, f2, f3]


def fj(x):
    x1, x2, x3 = x
    j1 = [3, x3 * np.sin(x2 * x3), x2 * np.sin(x2 * x3)]
    j2 = [8 * x1, -1250 * x2, 2]
    j3 = [-x2 * np.exp(-1 * x1 * x2), -x1 * np.exp(-1 * x1 * x2), 20]

    return [j1, j2, j3]


def newtonRaphsonMethod(f, fj, x0=[10, 11, 12], N=100):
    x = [x0]

    for i in range(N):
        xt = x[-1] - la.inv(fj(x[-1]))@f(x[-1])
        x.append(xt)

    return x


if __name__ == "__main__":
    xN = newtonRaphsonMethod(f=f, fj=fj)
    print(f"Root of the given equations is: {xN[-1]}")

    xNorms = [la.norm(f(x)) for x in xN]
    plt.title("Newton Raphson Method")
    plt.xlabel("Iteration")
    plt.ylabel("Norm")
    plt.plot(list(range(1, len(xN)+1)), xNorms, label='Newton-Raphson', color='blue')
    plt.legend(loc='best')
    plt.grid()
    plt.show()
