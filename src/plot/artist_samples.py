import matplotlib.pyplot as plt
import numpy as np

# samples in https://matplotlib.org/stable/tutorials/artists.html


def sample0() -> None:
    # Figure -> Axes -> primitives
    fig = plt.figure()  # Figure
    # two rows, one column, first plot
    ax = fig.add_subplot(2, 1, 1)  # Axes
    t = np.arange(0.0, 1.0, 0.01)
    s = np.sin(2 * np.pi * t)
    (_line,) = ax.plot(t, s, color="blue", lw=2)  # Line2D (one of primitives)
    _xtext = ax.set_xlabel("my xdata")  # Text (one of primitives)
    _ytext = ax.set_ylabel("my ydata")
    plt.show()
