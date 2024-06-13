import asyncio
import logging
import sys

from aiochannel import Channel

logger = logging.getLogger(__name__)


async def ping(tx: Channel[str], count: int = 10, delay: float = 1) -> None:
    for i in range(1, count + 1):
        await asyncio.sleep(delay)
        await tx.put(f"Hello {i}")
        logger.info(f"put {i}")


async def pong(rx: Channel[str]) -> None:
    async for msg in rx:
        assert isinstance(msg, str)
        logger.info(f"receive '{msg}'")


async def ping_pong() -> None:
    logger.info("starting ping-pong...")
    ch: Channel[str] = Channel(10)
    ping_task = asyncio.create_task(ping(ch))
    pong_task = asyncio.create_task(pong(ch))
    await asyncio.wait([ping_task, pong_task], return_when=asyncio.FIRST_COMPLETED)
    logger.info("done!")


def run_ping_pong() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    logger.setLevel(logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    asyncio.run(ping_pong())
