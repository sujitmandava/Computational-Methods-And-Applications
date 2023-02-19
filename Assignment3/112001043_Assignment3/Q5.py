import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, Akima1DInterpolator, BarycentricInterpolator
from matplotlib.animation import FuncAnimation


def func(x):
    return np.tan(x) * np.sin(30*x) * np.exp(x)


xlim = (0, 1)
ylim = (-4, 4)

n_points = 5

x = np.linspace(xlim[0], xlim[1], n_points)
y = func(x)

fig, ax = plt.subplots()
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)

x_plot = np.linspace(*xlim, 1000)
ax.plot(x_plot, func(x_plot), label="True")

line_spline, = ax.plot([], [], c='red', label="Cubic Spline")
line_akima, = ax.plot([], [], c='green', label="Akima")
line_bary, = ax.plot([], [], c='purple', label="Barycentric")


def animate(i):
    n_points = i+2
    x_new = np.linspace(xlim[0], xlim[1], n_points)
    y_new = func(x_new)

    ax.set_title(
        f"Different interpolations of tan(x)⋅sin(30x)⋅eˣ for {n_points} samples")

    cs = CubicSpline(x_new, y_new)
    akima = Akima1DInterpolator(x_new, y_new)
    bary = BarycentricInterpolator(x_new, y_new)

    line_spline.set_data(x_plot, cs(x_plot))
    line_akima.set_data(x_plot, akima(x_plot))
    line_bary.set_data(x_plot, bary(x_plot))


animation = FuncAnimation(fig, animate, frames=100, interval=500)

plt.legend(loc='upper left')
plt.grid()
plt.show()
