# `pydase_client`

This package is a slim client for `pydase` services, providing you with both synchronous
and asynchronous clients.

## Synchronous
```python
import pydase_client

with pydase_client.Client("ws://localhost:8001") as client:
    print(client.get_value("some_property"))
    client.set_value("some_property", 10.0))
```

You can also leave out the port if it is either 80 (ws) or 443 (wss).

## Asynchronous
```python
import asyncio

import pydase_client


async def do_something() -> None:
    async with pydase_client.AsyncClient("wss://localhost:443") as client:
        print(await client.get_value("some_property"))
        client.set_value("some_property", 10.0))


asyncio.run(do_something())
```

You can also leave out the port if it is either 80 (ws) or 443 (wss).
