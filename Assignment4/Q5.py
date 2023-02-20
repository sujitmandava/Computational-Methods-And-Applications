import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


def f(x):
    return 2*x*np.exp(x*x)


def integral_f(x):
    return np.exp(x*x)


def visualizeIntegrals(u_max):
    uPoints = np.linspace(0, u_max, 1000)
    uPoints = list(filter(lambda x: x != 0, uPoints))
    actualArea = []
    trapezoid = []
    quad = []
    simpson = []
    romberg = []

    for u in uPoints:
        x = np.linspace(0, u, 1000)
        y = [f(p) for p in x]

        actualArea.append(integral_f(u) - integral_f(0))
        trapezoid.append(integrate.trapezoid(y, x))
        quad.append(integrate.quad(f, 0, u)[0])
        simpson.append(integrate.simpson(y, x))
        romberg.append(integrate.romberg(f, 0, u))

    plt.title("Various integration functions for area under y(x) = 2x*exp(x^2)")
    plt.xlabel("u")
    plt.ylabel("Area under curve")

    plt.plot(uPoints, actualArea, color='blue', label='Actual area')
    plt.plot(uPoints, romberg, color='orange', label='Romberg')
    plt.plot(uPoints, trapezoid, color='red', label='Trapezoid')
    plt.plot(uPoints, quad, color='green', label='Quadrature/General Purpose')
    plt.plot(uPoints, simpson, color='purple', label='Simpson')

    plt.legend(loc='best')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # Input max u value
    visualizeIntegrals(0.2)
