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
        # Calculate all possible profiles:
        # grondmaatregel_profile
        # kwelscherm_profile
        # stability_wall_profile
        # chest_dam_profile
        _grondmaatregel_profile = ProfileReinforcement().calculate_new_profile(
            self.base_profile, self.scenario
        )
        return [_grondmaatregel_profile]

    def _get_profile_cost_report_list(self) -> List[ProfileCostReport]:
        _profile_cost_builder = ProfileCostBuilder()
        _profile_cost_builder.base_profile = self.base_profile
        _reports = []
        for _calc_profile in self._get_calculated_profiles():
            _profile_cost_builder.calculated_profile = _calc_profile
            _reports.append(_profile_cost_builder.build())
        return _reports

    def build(self) -> MultipleProfileCostReport:

        _reports = self._get_profile_cost_report_list()
        for _rep in _reports:
            _min_width = _rep.profile.location.x
            pass
