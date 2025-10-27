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

    @classmethod
    @abc.abstractmethod
    def from_ini(cls, ini_config: SectionProxy) -> "ConfigSectionFomBase":
        """
        Create an instance of the class from an INI configuration section.

        Args:
            ini_config (SectionProxy): Section containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> "ConfigSectionFomBase":
        """
        Create an instance of the class from a dictionary (e.g., from JSON).
        Note no defaults are assigned here, so missing values will be None.
        Reason for this is to avoid overriding defaults from other configuration layers.

        Args:
            input_dict (dict): Dictionary containing the configuration.

        Returns:
            FileObjectModelProtocol: The created instance.
        """

    def _set_float_values(
        self,
        config: dict[str, Any],
        mappings: dict[str, str],
        default: Optional[float] = None,
    ) -> None:
        for key, attr in mappings.items():
            _input_value = config.get(key, default)
            setattr(
                self,
                attr,
                (
                    float(config.get(key, default))
                    if _input_value != default
                    else default
                ),
            )

    def _set_surtax_factor_values(
        self,
        config: dict[str, Any],
        mappings: dict[str, str],
        default: Optional[SurtaxFactorEnum] = None,
    ) -> None:
        for key, attr in mappings.items():
            _input_str = config.get(key, default.name if default else None)
            setattr(
                self,
                attr,
                SurtaxFactorEnum[_input_str.upper()] if _input_str else default,
            )

    def set_defaults(self, defaults: "ConfigSectionFomBase") -> "ConfigSectionFomBase":
        """
        Override current settings with defaults where current settings are missing.

        Args:
            defaults (ConfigSectionFomBase): Object containing default settings.

        Returns:
            ConfigSectionFomBase: Object with settings overridden by defaults, where needed.
        """
        for _key, _value in defaults.__dict__.items():
            if getattr(self, _key) in ("", None, math.nan):
                setattr(self, _key, _value)
        return self
