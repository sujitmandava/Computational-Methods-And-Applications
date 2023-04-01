import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def ode(t, theta, v, g, L):
    return (v, -(g/L)*math.sin(theta))


def pendulumODE(ode, g, L, v0, theta0, t0, T, h):
    currT = t0
    currV = v0
    currTheta = theta0
    thetaList = [theta0]

    while currT <= T:
        currODE = ode(currT, currTheta, currV, g, L)
        currTheta += h*currODE[0]
        currV += h*currODE[1]
        thetaList.append(currTheta)
        currT += h

    initX, initY = L*math.sin(theta0), -L*math.cos(theta0)

    fig = plt.figure()
    ax = fig.add_subplot(aspect='equal')

    (line,) = ax.plot([0, initX], [0, initY], lw=3, color='blue')
    pendulum = ax.add_patch(plt.Circle(
        (initX, initY), 0.01, color='black', zorder=3))
    patches = [line, pendulum]

    def anim_init():
        ax.set_title("Gravity Pendulum")
        ax.set_xlim(-2*L, 2*L)
        ax.set_ylim(-2*L, 2*L)

        return patches

    def animate(i):
        x, y = L*math.sin(thetaList[i]), -L*math.cos(thetaList[i])

        line.set_data([0, x], [0, y])
        pendulum.set_center((x, y))

        return patches

    numFrames = len(thetaList)
    interval = 1

    anim = FuncAnimation(fig, animate, init_func=anim_init,
                         frames=numFrames, repeat=True, interval=interval, blit=True,)
    plt.grid()
    plt.show()
    return anim


if __name__ == "__main__":
    animation = pendulumODE(ode, 10, 0.1, 0, math.pi/4, 0, 10, 0.001)
