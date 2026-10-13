from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.strategies.strategy_reinforcement_filter_criteria_protocol import (
    StrategyReinforcementFilterCriteriaProtocol,
)
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_reinforcement_input import (
    StrategyReinforcementInputProtocol,
)


class StrategyReinforcementActiveFilterCriteria(
    StrategyReinforcementFilterCriteriaProtocol
):
    """
    This class is used to filter reinforcement profiles based on the active criteria.
    """

    def criteria_met_by(
        self, strategy_reinforcement: StrategyReinforcementInputProtocol
    ) -> bool:
        return (
            strategy_reinforcement.active
            or strategy_reinforcement.reinforcement_type
            == CofferdamReinforcementProfile
        )
