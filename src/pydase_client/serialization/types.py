from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    import pydase.units as u  # type: ignore

logger = logging.getLogger(__name__)


class SignatureDict(TypedDict):
    parameters: dict[str, dict[str, Any]]
    return_annotation: dict[str, Any]


class SerializedObjectBase(TypedDict):
    full_access_path: str
    doc: str | None
    readonly: bool


class SerializedInteger(SerializedObjectBase):
    value: int
    type: Literal["int"]


class SerializedFloat(SerializedObjectBase):
    value: float
    type: Literal["float"]


class SerializedQuantity(SerializedObjectBase):
    value: u.QuantityDict
    type: Literal["Quantity"]


class SerializedBool(SerializedObjectBase):
    value: bool
    type: Literal["bool"]


class SerializedString(SerializedObjectBase):
    value: str
    type: Literal["str"]


class SerializedEnum(SerializedObjectBase):
    name: str
    value: str
    type: Literal["Enum", "ColouredEnum"]
    enum: dict[str, Any]


class SerializedList(SerializedObjectBase):
    value: list[SerializedObject]
    type: Literal["list"]


class SerializedDict(SerializedObjectBase):
    value: dict[str, SerializedObject]
    type: Literal["dict"]


class SerializedNoneType(SerializedObjectBase):
    value: None
    type: Literal["NoneType"]


class SerializedNoValue(SerializedObjectBase):
    value: None
    type: Literal["None"]


SerializedObject = (
    SerializedBool
    | SerializedFloat
    | SerializedInteger
    | SerializedString
    | SerializedList
    | SerializedDict
    | SerializedNoneType
    | SerializedEnum
    | SerializedQuantity
    | SerializedNoValue
)
