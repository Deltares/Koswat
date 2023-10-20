from koswat.calculations.reinforcement_profiles.standard_reinforcement.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.calculations.reinforcement_profiles.standard_reinforcement.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)


class SoilReinforcementProfile(StandardReinforcementProfile):
    input_data: SoilInputProfile

    def __str__(self) -> str:
        return "Grondmaatregel profiel"
