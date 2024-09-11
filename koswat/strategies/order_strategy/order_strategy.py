from __future__ import annotations

from typing import Type

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.vps_reinforcement_profile import (
    VPSReinforcementProfile,
)
from koswat.strategies.order_strategy.order_cluster import OrderCluster
from koswat.strategies.order_strategy.order_strategy_buffering import (
    OrderStrategyBuffering,
)
from koswat.strategies.order_strategy.order_strategy_clustering import (
    OrderStrategyClustering,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)
from koswat.strategies.strategy_protocol import StrategyProtocol


class OrderStrategy(StrategyProtocol):
    @staticmethod
    def get_default_order_for_reinforcements() -> list[
        Type[ReinforcementProfileProtocol]
    ]:
        return [
            SoilReinforcementProfile,
            VPSReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]

    @staticmethod
    def get_strategy_reinforcements(
        location_matrix: dict[
            PointSurroundings, list[Type[ReinforcementProfileProtocol]]
        ],
        selection_order: list[Type[ReinforcementProfileProtocol]],
    ) -> list[StrategyLocationReinforcement]:
        _strategy_reinforcements = []
        for (
            _location,
            _reinforcements,
        ) in location_matrix.items():
            _selected_reinforcement = next(
                (_or for _or in selection_order if _or in _reinforcements),
                selection_order[-1],
            )
            _strategy_reinforcements.append(
                StrategyLocationReinforcement(
                    location=_location,
                    available_measures=_reinforcements,
                    selected_measure=_selected_reinforcement,
                )
            )
        return _strategy_reinforcements

    def apply_strategy(
        self, strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        _reinforcement_order = self.get_default_order_for_reinforcements()
        _strategy_reinforcements = self.get_strategy_reinforcements(
            strategy_input.locations_matrix, _reinforcement_order
        )
        OrderStrategyBuffering.with_strategy(
            _reinforcement_order, strategy_input.reinforcement_min_buffer
        ).apply(_strategy_reinforcements)
        OrderStrategyClustering.with_strategy(
            _reinforcement_order, strategy_input.reinforcement_min_length
        ).apply(_strategy_reinforcements)
        return _strategy_reinforcements
