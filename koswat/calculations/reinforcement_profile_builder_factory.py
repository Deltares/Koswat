from koswat.calculations.outside_slope_reinforcement import (
    CofferDamInputProfile,
    CofferdamReinforcementProfile,
    OutsideSlopeReinforcementProfile,
    OutsideSlopeReinforcementProfileBuilder,
)
from koswat.calculations.protocols import (
    ReinforcementInputProfileProtocol,
    ReinforcementProfileBuilderProtocol,
    ReinforcementProfileProtocol,
)
from koswat.calculations.standard_reinforcement import (
    PipingWallInputProfile,
    PipingWallReinforcementProfile,
    SoilInputProfile,
    SoilReinforcementProfile,
    StabilityWallInputProfile,
    StabilityWallReinforcementProfile,
    StandardReinforcementProfile,
    StandardReinforcementProfileBuilder,
)

_reinforcements = {
    SoilReinforcementProfile: SoilInputProfile,
    PipingWallReinforcementProfile: PipingWallInputProfile,
    StabilityWallReinforcementProfile: StabilityWallInputProfile,
    CofferdamReinforcementProfile: CofferDamInputProfile,
}


class ReinforcementProfileBuilderFactory:
    @staticmethod
    def get_available_reinforcements() -> list[ReinforcementProfileProtocol]:
        """
        Gets all available reinforcements defined in Koswat.

        Returns:
            List[ReinforcementProfileProtocol]: List of reinforcement profile protocols types.
        """
        return list(_reinforcements.keys())

    @staticmethod
    def get_reinforcement_input_profile(
        reinforcement_profile: ReinforcementProfileProtocol,
    ) -> ReinforcementInputProfileProtocol:
        """
        Gets the appropiate reinforcement input profile (`ReinforcementInputProfileProtocol`) for the given reinforcement profile.

        Args:
            reinforcement_profile (ReinforcementProfileProtocol): Reinforcement profile type that needs an associated input profile.

        Raises:
            NotImplementedError: When the given `reinforcement_profile` (`ReinforcementProfileProtocol`) is not mapped to an existing type.

        Returns:
            ReinforcementInputProfileProtocol: Valid `typing.Type`.
        """
        _input_profile = _reinforcements.get(reinforcement_profile, None)
        if not _input_profile:
            raise NotImplementedError(
                "Reinforcement profile {} not recognized.".format(reinforcement_profile)
            )
        return _input_profile

    @staticmethod
    def get_builder(
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
