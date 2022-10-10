from typing import List, Type

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations import (
    PipingWallReinforcementProfileCalculation,
    ReinforcementProfileCalculationProtocol,
    ReinforcementProfileProtocol,
    SoilReinforcementProfileCalculation,
    StabilityWallReinforcementProfileCalculation,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_builder import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper
from koswat.koswat_scenario import KoswatScenario


class KoswatSummaryBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper
    base_profile: KoswatProfileBase
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.scenario = None

    def _get_calculated_profile(
        self, builder_type: Type[ReinforcementProfileCalculationProtocol]
    ) -> ReinforcementProfileProtocol:
        _builder = builder_type()
        _builder.base_profile = self.base_profile
        _builder.scenario = self.scenario
        return _builder.build()

    def _get_calculated_profile_list(self) -> List[ReinforcementProfileProtocol]:
        _profile_calculations = [
            SoilReinforcementProfileCalculation,
            PipingWallReinforcementProfileCalculation,
            StabilityWallReinforcementProfileCalculation,
        ]
        # kwelscherm_profile
        # chest_dam_profile
        return list(map(self._get_calculated_profile, _profile_calculations))

    def _get_multi_location_profile_cost_builder(
        self,
    ) -> MultiLocationProfileCostReportBuilder:
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.base_profile = self.base_profile
        _builder.surroundings = self.surroundings
        return _builder

    def build(self) -> KoswatSummary:
        _summary = KoswatSummary()
        _mlpc_builder = self._get_multi_location_profile_cost_builder()
        for _calc_profile in self._get_calculated_profile_list():
            _mlpc_builder.calc_profile = _calc_profile
            _summary.locations_profile_report_list.append(_mlpc_builder.build())
        return _summary
