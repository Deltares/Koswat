import abc
from itertools import groupby
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class OrderStrategyBase(abc.ABC):
    reinforcement_order: list[ReinforcementProfileProtocol]

    def _get_reinforcement_groupings(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[int, StrategyLocationReinforcement]:
        return list(
            (self.reinforcement_order.index(k), list(g))
            for k, g in groupby(
                location_reinforcements,
                lambda x: x.selected_measure,
            )
        )

    @abc.abstractmethod
    def apply(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> None:
        pass
