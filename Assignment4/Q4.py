import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 2*x*np.exp(x*x)


def integralM(a, b, M):
    integral = 0
    coef = (b-a)/(2*M)
    for k in range(1, M):
        x0 = a + (b-a)*(k-1)/M
        x1 = a + (b-a)*k/M
        y0 = f(x0)
        y1 = f(x1)

        integral += (y1 + y0)

    return coef*integral


if __name__ == "__main__":
    x = np.linspace(1, 3, 1000)
    y = f(x)

    plt.plot(x, y, color='blue', label='f(x)')
    plt.yscale('log')
    plt.grid()
    plt.legend(loc='best')
    plt.show()
