import math
from typing import Optional

from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class SectionConfigHelper:
    """
    Class with helper methods for configuration sections.
    """

    @staticmethod
    def get_string(
        input_val: Optional[str], set_default: Optional[bool] = True
    ) -> Optional[str]:
        """
        Returns the input string or a default value.

        Args:
            input_val (Optional[str]): Input string.
            set_default (bool): Whether to set a default value.

        Returns:
            Optional[str]: Input string or default value.
        """
        if input_val is not None:
            return input_val
        return "" if set_default else None

    @staticmethod
    def get_enum(
        input_val: Optional[str], set_default: Optional[bool] = True
    ) -> Optional[SurtaxFactorEnum]:
        """
        Converts a string to an enum value.

        Args:
            input_val (Optional[str]): Input string.
            set_default (bool): Whether to set a default value.

        Returns:
            Optional[SurtaxFactorEnum]: Corresponding enum value or None.
        """
        if input_val:
            return SurtaxFactorEnum[input_val.upper()]
        return SurtaxFactorEnum.NORMAAL if set_default else None

    @staticmethod
    def get_float(
        input_val: Optional[str | float], set_default: Optional[bool] = True
    ) -> Optional[float]:
        """
        Converts a string to a float value.

        Args:
            input_val (Optional[str]): Input string.
            set_default (bool): Whether to set a default value.

        Returns:
            Optional[float]: Corresponding float value or None.
        """
        if input_val is not None:
            return float(input_val)
        return math.nan if set_default else None

    @staticmethod
    def get_bool(
        input_val: Optional[str | bool], set_default: Optional[bool] = True
    ) -> Optional[bool]:
        """
        Converts a string to a boolean value.

        Args:
            input_val (Optional[str]): Input string.
            set_default (bool): Whether to set a default value.

        Returns:
            Optional[bool]: Corresponding boolean value or None.
        """
        if input_val is not None:
            if isinstance(input_val, bool):
                return input_val
            return input_val.lower() == "true"
        return False if set_default else None
