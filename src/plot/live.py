from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from typing_extensions import Any, Generator, NoReturn


def sinwave() -> None:
    fig, ax = plt.subplots()
    xdata, ydata = deque[float](), deque[float]()
    (line,) = ax.plot(ydata, ydata, "ro")

    def init() -> tuple[Axes]:
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-1, 1)
        return (ax,)

    def frames() -> Generator[float, Any, NoReturn]:
        v = 0.0
        while True:
            yield v
            v += 0.1

    def update(frame: float) -> tuple[Axes]:
        xdata.append(frame)
        ydata.append(np.sin(frame))
        if frame > 2 * np.pi:
            xleft = xdata.popleft()
            ydata.popleft()
            ax.set_xlim(xleft, frame)
            ax.tick_params("x", reset=True)
        line.set_data(xdata, ydata)
        return (ax,)

    _ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, save_count=10, interval=50)
    plt.show()
