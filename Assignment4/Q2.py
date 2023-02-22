import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(x**2)


def f_prime(x):
    return 2*x*np.cos(x**2)


def forward_difference(x, h):
    return (f(x+h) - f(x))/h


def backward_difference(x, h):
    return (f(x) - f(x-h))/h


def centered_difference(x, h):
    return (f(x+h) - f(x-h))/(2*h)


if __name__ == "__main__":
    x = np.linspace(0, 1, 1000)
    yf = abs(forward_difference(x, 0.01))
    yb = abs(backward_difference(x, 0.01))
    yc = abs(centered_difference(x, 0.01))

    plt.title(
        "Absolute errors of different approximations")
    plt.plot(x, abs(yf-f_prime(x)), color='red',
             label='Forward difference approximation')
    plt.plot(x, abs(yb-f_prime(x)), color='blue',
             label='Backward difference approximation')
    plt.plot(x, abs(yc-f_prime(x)), color='green',
             label='Centered difference approximation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc="best")
    # plt.tight_layout()
    plt.grid()
    plt.show()
