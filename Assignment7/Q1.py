from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


def fT(x):
    return np.exp(-x)


def f0(t):
    return 0


def fL(t):
    return 0


def f(x, t):
    return 0


def getTridiagonalMatrix(a, b, c, n):
    return np.eye(n, k=1) * a + np.eye(n, k=0) * b + np.eye(n, k=-1) * c


def plotHeatEquation(L, T, h, ht, f0, fT, fL, f, mu):
    def solvePDE(L, T, h, ht, f0, fT, fL, f, mu):
        nRod = int(L // h) + 1
        rod = np.linspace(0, L, nRod + 1)

        nTime = int(T // ht) + 1
        time = np.linspace(0, T, nTime + 1)

        A = getTridiagonalMatrix(1, -2, 1, nRod+1)
        u = np.array([fT(x) for x in rod])
        result = [u]

        for t in time[1:]:
            m = np.array([f(x, t) for x in rod])
            du = ((mu / (h**2)) * (A @ u)) + m
            u = u + ht * du
            u[0] = f0(t)
            u[-1] = fL(t)
            result.append(u)

        return result, rod, time

    result, _, _ = solvePDE(L, T, h, ht, f0, fT, fL, f, mu)

    fig = plt.figure()
    ax = plt.axes()
    patches = []

    pltHeat = plt.imshow([result[0]], cmap="hot", aspect="auto", animated=True)
    cb = fig.colorbar(pltHeat)
    cb.set_label("Temperature")
    patches.append(pltHeat)

    def anim_init():
        ax.set_title(
            f"Heat Conduction in a rod of length L = {L} and mu = {mu}")
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        return patches

    def animate(i):
        pltHeat.set_array([result[i]])
        return patches

    numFrames = len(result)
    interval = 1

    anim = FuncAnimation(
        fig,
        animate,
        init_func=anim_init,
        frames=numFrames,
        repeat=True,
        interval=interval,
    )
    plt.show()

    return anim


if __name__ == "__main__":
    L, mu = 3, (10 ** (-4))
    T, h, ht = 2000, 0.01, 0.5

    ani = plotHeatEquation(
        fT=fT,
        f0=f0,
        fL=fL,
        f=f,
        L=L,
        mu=mu,
        T=T,
        h=h,
        ht=ht,
    )
