import logging
from typing import List

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations import (
    ReinforcementProfileBuilderFactory,
    ReinforcementProfileProtocol,
)
from koswat.configuration.settings import KoswatScenario
from koswat.cost_report.multi_location_profile import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


class KoswatSummaryBuilder(BuilderProtocol):
    surroundings: SurroundingsWrapper
    base_profile: KoswatProfileBase
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.scenario = None

    def _get_calculated_profile_list(self) -> List[ReinforcementProfileProtocol]:
        _available_reinforcements = (
            ReinforcementProfileBuilderFactory.get_available_reinforcements()
        )
        _calculated_profiles = []
        for _reinforcement_type in _available_reinforcements:
            try:
                _builder = ReinforcementProfileBuilderFactory.get_builder(
                    _reinforcement_type
                )
                _builder.base_profile = self.base_profile
                _builder.scenario = self.scenario
                _calc_profile = _builder.build()
                _calculated_profiles.append(_calc_profile)
            except Exception as e_info:
                logging.error(
                    "Error calculating reinforcement: {}".format(_reinforcement_type())
                )
                logging.error(e_info)
                raise
        return _calculated_profiles

    def _get_multi_location_profile_cost_builder(
        self,
    ) -> MultiLocationProfileCostReportBuilder:
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.surroundings = self.surroundings
        return _builder

    def build(self) -> KoswatSummary:
        _summary = KoswatSummary()
        _mlpc_builder = self._get_multi_location_profile_cost_builder()
        for _calc_profile in self._get_calculated_profile_list():
            _mlpc_builder.reinforced_profile = _calc_profile
            _summary.locations_profile_report_list.append(_mlpc_builder.build())
        return _summary
