from dataclasses import dataclass
from typing import Any

from numpy import isin

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatPipingWallSettings(KoswatConfigProtocol):
    """
    Settings related to Piping wall reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    land_purchase_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_length_piping_wall: float = 0
    transition_cbwall_sheetpile: float = 99
    max_length_piping_wall: float = 99

    def is_valid(self) -> bool:
        return True

    def set_defaults(
        self, other: "KoswatPipingWallSettings"
    ) -> "KoswatPipingWallSettings":
        """
        Add the defaults from another KoswatPipingWallSettings instance to this instance, if not set.

        Args:
            other (KoswatPipingWallSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatPipingWallSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatPipingWallSettings):
            raise TypeError(
                "Can only merge with another KoswatPipingWallSettings instance."
            )

        def _set_default(this_value: Any, other_value: Any) -> Any:
            if this_value is None:
                return other_value
            return this_value

        self.soil_surtax_factor = _set_default(
            self.soil_surtax_factor, other.soil_surtax_factor
        )
        self.constructive_surtax_factor = _set_default(
            self.constructive_surtax_factor, other.constructive_surtax_factor
        )
        self.land_purchase_surtax_factor = _set_default(
            self.land_purchase_surtax_factor, other.land_purchase_surtax_factor
        )
        self.min_length_piping_wall = _set_default(
            self.min_length_piping_wall, other.min_length_piping_wall
        )
        self.transition_cbwall_sheetpile = _set_default(
            self.transition_cbwall_sheetpile, other.transition_cbwall_sheetpile
        )
        self.max_length_piping_wall = _set_default(
            self.max_length_piping_wall, other.max_length_piping_wall
        )

        return self
