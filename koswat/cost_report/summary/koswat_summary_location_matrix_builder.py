import logging
from collections import defaultdict
from dataclasses import dataclass, field

from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.strategies.strategy_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_input import StrategyReinforcementInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
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
    ) -> dict[PointSurroundings, StrategyReinforcementTypeCosts]:
        _infra_costs = locations_profile.get_infra_costs_per_location()

        def create_strategy_location_reinforcement_costs():
            return StrategyReinforcementTypeCosts(
                reinforcement_type=type(
                    locations_profile.profile_cost_report.reinforced_profile
                ),
                base_costs_with_surtax=locations_profile.profile_cost_report.total_cost_with_surtax,
            )

        _dict_matrix = defaultdict(create_strategy_location_reinforcement_costs)
        for _location in locations_profile.report_locations:
            (
                _dict_matrix[_location].infrastructure_costs,
                _dict_matrix[_location].infrastructure_costs_with_surtax,
            ) = _infra_costs.get(_location, (0.0, 0.0))
        return dict(_dict_matrix)

    def _get_list_summary_matrix_for_locations_with_reinforcements(
        self,
    ) -> list[dict[PointSurroundings, StrategyReinforcementTypeCosts]]:
        return list(
            map(
                self._get_multi_location_profile_to_dict_matrix,
                self.locations_profile_report_list,
            )
        )

    def _get_reinforcements_input_list(
        self,
        locations_per_reinforcement: list[
            dict[PointSurroundings, StrategyReinforcementTypeCosts]
        ],
    ) -> list[StrategyReinforcementInput]:
        def get_reinforcement(
            reinforcement_cost: StrategyReinforcementTypeCosts,
        ) -> StrategyReinforcementInput:
            _reinforcement = next(
                (
                    _pcr.profile_cost_report.reinforced_profile
                    for _pcr in self.locations_profile_report_list
                    if type(_pcr.profile_cost_report.reinforced_profile)
                    == reinforcement_cost.reinforcement_type
                ),
                None,
            )
            if not _reinforcement:
                raise ValueError(
                    f"Reinforcement type {reinforcement_cost.reinforcement_type} not found in profile reports."
                )
            return StrategyReinforcementInput(
                reinforcement_type=reinforcement_cost.reinforcement_type,
                base_costs_with_surtax=reinforcement_cost.base_costs_with_surtax,
                ground_level_surface=_reinforcement.new_ground_level_surface,
            )

        # Get the reinforcement cost of the first location for each reinforcement (if present).
        _reinforcement_costs = []
        for _ref_loc_dict in locations_per_reinforcement:
            _locs = list(_ref_loc_dict.values())
            if not _locs:
                continue
            _reinforcement_costs.append(_locs[0])

        return list(map(get_reinforcement, _reinforcement_costs))

    def build(
        self,
    ) -> tuple[list[StrategyLocationInput], list[StrategyReinforcementInput]]:
        """
        Build the locations-reinforcements matrix.

        Returns:
            tuple[list[StrategyLocationInput], list[StrategyReinforcementInput]]:
                Tuple containing:
                - list[StrategyLocationInput]: The locations-reinforcements matrix.
                - list[StrategyReinforcementInput]: The list of applied reinforcements.
        """
        # 1. First we get all the possible reinforcements per point.
        logging.info("Initalizing locations-reinforcements matrix.")
        _reinforce_matrix_dict_list = (
            self._get_list_summary_matrix_for_locations_with_reinforcements()
        )

        # 2. Then we initialize the matrix with all available locations,
        # but no reinforcements.
        _strategy_locations_dict = dict((_ps, []) for _ps in self.available_locations)

        # 3. Last, we merge the reinforcements dictionary into the matrix.
        for _loc_key, _strat_locs in _strategy_locations_dict.items():
            for _reinforce_matrix_dict in _reinforce_matrix_dict_list:
                # Add the reinforcement to the matrix if location exists.
                if _loc_key in _reinforce_matrix_dict.keys():
                    _strat_locs.append(_reinforce_matrix_dict[_loc_key])

        # 4. Sort matrix by traject order for normalized usage in Koswat.
        def to_strategy_location(
            matrix_tuple: tuple[PointSurroundings, list[StrategyReinforcementTypeCosts]]
        ) -> StrategyLocationInput:
            return StrategyLocationInput(
                point_surrounding=matrix_tuple[0],
                strategy_reinforcement_type_costs=matrix_tuple[1],
            )

        _strategy_locations = list(
            map(
                to_strategy_location,
                dict(
                    sorted(
                        _strategy_locations_dict.items(),
                        key=lambda x: x[0].traject_order,
                    )
                ).items(),
            )
        )

        logging.info("Finalized locations-reinforcements matrix.")

        # 5. Collect the reinforcements used in the strategy.
        _strategy_reinforcements_list = self._get_reinforcements_input_list(
            _reinforce_matrix_dict_list
        )

        return _strategy_locations, _strategy_reinforcements_list
