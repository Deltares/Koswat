from __future__ import annotations

from typing import List

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)


class KoswatSummary:
    locations_profile_report_list: List[MultiLocationProfileCostReport]

    def __init__(self) -> None:
        self.locations_profile_report_list = []
