from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt


def norm12(r1, r2):
    return max(np.linalg.norm(r2-r1), 20)


def rdd(r, rA, rB):
    return (rA-r)/(norm12(r, rA)**3) + (rB-r)/(norm12(r, rB)**3)


def calcCentre(r1, r2, r3):
    rCentre = []
    for i in range(len(r1)):
        rCentre.append((r1[i]+r2[i]+r3[i])/3)
    return rCentre


def solveODE(rInit, vInit, t0, T, n=1000):
    def ivpFunc(t, y):
        r1x, r1y, r2x, r2y, r3x, r3y, v1x, v1y, v2x, v2y, v3x, v3y = y
        r1 = np.array([r1x, r1y])
        r2 = np.array([r2x, r2y])
        r3 = np.array([r3x, r3y])
        v1 = [v1x, v1y]
        v2 = [v2x, v2y]
        v3 = [v3x, v3y]

        v1d = rdd(r1, r2, r3)
        v2d = rdd(r2, r1, r3)
        v3d = rdd(r3, r1, r2)
        return [*v1, *v2, *v3, *v1d, *v2d, *v3d]

    t = np.linspace(t0, T, n)

    solution = solve_ivp(fun=ivpFunc, t_span=[t0, T], y0=[
                         *rInit, *vInit], t_eval=t)

    r1x, r1y, r2x, r2y, r3x, r3y, *vs = solution.y

    fig = plt.figure()
    ax = fig.add_subplot(aspect='equal')

    bodyA = ax.add_patch(plt.Circle(
        (r1x[0], r1y[0]), 0.1, color='purple', zorder=3, label='Body A'))
    bodyB = ax.add_patch(plt.Circle(
        (r2x[0], r2y[0]), 0.1, color='orange', zorder=3, label='Body B'))
    bodyC = ax.add_patch(plt.Circle(
        (r3x[0], r3y[0]), 0.1, color='blue', zorder=3, label='Body C'))

    centre = calcCentre([r1x[0], r1y[0]], [r2x[0], r2y[0]], [r3x[0], r3y[0]])
    plt.scatter(centre[0], centre[1], marker='o',
             label="Centre of initial three points", color='black')
    patches = [bodyA, bodyB, bodyC]

    def anim_init():
        ax.set_title("Three Body Problem")
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)

        return patches

    def animate(i):
        bodyA.set_center((r1x[i], r1y[i]))
        bodyB.set_center((r2x[i], r2y[i]))
        bodyC.set_center((r3x[i], r3y[i]))

        return patches

    numFrames = len(r1x)
    anim = FuncAnimation(fig, animate, init_func=anim_init,
                         frames=numFrames, repeat=True, interval=1, blit=True,)

    plt.legend()
    plt.grid()
    plt.show()

    return anim


if __name__ == "__main__":
    r10 = [0, 4]
    r20 = [3.46, -2]
    r30 = [-3.46, -2]
    v10 = [0, 0]
    v20 = [0, 0]
    v30 = [0, 0]

    c = calcCentre(r10, r20, r30)
    print(c)
    print(type(c))
    ani = solveODE(rInit=[*r10, *r20, *r30],
                   vInit=[*v10, *v20, *v30], t0=0, T=400)
