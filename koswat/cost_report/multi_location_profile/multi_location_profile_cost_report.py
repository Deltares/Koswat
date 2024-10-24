import math
from dataclasses import dataclass, field

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


@dataclass
class MultiLocationProfileCostReport(CostReportProtocol):
    report_locations: list[PointSurroundings] = field(default_factory=lambda: [])
    infra_multilocation_profile_cost_report: list[
        InfrastructureLocationProfileCostReport
    ] = field(default_factory=lambda: [])
    profile_cost_report: ProfileCostReport = None

    def get_infra_costs_per_location(self) -> dict[PointSurroundings, float]:
        """
        Gets the total costs related to infrastructures at each of the points for
        the profile type in `profile_cost_report`

        Returns:
            dict[PointSurroundings, float]: Total cost per location.
        """
        return {
            _infra_cost_report.location: _infra_cost_report.total_cost
            for _infra_cost_report in self.infra_multilocation_profile_cost_report
        }

    @property
    def cost_per_km(self) -> float:
        if not self.profile_cost_report:
            return math.nan
        return self.profile_cost_report.total_cost * 1000

    @property
    def cost_per_km_with_surtax(self) -> float:
        if not self.profile_cost_report:
            return math.nan
        return self.profile_cost_report.total_cost_with_surtax * 1000

    @property
    def total_cost(self) -> float:
        """
        Calculates the cost of the measure for all possible locations,
        regardless whether that measure is chosen by the order strategy or not.
        """
        if not self.profile_cost_report or not self.report_locations:
            return math.nan
        return self.profile_cost_report.total_cost * len(self.report_locations)

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.profile_cost_report or not self.report_locations:
            return math.nan
        return self.profile_cost_report.total_cost_with_surtax * len(
            self.report_locations
        )

    @property
    def profile_type_name(self) -> str:
        if (
            not self.profile_cost_report
            or not self.profile_cost_report.reinforced_profile
        ):
            return ""
        return self.profile_cost_report.reinforced_profile.output_name
