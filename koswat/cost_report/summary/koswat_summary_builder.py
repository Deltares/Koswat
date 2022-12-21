import logging
from typing import List

from koswat.calculations import ReinforcementProfileBuilderFactory
from koswat.calculations.protocols import ReinforcementProfileProtocol
from koswat.configuration.settings.koswat_run_settings import KoswatRunScenarioSettings
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.multi_location_profile import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary


class KoswatSummaryBuilder(BuilderProtocol):
    run_scenario_settings: KoswatRunScenarioSettings

    def __init__(self) -> None:
        self.run_scenario_settings = None

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
                _builder.base_profile = self.run_scenario_settings.input_profile_case
                _builder.scenario = self.run_scenario_settings.scenario
                _calc_profile = _builder.build()
                _calculated_profiles.append(_calc_profile)
            except Exception as e_info:
                logging.error(
                    "Error calculating reinforcement: {}. Detailed error: {}".format(
                        _reinforcement_type(), e_info
                    )
                )

        return _calculated_profiles

    def _get_multi_location_profile_cost_builder(
        self,
    ) -> MultiLocationProfileCostReportBuilder:
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.surroundings = self.run_scenario_settings.surroundings
        return _builder

    def build(self) -> KoswatSummary:
        _summary = KoswatSummary()
        logging.info(
            "Creating analysis for {} - scenario {} - {}".format(
                self.run_scenario_settings.input_profile_case.input_data.dike_section,
                self.run_scenario_settings.scenario.scenario_section,
                self.run_scenario_settings.scenario.scenario_name,
            )
        )
        _mlpc_builder = self._get_multi_location_profile_cost_builder()
        for _calc_profile in self._get_calculated_profile_list():
            _mlpc_builder.reinforced_profile = _calc_profile
            _summary.locations_profile_report_list.append(_mlpc_builder.build())
        return _summary
