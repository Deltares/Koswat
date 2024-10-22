from dataclasses import dataclass, field

from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)
from koswat.cost_report.infrastructure.infrastructure_profile_costs_calculator import (
    InfrastructureProfileCostsCalculator,
)
from koswat.cost_report.infrastructure.profile_zone_calculator import (
    ProfileZoneCalculator,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


@dataclass
class MultiInfrastructureProfileCostsCalculator:
    """
    Calculator that contains all possible "infrastructure" calculators
    (`InfrastructureProfileCostsCalculator`) one for each of the available
    infrastructures in the current `KoswatScenario`.
    Its `calculate` method only requires a reinforcement
    (`ReinforcementProfileProtocol`) to determine all infrastructures' costs.
    """

    infrastructure_calculators: list[InfrastructureProfileCostsCalculator] = field(
        default_factory=lambda: []
    )

    def calculate(
        self, reinforced_profile: ReinforcementProfileProtocol
    ) -> list[InfrastructureLocationProfileCostReport]:
        """
        Calculates the costs related to appyling the provided `reinforcement_profile`
        at all the locations where an infrastructure is present. It first determines
        zone `A` and `B` and then provides their widths to the inner
        infrastructure calculators (`InfrastructureProfileCostsCalculator`).

        Args:
            reinforced_profile (ReinforcementProfileProtocol): Reinforcement to be applied.

        Returns:
            list[InfrastructureLocationProfileCostReport]: Collection of reports summarizing the cost-impact of a `reinforced_profile`.
        """
        _width_zone_a, _width_zone_b = ProfileZoneCalculator(
            reinforced_profile=reinforced_profile
        ).calculate()

        _reports = []
        for _calculator in self.infrastructure_calculators:
            _subreports = _calculator.calculate(_width_zone_a, _width_zone_b)
            _reports.extend(
                [
                    InfrastructureLocationProfileCostReport(
                        reinforced_profile=reinforced_profile,
                        infrastructure=_calculator.infrastructure,
                        infrastructure_location_costs=_subreport,
                    )
                    for _subreport in _subreports
                ]
            )

        return _reports
