import logging
import sys
from types import TracebackType
from typing import TYPE_CHECKING, Any

from pydase_client.serialization.deserializer import loads

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

import socketio  # type: ignore

from pydase_client.serialization.serializer import dump

if TYPE_CHECKING:
    from pydase_client.serialization.types import SerializedObject

logger = logging.getLogger(__name__)


class AsyncClient:
    def __init__(
        self,
        url: str,
    ):
        self._url = url
        self._sio = socketio.AsyncClient()
        self._sio.on("connect", self._handle_connect)
        self._sio.on("disconnect", self._handle_disconnect)

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __adel__(self) -> None:
        await self.disconnect()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.disconnect()

    async def _handle_connect(self) -> None:
        logger.debug("Connected")

    async def _handle_disconnect(self) -> None:
        logger.debug("Disconnected")

    async def connect(self) -> None:
        if not self._sio.connected:
            await self._sio.connect(
                self._url,
                socketio_path="/ws/socket.io",
                transports=["websocket"],
                retry=False,
            )

    async def disconnect(self) -> None:
        if self._sio.connected:
            await self._sio.disconnect()

    async def get_value(self, full_access_path: str) -> Any:
        serialized_value: SerializedObject | None = await self._sio.call(
            "get_value", full_access_path
        )
        if serialized_value is not None:
            return loads(serialized_value)
        return None

    async def set_value(self, full_access_path: str, new_value: Any) -> Any:
        return await self._sio.call(
            "update_value",
            {
                "access_path": full_access_path,
                "value": dump(new_value),
            },
        )

    async def trigger_method(
        self,
        full_access_path: str,
        *,
        args: tuple[Any] = (),  # type: ignore
        kwargs: dict[str, Any] = {},
    ) -> Any:
        result = await self._sio.call(
            "trigger_method",
            {
                "access_path": full_access_path,
                "args": dump(list(args)),
                "kwargs": dump(kwargs),
            },
        )

        if result is not None:
            return loads(serialized_object=result)

        return None
