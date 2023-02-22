import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 2*x*np.exp(x*x)

def f_prime(x):
    return np.exp(x*x)


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
    x = list(range(1, 1001))
    y = [integralM(1, 3, M) for M in x]

    plt.title('(Trapezoidal) Area under y(x) = 2x*exp(x^2) as a function of M')
    plt.plot(x, y, color='blue', label='Trapezoidal Approximation')
    plt.axhline(f_prime(3) - f_prime(1), color='red', label='Actual Area')
    plt.xlabel('M')
    plt.ylabel('Area under graph')
    plt.grid()
    plt.legend(loc='best')
    plt.show()
