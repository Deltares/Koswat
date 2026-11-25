"""
                GNU GENERAL PUBLIC LICENSE
                  Version 3, 29 June 2007

KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
Copyright (C) 2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
from dataclasses import replace

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike_reinforcements.input_profile import (
    CofferdamInputProfile,
    PipingWallInputProfile,
    SoilInputProfile,
    SoilWatersideInputProfile,
    StabilityWallCrestInputProfile,
    StabilityWallToeInputProfile,
    VPSInputProfile,
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
    SoilWatersideReinforcementProfile,
    StabilityWallCrestReinforcementProfile,
    StabilityWallToeReinforcementProfile,
    VPSReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile import (
    StandardReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.standard_reinforcement_profile_builder import (
    StandardReinforcementProfileBuilder,
)

_reinforcements = {
    SoilReinforcementProfile: SoilInputProfile,
    SoilWatersideReinforcementProfile: SoilWatersideInputProfile,
    VPSReinforcementProfile: VPSInputProfile,
    PipingWallReinforcementProfile: PipingWallInputProfile,
    StabilityWallToeReinforcementProfile: StabilityWallToeInputProfile,
    StabilityWallCrestReinforcementProfile: StabilityWallCrestInputProfile,
    CofferdamReinforcementProfile: CofferdamInputProfile,
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
        _builder.reinforcement_settings = self.reinforcement_settings
        _builder.scenario = self._get_scenario(reinforcement_profile_type)
        return _builder.build()

    def _get_scenario(
        self, reinforcement_profile_type: type[ReinforcementProfileProtocol]
    ) -> KoswatScenario:
        """
        Gets the scenario to be used for the given reinforcement type.
        When a factor_settlement is defined, d_h is multiplied by it.
        Only the waterside soil reinforcement gets an adjusted waterside_slope;
        all other reinforcements use the original scenario.
        Quick fix, should be improved in the future.
        """
        _scenario = replace(self.scenario)
        if issubclass(reinforcement_profile_type, SoilWatersideReinforcementProfile):
            _scenario.waterside_slope += 0.01
        _factor_settlement = self.base_profile.input_data.factor_settlement
        if not math.isnan(_factor_settlement):
            _scenario.d_h *= _factor_settlement
        return _scenario

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
