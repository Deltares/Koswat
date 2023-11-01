import math

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.surroundings.surroundings_polderside.koswat_surroundings_polderside import (
    PointSurroundings,
)


class MultiLocationProfileCostReport(CostReportProtocol):
    locations: list[PointSurroundings]
    profile_cost_report: ProfileCostReport

    def __init__(self) -> None:
        self.locations = []
        self.profile_cost_report = None

    @property
    def cost_per_km(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost * 1000

    @property
    def cost_with_surtax_per_km(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost_with_surtax * 1000

    @property
    def total_cost(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost * len(self.locations)

    @property
    def total_cost_with_surtax(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost_with_surtax * len(self.locations)

    @property
    def total_volume(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_volume * len(self.locations)

    @property
    def profile_type_name(self) -> str:
        if (
            not self.profile_cost_report
            or not self.profile_cost_report.reinforced_profile
        ):
            return ""
        return str(self.profile_cost_report.reinforced_profile)
