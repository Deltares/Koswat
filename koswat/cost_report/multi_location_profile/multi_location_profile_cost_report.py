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
    obstacle_locations: list[PointSurroundings] = field(default_factory=lambda: [])
    infra_multilocation_profile_cost_report: list[
        InfrastructureLocationProfileCostReport
    ] = field(default_factory=lambda: [])
    profile_cost_report: ProfileCostReport = None

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
        if not self.profile_cost_report or not self.obstacle_locations:
            return math.nan
        return self.profile_cost_report.total_cost * len(self.obstacle_locations)

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.profile_cost_report or not self.obstacle_locations:
            return math.nan
        return self.profile_cost_report.total_cost_with_surtax * len(
            self.obstacle_locations
        )

    @property
    def infrastructure_cost(self) -> float:
        if not self.infra_multilocation_profile_cost_report:
            return math.nan
        return sum(x.total_cost for x in self.infra_multilocation_profile_cost_report)

    @property
    def infrastructure_cost_with_surtax(self) -> float:
        if not self.infra_multilocation_profile_cost_report:
            return math.nan
        return sum(
            x.total_cost_with_surtax
            for x in self.infra_multilocation_profile_cost_report
        )

    @property
    def profile_type_name(self) -> str:
        if (
            not self.profile_cost_report
            or not self.profile_cost_report.reinforced_profile
        ):
            return ""
        return self.profile_cost_report.reinforced_profile.output_name
