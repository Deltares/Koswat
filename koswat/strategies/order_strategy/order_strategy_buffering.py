from dataclasses import dataclass

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.order_strategy.order_strategy_base import OrderStrategyBase
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


@dataclass
class OrderStrategyBuffering(OrderStrategyBase):
    """
    Applies buffering, through masks, to each location pre-assigned reinforcement.
    The result of the `apply` method will be the locations with the best
    reinforcement fit (lowest index from `reinforcement_order`) that fulfills the
    `reinforcement_min_buffer` requirement.
    """

    reinforcement_order: list[type[ReinforcementProfileProtocol]]
    reinforcement_min_buffer: float

    def _get_buffer_mask(
        self, location_reinforcements: list[StrategyLocationReinforcement]
    ) -> list[int]:
        _grouped_location_reinforcements = self._get_reinforcement_groupings(
            location_reinforcements
        )
        _len_location_reinforcements = len(location_reinforcements)
        _candidates_masks = dict(
            (_r_idx, [-1] * _len_location_reinforcements)
            for _r_idx in range(0, len(self.reinforcement_order))
        )
        _visited = 0
        for _reinforcement_idx, _sub_group in _grouped_location_reinforcements:
            # Define indices.
            _lower_limit = int(max(0, _visited - self.reinforcement_min_buffer))
            _new_visited = _visited + len(_sub_group)
            _upper_limit = int(
                min(
                    _new_visited + self.reinforcement_min_buffer,
                    _len_location_reinforcements,
                )
            )

            # Update masks
            _candidates_masks[_reinforcement_idx][_lower_limit:_new_visited] = [
                _reinforcement_idx
            ] * (_new_visited - _lower_limit)

            _candidates_masks[_reinforcement_idx][_visited:_upper_limit] = [
                _reinforcement_idx
            ] * (_upper_limit - _visited)

            # Update visited
            _visited = _new_visited

        # Combine dicts and get max value as "higher values" cannot use
        # a "lower value" buffer.
        return list(map(max, zip(*_candidates_masks.values())))

    def apply(
        self,
        location_reinforcements: list[StrategyLocationReinforcement],
    ) -> None:
        _result_mask = self._get_buffer_mask(location_reinforcements)

        # Apply buffer values.
        for _idx, _location in enumerate(location_reinforcements):
            _location.set_selected_measure(
                self.reinforcement_order[_result_mask[_idx]], StrategyStepEnum.ORDERED
            )
