import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(x**2)


def f_prime(x):
    return 2*x*np.cos(x**2)


def forward_difference(x, h):
    return (f(x+h) - f(x))/h


if __name__ == "__main__":
    x = np.linspace(0, 1, 1000)
    y_actual = f_prime(x)
    y_approx = forward_difference(x, 0.01)

    plt.title(
        "Derivative of $sin(x^{2})$ v/s Forward Finite Difference Approximation")
    plt.plot(x, y_actual, color='red', label='$sin(x^{2})$')
    plt.plot(x, y_approx, color='blue',
             label='Forward difference approximation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.grid()
    plt.show()
