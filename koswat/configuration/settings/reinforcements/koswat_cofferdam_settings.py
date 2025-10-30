from dataclasses import dataclass
from typing import Any

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


@dataclass
class KoswatCofferdamSettings(KoswatConfigProtocol):
    """
    Settings related to Cofferdam reinforcement
    """

    active: bool = True
    soil_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    constructive_surtax_factor: SurtaxFactorEnum = SurtaxFactorEnum.NORMAAL
    min_length_cofferdam: float = 0
    max_length_cofferdam: float = 99

    def is_valid(self) -> bool:
        return True

    def set_defaults(
        self, other: "KoswatCofferdamSettings"
    ) -> "KoswatCofferdamSettings":
        """
        Add the defaults from another KoswatCofferdamSettings instance to this instance, if not set.

        Args:
            other (KoswatCofferdamSettings): The other instance to get defaults from.

        Raises:
            TypeError: If the other instance has a different type.

        Returns:
            KoswatCofferdamSettings: The instance with defaults set.
        """
        if not isinstance(other, KoswatCofferdamSettings):
            raise TypeError(
                "Can only merge with another KoswatCofferdamSettings instance."
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
        self.min_length_cofferdam = _set_default(
            self.min_length_cofferdam, other.min_length_cofferdam
        )
        self.max_length_cofferdam = _set_default(
            self.max_length_cofferdam, other.max_length_cofferdam
        )

        return self
