import asyncio

import pydase_client


async def do_something() -> None:
    async with pydase_client.AsyncClient("ws://localhost:8001") as client:
        await client.set_value("some_float", 10.2)
        print(await client.get_value("some_float"))
        print(
            await client.trigger_method(
                "some_function", args=(), kwargs={"input": "Hello"}
            )
        )


asyncio.run(do_something())
