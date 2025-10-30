from dataclasses import dataclass
from typing import Any

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatVPSSettings(KoswatConfigProtocol):
    """
    Settings related to Vertical Piping Solution reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    polderside_berm_width_vps: float = 0

    def is_valid(self) -> bool:
        return True

    def set_defaults(self, other: "KoswatVPSSettings") -> "KoswatVPSSettings":
        """
        Add the defaults from another KoswatVPSSettings instance to this instance, if not set.

        Args:
            other (KoswatVPSSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatVPSSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatVPSSettings):
            raise TypeError("Can only merge with another KoswatVPSSettings instance.")

        def _set_default(this_value: Any, other_value: Any) -> Any:
            if this_value is None:
                return other_value
            return this_value

        self.active = _set_default(self.active, other.active)
        self.soil_surtax_factor = _set_default(
            self.soil_surtax_factor, other.soil_surtax_factor
        )
        self.constructive_surtax_factor = _set_default(
            self.constructive_surtax_factor, other.constructive_surtax_factor
        )
        self.land_purchase_surtax_factor = _set_default(
            self.land_purchase_surtax_factor, other.land_purchase_surtax_factor
        )
        self.polderside_berm_width_vps = _set_default(
            self.polderside_berm_width_vps, other.polderside_berm_width_vps
        )

        return self
