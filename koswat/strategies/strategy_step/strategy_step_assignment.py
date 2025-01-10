from typing import TypedDict

from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


class StrategyStepAssignment(TypedDict):
    step_type: StrategyStepEnum
    step_value: type[ReinforcementProfileProtocol]
