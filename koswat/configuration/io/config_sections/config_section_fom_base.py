import abc
import math
from configparser import SectionProxy
from typing import Any, Optional

from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class ConfigSectionFomBase(FileObjectModelProtocol, abc.ABC):
    """
    Base class for configuration section file object models.
    """

    _surtax_mappings: dict
    _float_mappings: dict

    @staticmethod
    def _get_surtax_factor(input_str: Optional[str]) -> SurtaxFactorEnum:
        if not input_str:
            return SurtaxFactorEnum.NORMAAL
        return SurtaxFactorEnum[input_str.upper()]

    @classmethod
    def from_ini(cls, ini_config: SectionProxy) -> FileObjectModelProtocol:
        """
        Create an instance of the class from an INI configuration section.

        Args:
            ini_config (SectionProxy): Section containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """
        _section = cls()
        for key, attr in cls._float_mappings.items():
            setattr(_section, attr, ini_config.getfloat(key, fallback=math.nan))
        for key, attr in cls._surtax_mappings.items():
            setattr(_section, attr, cls._get_surtax_factor(ini_config.get(key, None)))

        return _section

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> FileObjectModelProtocol:
        """
        Create an instance of the class from a dictionary (e.g., from JSON).
        Note no defaults are assigned here, so missing values will be None.
        Reason for this is to avoid overriding defaults from other configuration layers.

        Args:
            input_dict (dict): Dictionary containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """
        _section = cls()
        for key, attr in cls._float_mappings.items():
            setattr(
                _section,
                attr,
                float(input_dict.get(key)) if key in input_dict else None,
            )
        for key, attr in cls._surtax_mappings.items():
            setattr(
                _section,
                attr,
                (
                    cls._get_surtax_factor(input_dict.get(key))
                    if key in input_dict
                    else None
                ),
            )

        return _section
