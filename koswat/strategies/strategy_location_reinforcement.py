from dataclasses import dataclass, field

from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.strategies.strategy_input import StrategyLocationInput
from koswat.strategies.strategy_reinforcement_type_costs import (
    StrategyReinforcementTypeCosts,
)
from koswat.strategies.strategy_step.strategy_step_assignment import (
    StrategyStepAssignment,
)
from koswat.strategies.strategy_step.strategy_step_enum import StrategyStepEnum


@dataclass
class StrategyLocationReinforcement:
    """
    Represents a location and the different reinforcements that can be applied to it
    as well their costs.
    This class is used to show the final chosen state for a location.
    """

    location: PointSurroundings
    # PHASED-OUT, this property should be removed once we confirm available measures
    # are filtered by the order strategy (cost-space evaluation)
    # use `filtered_measures` instead!
    available_measures: list[type[ReinforcementProfileProtocol]] = field(
        default_factory=lambda: []
    )
    filtered_measures: list[type[ReinforcementProfileProtocol]] = field(
        default_factory=lambda: []
    )
    strategy_location_input: StrategyLocationInput = None

    _selected_measure_steps: list[StrategyStepAssignment] = field(
        init=False, default_factory=lambda: []
    )

    def __post_init__(self):
        if any(self.filtered_measures):
            # Set the inital selection to the first available measure.
            self.set_selected_measure(
                self.filtered_measures[0], StrategyStepEnum.INITIAL
            )

    @property
    def current_selected_measure(self) -> type[ReinforcementProfileProtocol]:
        """
        Exposes the current selected measure for this object.
        """
        if not any(self._selected_measure_steps):
            return None
        return self._selected_measure_steps[-1]["step_value"]

    @property
    def current_cost(self) -> float:
        """
        Estimates the costs with surtax at this location for the given `current_selected_measure`.
        """
        if not self.current_selected_measure or not self.strategy_location_input:
            return 0.0
        for _srtc in self.strategy_location_input.strategy_reinforcement_type_costs:
            if _srtc.reinforcement_type == self.current_selected_measure:
                return _srtc.total_costs_with_surtax
        return 0.0

    @property
    def cheapest_reinforcement(self) -> StrategyReinforcementTypeCosts:
        if not self.strategy_location_input:
            return None
        return self.strategy_location_input.cheapest_reinforcement

    def set_selected_measure(
        self,
        reinforcement_type: type[ReinforcementProfileProtocol],
        step: StrategyStepEnum,
    ):
        """
        Changes the value reprsented in `current_selected_measure` and updates the
        dictionary of selections (history).

        Args:
            reinforcement_type (type[ReinforcementProfileProtocol]): Reinforcement type
            step (StrategyStepsEnum): Step whose
        """
        # Update the assigned value for this step.
        # TODO: Eventually we want to remove from `filtered_measures` all measures with
        # a lower index, something like:
        # _from_idx = self._filtered_measures.index(reinforcement_type)
        # self._filtered_measures = self._filtered_measures[_from_idx:]
        self._selected_measure_steps.append(
            StrategyStepAssignment(
                step_type=step,
                step_value=reinforcement_type,
            )
        )

    def get_selected_measure_steps(
        self,
    ) -> tuple[
        type[ReinforcementProfileProtocol],
        type[ReinforcementProfileProtocol],
        type[ReinforcementProfileProtocol],
    ]:
        """
        Outputs the selected measure following the domain (expected) steps:
            - Initial step,
            - Order step,
            - Infrastructure step

        Returns:
            tuple[
                type[ReinforcementProfileProtocol],
                type[ReinforcementProfileProtocol],
                type[ReinforcementProfileProtocol]]: Resulting tuple.
        """

        def filter_ordered_step(assignment_step: StrategyStepAssignment) -> bool:
            return assignment_step["step_type"] == StrategyStepEnum.ORDERED

        _initial_step = self._selected_measure_steps[0]
        _ordered_step = next(
            filter(filter_ordered_step, self._selected_measure_steps[-1::-1]),
            _initial_step,
        )
        return (
            _initial_step["step_value"],
            _ordered_step["step_value"],
            self.current_selected_measure,
        )

    def get_reinforcement_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> float:
        if reinforcement_type not in self.available_measures:
            raise ValueError(
                f"Reinforcement {reinforcement_type.output_name} not available, costs cannot be computed.",
            )
        return self.strategy_location_input.get_reinforcement_costs(reinforcement_type)

    def get_infrastructure_costs(
        self, reinforcement_type: type[ReinforcementProfileProtocol]
    ) -> tuple[float, float]:
        """
        Returns the infrastructure costs for the given reinforcement type (without and with surtax).

        Args:
            reinforcement_type (type[ReinforcementProfileProtocol]): Reinforcement type.

        Returns:
            tuple[float, float]: Tuple containing the infrastructure costs without and with surtax.
        """
        if (
            self.strategy_location_input
            and reinforcement_type in self.available_measures
        ):
            return self.strategy_location_input.get_infrastructure_costs(
                reinforcement_type
            )
        return (0.0, 0.0)
