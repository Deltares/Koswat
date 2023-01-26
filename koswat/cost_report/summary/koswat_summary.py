from __future__ import annotations

from typing import List

from koswat.cost_report.multi_location_profile import MultiLocationProfileCostReport
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings


class KoswatSummary:
    locations_profile_report_list: List[MultiLocationProfileCostReport]
    available_locations: List[PointSurroundings]

    def __init__(self) -> None:
        self.locations_profile_report_list = []
        self.available_locations = []
