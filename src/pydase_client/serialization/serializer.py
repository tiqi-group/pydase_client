from __future__ import annotations

import inspect
import logging
import sys
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

import pydase_client.units as u

if TYPE_CHECKING:
    from pydase_client.serialization.types import (
        SerializedBool,
        SerializedDict,
        SerializedEnum,
        SerializedFloat,
        SerializedInteger,
        SerializedList,
        SerializedNoneType,
        SerializedObject,
        SerializedQuantity,
        SerializedString,
    )

logger = logging.getLogger(__name__)


def get_attribute_doc(attr: Any) -> str | None:
    """This function takes an input attribute attr and returns its documentation
    string if it's different from the documentation of its type, otherwise,
    it returns None.
    """
    attr_doc = inspect.getdoc(attr)
    attr_class_doc = inspect.getdoc(type(attr))
    return attr_doc if attr_class_doc != attr_doc else None


class SerializationError(Exception):
    pass


class Serializer:
    @staticmethod
    def serialize_object(obj: Any, access_path: str = "") -> SerializedObject:
        result: SerializedObject

        if isinstance(obj, list):
            result = Serializer._serialize_list(obj, access_path=access_path)

        elif isinstance(obj, dict):
            result = Serializer._serialize_dict(obj, access_path=access_path)

        # Special handling for u.Quantity
        elif isinstance(obj, u.Quantity):
            result = Serializer._serialize_quantity(obj, access_path=access_path)

        # Handling for Enums
        elif isinstance(obj, Enum):
            result = Serializer._serialize_enum(obj, access_path=access_path)

        elif isinstance(obj, int | float | bool | str | None):
            result = Serializer._serialize_primitive(obj, access_path=access_path)

        try:
            return result
        except UnboundLocalError:
            raise SerializationError(
                f"Could not serialized object of type {type(obj)}."
            )

    @staticmethod
    def _serialize_primitive(
        obj: float | bool | str | None,
        access_path: str,
    ) -> (
        SerializedInteger
        | SerializedFloat
        | SerializedBool
        | SerializedString
        | SerializedNoneType
    ):
        doc = get_attribute_doc(obj)
        return {  # type: ignore
            "full_access_path": access_path,
            "doc": doc,
            "readonly": False,
            "type": type(obj).__name__,
            "value": obj,
        }

    @staticmethod
    def _serialize_enum(obj: Enum, access_path: str = "") -> SerializedEnum:
        value = obj.name
        doc = obj.__doc__
        class_name = type(obj).__name__
        if sys.version_info < (3, 11) and doc == "An enumeration.":
            doc = None
        obj_type: Literal["ColouredEnum", "Enum"] = "Enum"

        return {
            "full_access_path": access_path,
            "name": class_name,
            "type": obj_type,
            "value": value,
            "readonly": False,
            "doc": doc,
            "enum": {
                name: member.value for name, member in obj.__class__.__members__.items()
            },
        }

    @staticmethod
    def _serialize_quantity(
        obj: u.Quantity, access_path: str = ""
    ) -> SerializedQuantity:
        doc = get_attribute_doc(obj)
        value: u.QuantityDict = {"magnitude": obj.m, "unit": str(obj.u)}
        return {
            "full_access_path": access_path,
            "type": "Quantity",
            "value": value,
            "readonly": False,
            "doc": doc,
        }

    @staticmethod
    def _serialize_dict(obj: dict[str, Any], access_path: str = "") -> SerializedDict:
        readonly = False
        doc = get_attribute_doc(obj)
        value = {}
        for key, val in obj.items():
            value[key] = Serializer.serialize_object(
                val, access_path=f'{access_path}["{key}"]'
            )
        return {
            "full_access_path": access_path,
            "type": "dict",
            "value": value,
            "readonly": readonly,
            "doc": doc,
        }

    @staticmethod
    def _serialize_list(obj: list[Any], access_path: str = "") -> SerializedList:
        readonly = False
        doc = get_attribute_doc(obj)
        value = [
            Serializer.serialize_object(o, access_path=f"{access_path}[{i}]")
            for i, o in enumerate(obj)
        ]
        return {
            "full_access_path": access_path,
            "type": "list",
            "value": value,
            "readonly": readonly,
            "doc": doc,
        }


def create_empty_serialized_object() -> SerializedObject:
    """Create a new empty serialized object."""

    return {
        "full_access_path": "",
        "value": None,
        "type": "None",
        "doc": None,
        "readonly": False,
    }


def dump(obj: Any) -> SerializedObject:
    return Serializer.serialize_object(obj)
