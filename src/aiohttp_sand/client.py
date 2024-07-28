import asyncio

import aiohttp


async def request_test() -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://github.com/H1rono.keys") as response,
    ):
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        text = await response.text()
        print("Body:", text[:15])


def run_request_test() -> None:
    asyncio.run(request_test())
