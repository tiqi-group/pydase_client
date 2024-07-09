import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class QuantityDict(TypedDict):
    magnitude: int | float
    unit: str


try:
    import pint  # type: ignore

    units: pint.UnitRegistry = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
    units.default_format = "~P"  # pretty and short format

    Quantity = pint.Quantity  # type: ignore
    Unit = units.Unit

    def convert_to_quantity(  # type: ignore
        value: QuantityDict | float | Quantity,  # type: ignore
        unit: str = "",
    ) -> Quantity:  # type: ignore
        """
        Convert a given value into a pint.Quantity object with the specified unit.

        Args:
            value (QuantityDict | float | int | Quantity):
                The value to be converted into a Quantity object.
                - If value is a float or int, it will be directly converted to the
                specified unit.
                - If value is a dict, it must have keys 'magnitude' and 'unit' to
                represent the value and unit.
                - If value is a Quantity object, it will remain unchanged.\n
            unit (str, optional): The target unit for conversion. If empty and value is
                not a Quantity object, it will assume a unitless quantity.

        Returns:
            Quantity: The converted value as a pint.Quantity object with the specified
                unit.

        Examples:
            >>> convert_to_quantity(5, 'm')
            <Quantity(5.0, 'meters')>
            >>> convert_to_quantity({'magnitude': 10, 'unit': 'mV'})
            <Quantity(10.0, 'millivolt')>
            >>> convert_to_quantity(10.0 * u.units.V)
            <Quantity(10.0, 'volt')>

        Notes:
            - If unit is not provided and value is a float or int, the resulting
            Quantity will be unitless.
        """

        if isinstance(value, int | float):
            quantity = float(value) * Unit(unit)
        elif isinstance(value, dict):
            quantity = float(value["magnitude"]) * Unit(value["unit"])
        else:
            quantity = value
        return quantity
except ImportError:

    class Quantity:  # type: ignore
        def __init__(self, value: float, unit: str) -> None:
            self.m = 0
            self.u = ""
            raise RuntimeError("To use quantities, please install `pint`.")

    def convert_to_quantity(
        value: QuantityDict | float | Quantity,  # type: ignore
        unit: str = "",
    ) -> Quantity:  # type: ignore
        raise RuntimeError("To use quantities, please install `pint`.")
