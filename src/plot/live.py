import logging
import sys
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing_extensions import Generator, NoReturn

_logger = logging.getLogger(__name__)


class SinAnimationState:
    def __init__(self, fig: Figure) -> None:
        self.ax = fig.add_subplot()
        self.xdata = deque[float]()
        self.ydata = deque[float]()
        self.line, *_ = self.ax.plot(self.xdata, self.ydata, "ro")
        self.logger = _logger.getChild(self.__class__.__name__)

    def init(self) -> tuple[Axes]:
        self.ax.set_xlim(0, 2 * np.pi)
        self.ax.set_ylim(-1.2, 1.2)
        self.logger.debug("init")
        return (self.ax,)

    def update(self, frame: float) -> tuple[Axes]:
        x, y = frame, np.sin(frame)
        self.logger.debug(f"update {x=}, {y=}")
        self.xdata.append(x)
        self.ydata.append(y)
        if x > 2 * np.pi:
            xleft = self.xdata.popleft()
            self.ydata.popleft()
            self.ax.set_xlim(xleft, x)
        self.line.set_data(self.xdata, self.ydata)
        return (self.ax,)

    def frames(self) -> Generator[float, None, NoReturn]:
        v = 0.0
        while True:
            self.logger.debug("generate frame")
            yield v
            v += 0.1


def sinwave() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    fig = plt.figure()
    state = SinAnimationState(fig)
    _ani = FuncAnimation(
        fig, state.update, frames=state.frames, init_func=state.init, blit=True, save_count=10, interval=50
    )
    plt.show()
