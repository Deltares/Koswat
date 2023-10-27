import logging
import math

from koswat.configuration.settings.koswat_run_scenario_settings import (
    KoswatRunScenarioSettings,
)
from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.multi_location_profile import (
    MultiLocationProfileCostReportBuilder,
)
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.cost_report.summary.koswat_summary_location_matrix_builder import (
    KoswatSummaryLocationMatrixBuilder,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements import ReinforcementProfileBuilderFactory
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile import (
    ReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput


class KoswatSummaryBuilder(BuilderProtocol):
    run_scenario_settings: KoswatRunScenarioSettings

    def __init__(self) -> None:
        self.run_scenario_settings = None

    @staticmethod
    def _get_corrected_koswat_scenario(
        orignial_scenario: KoswatScenario, input_profile_base: KoswatInputProfileBase
    ) -> KoswatScenario:
        """
        Get a koswat scenario (`KoswatScenario`) whose values are not `math.nan`.
        In practice this means that when a `KoswatScenario` value has not been set
        the corresponding one from `KoswatProfileBase` will be used instead.

        By having this code here we *guarantee* that a summary can be built with only
        the mandatory values of a `KoswatScenario`.

        Returns:
            KoswatScenario: Valid scenario to be used in reinforcements.
        """
        _new_koswat_scenario = KoswatScenario(**orignial_scenario.__dict__)
        if math.isnan(_new_koswat_scenario.kruin_breedte):
            _new_koswat_scenario.kruin_breedte = input_profile_base.kruin_breedte
        if math.isnan(_new_koswat_scenario.buiten_talud):
            _new_koswat_scenario.buiten_talud = input_profile_base.buiten_talud

        return _new_koswat_scenario

    def _get_calculated_profile_list(self) -> list[ReinforcementProfileProtocol]:
        _calculated_profiles = []
        _factory_builder = ReinforcementProfileBuilderFactory(
            base_profile=self.run_scenario_settings.input_profile_case,
            scenario=self._get_corrected_koswat_scenario(
                self.run_scenario_settings.scenario,
                self.run_scenario_settings.input_profile_case.input_data,
            ),
        )
        for (
            _reinforcement_profile_type
        ) in ReinforcementProfileBuilderFactory.get_available_reinforcements():
            try:
                _calc_profile = _factory_builder.build(_reinforcement_profile_type)
                _calculated_profiles.append(_calc_profile)
            except Exception as e_info:
                logging.error(
                    "Error calculating reinforcement: {}. Detailed error: {}".format(
                        _reinforcement_profile_type(), e_info
                    )
                )

        return _calculated_profiles

    def _get_multi_location_profile_cost_builder(
        self,
    ) -> MultiLocationProfileCostReportBuilder:
        _builder = MultiLocationProfileCostReportBuilder()
        _builder.surroundings = self.run_scenario_settings.surroundings
        _builder.koswat_costs = self.run_scenario_settings.costs
        return _builder

    def _get_final_reinforcement_per_location(
        self,
        locations_profile_report_list: list[MultiLocationProfileCostReport],
        available_locations: list[PointSurroundings],
    ) -> dict[PointSurroundings, ReinforcementProfile]:
        _matrix_builder = KoswatSummaryLocationMatrixBuilder()
        _matrix_builder.available_locations = available_locations
        _matrix_builder.locations_profile_report_list = locations_profile_report_list
        _matrix = _matrix_builder.build()

        _strategy_input = StrategyInput(
            locations_matrix=_matrix,
            structure_min_buffer=self.run_scenario_settings.surroundings.reinforcement_min_buffer,
            structure_min_length=self.run_scenario_settings.surroundings.reinforcement_min_separation,
        )

        # In theory this will become a factory (somewhere) where
        # the adequate strategy will be chosen.
        return OrderStrategy().apply_strategy(_strategy_input)

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

        _summary.reinforcement_per_locations = (
            self._get_final_reinforcement_per_location(
                _summary.locations_profile_report_list,
                self.run_scenario_settings.surroundings.locations,
            )
        )
        return _summary
