from __future__ import annotations

from dataclasses import dataclass, field

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
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_type import StrategyReinforcementType
from koswat.strategies.strategy_reinforcements_protocol import (
    StrategyReinforcementsProtocol,
)


@dataclass
class OrderStrategyReinforcements(StrategyReinforcementsProtocol):
    """
    Provide the reinforcements for the order strategy.
    """

    reinforcements: list[StrategyReinforcementType] = field(default_factory=list)

    @classmethod
    def from_strategy_input(
        cls, strategy_input: StrategyInput
    ) -> OrderStrategyReinforcements:
        _reinforcements = {
            StrategyReinforcementType(
                reinforcement_type=x.reinforcement_type,
                base_costs=x.base_costs,
                ground_level_surface=x.ground_level_surface,
            )
            for x in strategy_input.reinforcements
        }
        return cls(reinforcements=list(_reinforcements))

    @property
    def strategy_reinforcements(self) -> list[type[ReinforcementProfileProtocol]]:
        # TODO Implement this method.
        return self.get_default_order()

    @staticmethod
    def get_default_order() -> list[type[ReinforcementProfileProtocol]]:
        return [
            SoilReinforcementProfile,
            VPSReinforcementProfile,
            PipingWallReinforcementProfile,
            StabilityWallReinforcementProfile,
            CofferdamReinforcementProfile,
        ]
