from typing import Iterator

from koswat.strategies.order_strategy.order_strategy_reinforcement_filter_criteria import (
    OrderStrategyReinforcementSkipCriteria,
)
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputBase,
)


class OrderStrategyReinforcementSortCriteria:
    """
    Orders a list of strategy reinforcements based on the criteria from
    `OrderStrategyReinforcementSkipCriteria`
    """

    def __init__(self, strategy_reinforcements: list[StrategyReinforcementInputBase]):
        self.strategy_reinforcements = strategy_reinforcements

    def sort(self) -> list[StrategyReinforcementInputBase]:
        _initial_sorting = self._initial_sort()
        return list(self._get_most_flexible_reinforcements(_initial_sorting))

    def _initial_sort(self) -> list[StrategyReinforcementInputBase]:
        return sorted(
            self.strategy_reinforcements,
            key=lambda x: (x.ground_level_surface, x.base_costs_with_surtax),
            reverse=True,
        )

    def _get_most_flexible_reinforcements(
        self,
        reinforcements: list[StrategyReinforcementInputBase],
    ) -> Iterator[StrategyReinforcementInputBase]:
        for _idx, _reinforcement in enumerate(reinforcements[:-1]):
            _skip_criteria = OrderStrategyReinforcementSkipCriteria(
                _reinforcement, reinforcements[_idx + 1 :]
            )
            if not _skip_criteria.skip_reinforcement():
                yield _reinforcement
        # Last reinforcement is always included,
        # as it is the least restrictive but most expensive
        yield reinforcements[-1]
