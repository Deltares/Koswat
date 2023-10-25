from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile import (
    CofferDamInputProfile,
    PipingWallInputProfile,
    SoilInputProfile,
    StabilityWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile import (
    OutsideSlopeReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.outside_slope_reinforcement_profile_builder import (
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_builder_protocol import (
    ReinforcementProfileBuilderProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard import (
    PipingWallReinforcementProfile,
    SoilReinforcementProfile,
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)

_reinforcements = {
    SoilReinforcementProfile: SoilInputProfile,
    PipingWallReinforcementProfile: PipingWallInputProfile,
    StabilityWallReinforcementProfile: StabilityWallInputProfile,
    CofferdamReinforcementProfile: CofferDamInputProfile,
}


class ReinforcementProfileBuilderFactory:
    base_profile: KoswatProfileBase
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(
        self,
        base_profile: KoswatProfileBase,
        reinforcement_settings: KoswatReinforcementSettings,
        scenario: KoswatScenario,
    ) -> None:
        self.base_profile = base_profile
        self.reinforcement_settings = reinforcement_settings
        self.scenario = scenario

    def build(
        self, reinforcement_profile_type: type[ReinforcementProfileProtocol]
    ) -> ReinforcementProfileProtocol:
        if not reinforcement_profile_type:
            raise ValueError("No specified `reinforcement_profile_type`.")
        _builder = self.get_reinforcement_builder(reinforcement_profile_type)
        _builder.base_profile = self.base_profile
        _builder.scenario = self.scenario
        return _builder.build()

    @staticmethod
    def get_available_reinforcements() -> list[ReinforcementProfileProtocol]:
        """
        Gets all available reinforcements defined in Koswat.

        Returns:
            List[ReinforcementProfileProtocol]: List of reinforcement profile protocols types.
        """
        return list(_reinforcements.keys())

    @staticmethod
    def get_reinforcement_builder(
        reinforcement_profile_type: type[ReinforcementProfileProtocol],
    ) -> ReinforcementProfileBuilderProtocol:
        """
        Gets a valid reinforcement profile `builder` instance (`ReinforcementProfileBuilderProtocol`).

        Args:
            reinforcement_profile_type (Type[ReinforcementProfileProtocol]): Type that requires a builder.

        Raises:
            NotImplementedError: When there is no builder associated to the given `reinforcement_profile_type`.

        Returns:
            ReinforcementProfileBuilderProtocol: Valid instance of a `ReinforcementProfileBuilderProtocol`.
        """
        if issubclass(reinforcement_profile_type, StandardReinforcementProfile):
            _builder = StandardReinforcementProfileBuilder()
            _builder.reinforcement_profile_type = reinforcement_profile_type
            return _builder
        elif issubclass(reinforcement_profile_type, OutsideSlopeReinforcementProfile):
            _builder = OutsideSlopeReinforcementProfileBuilder()
            _builder.reinforcement_profile_type = reinforcement_profile_type
            return _builder
        else:
            raise NotImplementedError(
                f"Type {reinforcement_profile_type} not currently supported."
            )
