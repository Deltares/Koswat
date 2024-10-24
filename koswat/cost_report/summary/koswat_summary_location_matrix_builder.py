import logging
from collections import defaultdict
from dataclasses import dataclass, field

from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.strategies.strategy_input import (
    StrategyLocation,
    StrategyLocationReinforcementCosts,
)


@dataclass
class KoswatSummaryLocationMatrixBuilder(BuilderProtocol):
    """
    NOTE: Although this 'problem' could be easily solved with `pandas`
    or `numpy`, I prefer not to include external (heavy) dependencies unless
    strictly necessary.
    If / when performance would become a problem, then this builder could (perhaps)
    benefit from using the aforementioned libraries.
    """

    locations_profile_report_list: list[MultiLocationProfileCostReport] = field(
        default_factory=lambda: []
    )
    available_locations: list[PointSurroundings] = field(default_factory=lambda: [])

    def _get_multi_location_profile_to_dict_matrix(
        self, locations_profile: MultiLocationProfileCostReport
    ) -> dict[PointSurroundings, StrategyLocationReinforcementCosts]:
        _infra_costs = locations_profile.get_infra_costs_per_location()

        def create_strategy_location_reinforcement_costs():
            return StrategyLocationReinforcementCosts(
                reinforcement_type=type(
                    locations_profile.profile_cost_report.reinforced_profile
                ),
                base_costs=locations_profile.profile_cost_report.total_cost,
            )

        _dict_matrix = defaultdict(create_strategy_location_reinforcement_costs)
        for _location in locations_profile.report_locations:
            _dict_matrix[_location].infastructure_costs = _infra_costs.get(
                _location, 0.0
            )
        return dict(_dict_matrix)

    def _get_list_summary_matrix_for_locations_with_reinforcements(
        self,
    ) -> list[dict[PointSurroundings, StrategyLocationReinforcementCosts]]:
        return list(
            map(
                self._get_multi_location_profile_to_dict_matrix,
                self.locations_profile_report_list,
            )
        )

    def build(
        self,
    ) -> list[StrategyLocation]:
        # dict[PointSurroundings, list[Type[ReinforcementProfileProtocol]]]:
        # 1. First we get all the possible reinforcements per point.

        logging.info("Initalizing locations-reinforcements matrix.")
        _reinforce_matrix_dict_list = (
            self._get_list_summary_matrix_for_locations_with_reinforcements()
        )

        # 2. Then we initialize the matrix with all available locations,
        # but no reinforcements.

        _strategy_locations = dict((_ps, []) for _ps in self.available_locations)

        # 3. Last, we merge the reinforcements dictionary into the matrix.
        for _location in _strategy_locations.keys():
            for _reinforce_matrix_dict in _reinforce_matrix_dict_list:
                if _location in _reinforce_matrix_dict:
                    _strategy_locations[_location].append(
                        _reinforce_matrix_dict[_location]
                    )

        # 4. Sort matrix by traject order for normalized usage in Koswat.
        def to_strategy_location(
            matrix_tuple: tuple[
                PointSurroundings, list[StrategyLocationReinforcementCosts]
            ]
        ) -> StrategyLocation:
            return StrategyLocation(
                point_surrounding=matrix_tuple[0],
                available_reinforcements=matrix_tuple[1],
            )

        _strategy_locations = list(
            map(
                to_strategy_location,
                dict(
                    sorted(
                        _strategy_locations.items(), key=lambda x: x[0].traject_order
                    )
                ).items(),
            )
        )

        logging.info("Finalized locations-reinforcements matrix.")

        return _strategy_locations
