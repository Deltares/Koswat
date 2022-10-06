from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.profile_cost_builder import ProfileCostBuilder
from koswat.calculations.profile_reinforcement import ProfileReinforcementCalculation
from koswat.koswat_report import MultiLocationProfileCostReport
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiLocationProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings = None
    base_profile: KoswatProfileBase = None
    scenario: KoswatScenario = None

    def _get_calculated_profiles(self) -> List[KoswatProfileBase]:
        # Calculate all possible profiles:
        # grondmaatregel_profile
        _grondmaatregel_profile = (
            ProfileReinforcementCalculation().calculate_new_profile(
                self.base_profile, self.scenario
            )
        )
        # kwelscherm_profile
        # stability_wall_profile
        # chest_dam_profile
        return [_grondmaatregel_profile]

    def _get_profile_cost_report_list(self) -> List[MultiLocationProfileCostReport]:
        _profile_cost_builder = ProfileCostBuilder()
        _profile_cost_builder.base_profile = self.base_profile
        _reports = []
        for _calc_profile in self._get_calculated_profiles():
            _profile_cost_builder.calculated_profile = _calc_profile
            _profile_report = _profile_cost_builder.build()
            _multiple_location_cost_report = MultiLocationProfileCostReport()
            _multiple_location_cost_report.locations = (
                self.surroundings.buldings_polderside.get_locations_after_distance(
                    _calc_profile.profile_width
                )
            )
            _multiple_location_cost_report.profile_cost_report = _profile_report
            _reports.append(_multiple_location_cost_report)
        return _reports

    def build(self) -> List[MultiLocationProfileCostReport]:
        return self._get_profile_cost_report_list()
