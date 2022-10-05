from typing import Dict, List

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.profile_calculation_protocol import ProfileCalculationProtocol
from koswat.calculations.profile_cost_builder import ProfileCostBuilder
from koswat.calculations.profile_reinforcement import ProfileReinforcement
from koswat.koswat_report import MultipleProfileCostReport, ProfileCostReport
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfile
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings
    base_profile: KoswatProfile
    scenario: KoswatScenario

    def _get_calculated_profiles(self) -> List[KoswatProfile]:
        _grondmaatregel_profile = ProfileReinforcement().calculate_new_profile(
            self.base_profile, self.scenario
        )
        return [_grondmaatregel_profile]

    def build(self) -> MultipleProfileCostReport:
        _classified_surroundings = (
            self.surroundings.buldings_polderside.get_classify_surroundings()
        )
        # Calculate all possible profiles:
        # grondmaatregel_profile
        _profiles_report = self._get_calculated_profiles()
        # kwelscherm_profile
        # stability_wall_profile
        # chest_dam_profile
        # for (
        #     _distance_to_building,
        #     profile_locations,
        # ) in _classified_surroundings.items():
        #     if _distance_to_building > _grondmaatregel_profile.points[-1].x:
        #         # _Grondmaatregel applies here.
        #         pass

        # _cost_report = ProfileReinforcementCostBuilder().get_profile_cost_report(
        #         self.base_profile, _new_polder_profile
        #     )
