import asyncio
import logging
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import aiochannel
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


def channel_anime() -> None:
    logger = _logger.getChild("channel_anime")
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    fig, ax = plt.subplots()
    ch: aiochannel.Channel[tuple[float, float]] = aiochannel.Channel(10)
    xdata, ydata = deque[float](), deque[float]()
    (line,) = ax.plot(xdata, ydata, "bo")
    loop = asyncio.get_event_loop()
    terminate = Event()

    async def data_gen() -> None:
        x = 0.0
        while not terminate.is_set():
            y = np.exp(np.sin(x))
            try:
                await asyncio.wait_for(ch.put((x, y)), 0.1)
            except asyncio.TimeoutError:
                continue
            logger.info("generate")
            x += 0.1
            await asyncio.sleep(0.01)

    def init() -> tuple[Axes]:
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(0, 3.0)
        return (ax,)

    def update(frame: tuple[float, float] | None) -> tuple[Axes]:
        if frame is None:
            return (ax,)
        x, y = frame
        xdata.append(x)
        ydata.append(y)
        # xが単調増加だと仮定する
        if x > 2 * np.pi:
            xleft = xdata.popleft()
            ydata.popleft()
            ax.set_xlim(xleft, x)
        line.set_data(xdata, ydata)
        logger.info("update")
        return (ax,)

    def frames() -> Generator[tuple[float, float] | None, None, NoReturn]:
        while True:
            try:
                frame_future = asyncio.run_coroutine_threadsafe(ch.get(), loop)
                yield frame_future.result(0.02)
            except TimeoutError:
                yield None
            finally:
                logger.info("frame")

    def run_data_gen() -> None:
        loop.run_until_complete(data_gen())
        logger.info("done data_gen")

    def show() -> None:
        _ani = FuncAnimation(fig, update, frames=frames, init_func=init, save_count=10, interval=50)
        plt.show()

    with ThreadPoolExecutor() as pool:
        fut = pool.submit(run_data_gen)
        show()
        terminate.set()
        logger.info("wait future")
        fut.result(1)
