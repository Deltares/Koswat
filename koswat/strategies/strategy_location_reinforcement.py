from dataclasses import dataclass

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)


@dataclass
class StrategyLocationReinforcement:
    location: PointSurroundings
    selected_measure: type[ReinforcementProfileProtocol]
    available_measures: list[type[ReinforcementProfileProtocol]]
    strategy_location_input: StrategyLocationInput = None

    @property
    def current_cost(self) -> float:
        if not self.selected_measure or not self.strategy_location_input:
            return 0.0
        for _srtc in self.strategy_location_input.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == self.selected_measure:
                return _srtc.total_costs
        raise ValueError("No current cost could be calculated")

    @property
    def cheapest_reinforcement(self) -> StrategyReinforcementTypeCosts:
        if not self.strategy_location_input:
            return None
        return self.strategy_location_input.cheapest_reinforcement

    def get_reinforcement_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> float:
        if reinforcement_type not in self.available_measures:
            raise ValueError(
                f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed.",
            )
        return self.strategy_location_input.get_reinforcement_costs(reinforcement_type)
