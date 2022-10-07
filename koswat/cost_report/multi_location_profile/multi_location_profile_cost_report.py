import math
from typing import List

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.surroundings.buildings_polderside.koswat_buildings_polderside import (
    PointSurroundings,
)


class MultiLocationProfileCostReport(CostReportProtocol):
    locations: List[PointSurroundings]
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
    def total_cost(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost * len(self.locations)

    @property
    def total_volume(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_volume * len(self.locations)

    @property
    def profile_type(self) -> str:
        if not self.profile_cost_report or not self.profile_cost_report.new_profile:
            return ""
        return str(self.profile_cost_report.new_profile)

    def as_dict(self) -> float:
        return dict(
            total_cost=self.total_cost,
            total_volume=self.total_volume,
            profile_type=self.profile_type,
            locations=[_loc.location for _loc in self.locations],
        )
