import matplotlib.lines as lines
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


def sample1() -> None:
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_ylabel("Voltage [V]")
    ax1.set_title("A sine wave")

    t = np.arange(0.0, 1.0, 0.01)
    s = np.sin(2 * np.pi * t)
    (line,) = ax1.plot(t, s, color="blue", lw=2)

    # (left, bottom, width, height)
    ax2 = fig.add_axes((0.15, 0.1, 0.7, 0.3))
    n, bins, patches = ax2.hist(np.random.randn(1000), 50, facecolor="yellow", edgecolor="yellow")
    ax2.set_xlabel("Time [s]")

    plt.show()


def sample2() -> None:
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)

    x = np.arange(-np.pi, np.pi, 0.01)
    y = np.sin(x)
    (line,) = ax.plot(x, y)

    # inspect figure state
    plt.getp(fig)


def sample3() -> None:
    fig = plt.figure()

    l1 = lines.Line2D((0, 1), (0, 1), transform=fig.transFigure, figure=fig)
    l2 = lines.Line2D((0, 1), (1, 0), transform=fig.transFigure, figure=fig)
    fig.lines.extend([l1, l2])

    plt.show()


def sample4() -> None:
    fig = plt.figure()
    rect = fig.patch  # a rectangle
    rect.set_facecolor("lightgoldenrodyellow")

    ax1 = fig.add_axes((0.1, 0.3, 0.4, 0.4))
    ax1.patch.set_facecolor("lightslategray")

    for label in ax1.xaxis.get_ticklabels():
        label.set_color("red")
        label.set_rotation(45)
        label.set_fontsize(16)

    for line in ax1.yaxis.get_ticklines():
        line.set_color("green")
        line.set_markersize(25)
        line.set_markeredgewidth(3)

    plt.show()


def sample5() -> None:
    fig, ax = plt.subplots()
    ax.plot(100 * np.random.rand(20))
    # use automatic StrMethodFormatter
    ax.yaxis.set_major_formatter("${x:1.2f}")
    ax.yaxis.set_tick_params(which="major", labelcolor="green", labelleft=False, labelright=True)
    plt.show()
