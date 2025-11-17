import math
from typing import Optional

from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class SectionConfigHelper:
    """
    Class with helper methods for configuration sections.
    """

    @staticmethod
    def get_string_without_default(input_val: Optional[str]) -> Optional[str]:
        """
        Returns the input string or None.

        Args:
            input_val (Optional[str]): Input string.

        Returns:
            Optional[str]: Input string or None.
        """
        if input_val is not None:
            return input_val
        return None

    @staticmethod
    def get_string(input_val: Optional[str]) -> str:
        """
        Returns the input string or a default value.

        Args:
            input_val (Optional[str]): Input string.

        Returns:
            str: Input string. Default is an empty string.
        """
        _val = SectionConfigHelper.get_string_without_default(input_val)
        return _val if _val is not None else ""

    @staticmethod
    def get_enum_without_default(
        input_val: Optional[str],
    ) -> Optional[SurtaxFactorEnum]:
        """
        Converts a string to an enum value or None.

        Args:
            input_val (Optional[str]): Input string.

        Returns:
            Optional[SurtaxFactorEnum]: Corresponding enum value or None.
        """
        if input_val:
            return SurtaxFactorEnum[input_val.upper()]
        return None

    @staticmethod
    def get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
        """
        Converts a string to an enum value.

        Args:
            input_val (Optional[str]): Input string.

        Returns:
            SurtaxFactorEnum: Corresponding enum value. Default is SurtaxFactorEnum.NORMAAL.
        """
        _val = SectionConfigHelper.get_enum_without_default(input_val)
        return _val if _val is not None else SurtaxFactorEnum.NORMAAL

    @staticmethod
    def get_float_without_default(
        input_val: Optional[str | float],
    ) -> Optional[float]:
        """
        Converts a string to a float value or None.

        Args:
            input_val (Optional[str | float]): Input string or float.

        Returns:
            Optional[float]: Corresponding float value or None.
        """
        if input_val is not None:
            return float(input_val)
        return None

    @staticmethod
    def get_float(input_val: Optional[str | float]) -> float:
        """
        Converts a string to a float value.

        Args:
            input_val (Optional[str | float]): Input string or float.

        Returns:
            float: Corresponding float value. Default is math.nan.
        """
        _val = SectionConfigHelper.get_float_without_default(input_val)
        return _val if _val is not None else math.nan

    @staticmethod
    def get_bool_without_default(
        input_val: Optional[str | bool],
    ) -> Optional[bool]:
        """
        Converts a string to a boolean value or None.

        Args:
            input_val (Optional[str | bool]): Input string or boolean.

        Returns:
            Optional[bool]: Corresponding boolean value or None.
        """
        if input_val is not None:
            if isinstance(input_val, bool):
                return input_val
            return input_val.lower() == "true"
        return None

    @staticmethod
    def get_bool(input_val: Optional[str | bool]) -> bool:
        """
        Converts a string to a boolean value.

        Args:
            input_val (Optional[str | bool]): Input string or boolean.

        Returns:
            bool: Corresponding boolean value. Default is False.
        """
        _val = SectionConfigHelper.get_bool_without_default(input_val)
        return _val if _val is not None else False
