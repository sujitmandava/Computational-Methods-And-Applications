import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(x**2)


def f_prime(x):
    return 2*x*np.cos(x**2)


def forward_diffference(x, h):
    return (f(x+h) - f(x))/h


def centered_difference(x, h):
    return (f(x+h) - f(x-h))/(2*h)


if __name__ == "__main__":
    x = np.linspace(0, 1, 1000)
    h_vals = np.logspace(-16, 0, 1000)

    maxForwardError = []
    maxCenteredError = []

    for h in h_vals:
        error_forward = np.max(np.abs(forward_diffference(x, h) - f_prime(x)))
        error_centered = np.max(np.abs(centered_difference(x, h) - f_prime(x)))
        maxForwardError.append(error_forward)
        maxCenteredError.append(error_centered)

    max_error_forward_theoretical = 2*np.abs(np.cos(0))
    max_error_centered_theoretical = 2*np.abs(np.cos(0))

    plt.title(
        "Max absolute error of different approximations v/s h")
    plt.plot(h_vals, maxForwardError, color='red',
             label='Forward difference approximation')
    plt.plot(h_vals, maxCenteredError, color='blue',
             label='Centered difference approximation')
    plt.plot(h_vals, max_error_centered_theoretical*np.ones(len(h_vals)),
             '.', color='purple', label='Theoretical Max Centered Error')
    plt.plot(h_vals, max_error_forward_theoretical*np.ones(len(h_vals)),
             '--', color='green', label='Theoretical Max Forward Error')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('h')
    plt.ylabel('Max Absolute Error')
    plt.legend(loc="best")
    plt.tight_layout()
    plt.grid()
    plt.show()
