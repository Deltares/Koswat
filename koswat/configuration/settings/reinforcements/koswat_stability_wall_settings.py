from dataclasses import dataclass
from typing import Any

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatStabilityWallSettings(KoswatConfigProtocol):
    """
    Settings related to Stability wall reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    steepening_polderside_slope: float = 0
    min_length_stability_wall: float = 0
    transition_sheetpile_diaphragm_wall: float = 99
    max_length_stability_wall: float = 99

    def is_valid(self) -> bool:
        return True

    def set_defaults(
        self,
        other: "KoswatStabilityWallSettings",
    ) -> "KoswatStabilityWallSettings":
        """
        Add the defaults from another KoswatStabilityWallSettings instance to this instance, if not set.

        Args:
            other (KoswatStabilityWallSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatStabilityWallSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatStabilityWallSettings):
            raise TypeError(
                "Can only merge with another KoswatStabilityWallSettings instance."
            )

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
        self.steepening_polderside_slope = _set_default(
            self.steepening_polderside_slope, other.steepening_polderside_slope
        )
        self.min_length_stability_wall = _set_default(
            self.min_length_stability_wall, other.min_length_stability_wall
        )
        self.transition_sheetpile_diaphragm_wall = _set_default(
            self.transition_sheetpile_diaphragm_wall,
            other.transition_sheetpile_diaphragm_wall,
        )
        self.max_length_stability_wall = _set_default(
            self.max_length_stability_wall, other.max_length_stability_wall
        )

        return self
