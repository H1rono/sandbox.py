import asyncio
import logging
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from typing import Any

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


class ChanAnimationHandle:
    Frame = tuple[float, float]

    def __init__(self, loop: asyncio.AbstractEventLoop, ax: Axes, rx: aiochannel.Channel[Frame]) -> None:
        self._loop = loop
        self._ax = ax
        self._xdata = deque[float]()
        self._ydata = deque[float]()
        self._line, *_ = self._ax.plot(self._xdata, self._ydata, "bo")
        self._rx = rx
        self._logger = _logger.getChild(self.__class__.__name__)
        xlim_l, xlim_r = self._ax.get_xlim()
        self._init_xrange = xlim_r - xlim_l

    def init(self) -> tuple[Axes]:
        return (self._ax,)

    def frames(self) -> Generator[Frame | None, None, NoReturn]:
        while True:
            try:
                frame_future = asyncio.run_coroutine_threadsafe(self._rx.get(), self._loop)
                yield frame_future.result(0.02)
            except TimeoutError:
                yield None
            finally:
                self._logger.debug("frame")

    def update(self, frame: Frame | None) -> tuple[Axes]:
        if frame is None:
            return (self._ax,)
        x, y = frame
        self._xdata.append(x)
        self._ydata.append(y)
        xmin, xmax = min(self._xdata), max(self._xdata)
        if self._init_xrange < xmax - xmin:
            self._xdata.popleft()
            self._ydata.popleft()
            self._ax.set_xlim(xmin, xmax)
        self._line.set_data(self._xdata, self._ydata)
        self._logger.debug("update")
        return (self._ax,)

    def show(self, fig: Figure, *args: Any, **kwargs: Any) -> None:
        kwargs["init_func"] = self.init
        kwargs["frames"] = self.frames
        _ani = FuncAnimation(fig, self.update, *args, **kwargs)
        plt.show()


async def channel_anime_frames(tx: aiochannel.Channel[ChanAnimationHandle.Frame], terminate: Event) -> None:
    x = 0.0
    while not terminate.is_set():
        y = np.exp(np.sin(x))
        try:
            await asyncio.wait_for(tx.put((x, y)), 0.1)
        except asyncio.TimeoutError:
            continue
        _logger.debug("generate")
        x += 0.1
        await asyncio.sleep(0.01)


def run_ch_anime_frames(
    loop: asyncio.AbstractEventLoop, tx: aiochannel.Channel[ChanAnimationHandle.Frame], terminate: Event
) -> None:
    loop.run_until_complete(channel_anime_frames(tx, terminate))


def channel_anime() -> None:
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 3)
    ch: aiochannel.Channel[tuple[float, float]] = aiochannel.Channel(10)
    loop = asyncio.get_event_loop()
    terminate = Event()

    handle = ChanAnimationHandle(loop, ax, ch)

    with ThreadPoolExecutor() as pool:
        fut = pool.submit(run_ch_anime_frames, loop, ch, terminate)
        handle.show(fig, save_count=10, interval=50)
        terminate.set()
        fut.result(1)
