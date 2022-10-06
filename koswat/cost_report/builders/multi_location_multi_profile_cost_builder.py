from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.profile_reinforcement import ProfileReinforcementCalculation
from koswat.cost_report.builders.multi_location_profile_cost_builder import (
    MultiLocationProfileCostBuilder,
)
from koswat.cost_report.reports.koswat_report import (
    KoswatSummary,
)
from koswat.koswat_scenario import KoswatScenario
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiLocationMultiProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings
    base_profile: KoswatProfileBase
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.scenario = None

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

    def _get_multi_location_profile_cost_builder(
        self,
    ) -> MultiLocationProfileCostBuilder:
        _builder = MultiLocationProfileCostBuilder()
        _builder.base_profile = self.base_profile
        _builder.surroundings = self.surroundings
        return _builder

    def build(self) -> KoswatSummary:
        _summary = KoswatSummary()
        _mlpc_builder = self._get_multi_location_profile_cost_builder()
        for _calc_profile in self._get_calculated_profiles():
            _mlpc_builder.calc_profile = _calc_profile
            _summary.locations_profile_report_list.append(_mlpc_builder.build())
        return _summary
