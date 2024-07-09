# `pydase_client`

This package is a slim client for `pydase` services, providing you with both synchronous
and asynchronous clients.

## Installation

You can install this package using `pip` or `poetry`:

```bash
pip install git+https://github.com/tiqi-group/pydase_client.git
```

```bash
poetry add git+https://github.com/tiqi-group/pydase_client.git
```

## Synchronous
```python
import pydase_client

with pydase_client.Client("ws://localhost:8001") as client:
    client.set_value("some_property", 10.0))
    print(client.get_value("some_property"))
    client.trigger_method("some_function", args=(), kwargs={"input": "Hello"})
```

You can also leave out the port if it is either 80 (ws) or 443 (wss).

## Asynchronous
```python
import asyncio

import pydase_client


async def do_something() -> None:
    # Using secure websockets
    async with pydase_client.AsyncClient("wss://localhost:443") as client:
        await client.set_value("some_float", 10.2)
        print(await client.get_value("some_float"))
        print(
            await client.trigger_method(
                "some_function", args=(), kwargs={"input": "Hello"}
            )
        )


asyncio.run(do_something())
```

You can also leave out the port if it is either 80 (ws) or 443 (wss).
