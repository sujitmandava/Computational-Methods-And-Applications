import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def solveVanDerPol(x0, v0, mu, t0, T, n=1000):
    def ivpFunc(t, y):
        x, v = y
        return [v, mu*(1-(x**2))*v-x]

    t = np.linspace(t0, T, n)
    solution = solve_ivp(fun=ivpFunc, t_span=[t0, T], y0=[x0, v0], t_eval=t)
    Xt = solution.y[0]
    plt.title("Van Der Pol Equation")
    plt.plot(t, Xt, color='r')
    plt.grid()
    plt.show()

    pt1 = 0
    for i in range(1, n):
        if Xt[i-1] <= 0 and Xt[i] >= 0:
            pt1 = i
            break

    pt2 = -1
    for i in range(1, pt1):
        if Xt[i-1] <= 0 and Xt[i] >= 0:
            pt2 = i
            break

    timePeriod = abs(pt1-pt2)
    print(f"Time period of the oscillation for mu={mu}: {timePeriod}")


if __name__ == "__main__":
    solveVanDerPol(x0=0, v0=10, mu=0, t0=0, T=200)
