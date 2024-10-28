from __future__ import annotations

from dataclasses import dataclass, field

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


@dataclass
class InfraCluster:
    reinforcement_type: type[ReinforcementProfileProtocol]
    cluster: list[StrategyLocationReinforcement] = field(default_factory=lambda: [])

    @property
    def current_cost(self) -> float:
        """
        Calculates the cost of applying the `reinforcement_type` to
        all locations present in the `cluster`.

        Returns:
            float: The total (current) cost of this cluster.
        """
        return sum(_c.current_cost for _c in self.cluster)

    def set_cheapest_common_available_measure(
        self,
        measure_costs: dict[type[ReinforcementProfileProtocol]],
    ) -> None:
        """
        Updates all the location reinforcements with the cheapest reinforcement type
        from the `measure_costs`.

        Args:
            measure_costs (dict[type[ReinforcementProfileProtocol]]):
                dictionary with the total costs per reinforcement type.
        """
        _selection = min(
            measure_costs,
            key=measure_costs.get,
        )

        if _selection != self.reinforcement_type:
            self.reinforcement_type = _selection
            for _cd in self.cluster:
                _cd.selected_measure = _selection
