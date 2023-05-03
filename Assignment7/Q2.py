from matplotlib import projections
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


def getTridiagonalMatrix(a, b, c, n):
    return np.eye(n, k=1) * a + np.eye(n, k=0) * b + np.eye(n, k=-1) * c


def plot2DHeatEquation(
    fT, fB, f, mu, T, h, ht, xmin, xmax, ymin, ymax, xc, yc
):
    def solvePDE(fT, fB, f, mu, T, h, ht, xmin, xmax, ymin, ymax, xc, yc):
        N = int((xmax - xmin) // h) + 1
        xArr = np.linspace(xmin, xmax, N + 1)
        yArr = np.linspace(ymin, ymax, N + 1)

        nTime = int(T // ht) + 1
        time = np.linspace(0, T, nTime + 1)

        A = getTridiagonalMatrix(1, -2, 1, N+1)
        u = np.array([[fT(x, y) for y in yArr] for x in xArr])
        result = [u]

        for t in time[1:]:
            m = np.array([[f(x, y, t, xc, yc) for y in yArr] for x in xArr])
            du = ((mu / (h**2)) * ((A @ u) + (u @ A))) + m
            u = u + ht * du
            for i in range(N + 1):
                u[i][0] = fB(t)
                u[i][-1] = fB(t)
            for j in range(N + 1):
                u[0][j] = fB(t)
                u[-1][j] = fB(t)
            result.append(u)

        return result, xArr, yArr, time

    result, xArr, yArr, time = solvePDE(
        fT, fB, f, mu, T, h, ht, xmin, xmax, ymin, ymax, xc, yc)

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    patches = []

    X, Y = np.meshgrid(xArr, yArr)
    ax.plot_surface(
        X,
        Y,
        result[0],
        cmap="hot",
        linewidth=0,
        antialiased=False,
    )

    def anim_init():
        ax.set_title(
            f"Heat conduction in a sheet with boundary [{xmin}, {xmax}]x[{ymin}, {ymax}] and mu = {mu}"
        )
        return patches

    def animate(i):
        ax.plot_surface(
            X,
            Y,
            result[i],
            cmap="hot",
            linewidth=0,
            antialiased=False,
        )
        return patches

    numFrames = len(result)
    interval = 1

    anim = FuncAnimation(
        fig,
        func=animate,
        frames=numFrames,
        init_func=anim_init,
        repeat=False,
        interval=interval,
    )

    plt.show()

    return anim


if __name__ == "__main__":
    def in_uT0(x, y): return 0
    def in_uB(t): return 0

    def in_f(
        x, y, t, xc, yc): return np.exp(-np.sqrt(((x - xc) ** 2) + ((y - yc) ** 2)))
    in_mu = 5 * (10 ** (-5))
    in_T, in_h, in_ht = 2000, 0.01, 0.5
    in_xmin, in_xmax, in_ymin, in_ymax = 0, 1, 0, 1
    in_xc, in_yc = 0.5, 0.5

    ani = plot2DHeatEquation(
        fT=in_uT0,
        fB=in_uB,
        f=in_f,
        mu=in_mu,
        T=in_T,
        h=in_h,
        ht=in_ht,
        xmin=in_xmin,
        xmax=in_xmax,
        ymin=in_ymin,
        ymax=in_ymax,
        xc=in_xc,
        yc=in_yc
    )
