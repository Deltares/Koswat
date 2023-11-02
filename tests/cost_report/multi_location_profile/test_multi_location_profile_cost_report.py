import math

from koswat.cost_report.multi_location_profile.multi_location_profile_cost_report import (
    MultiLocationProfileCostReport,
)


class TestMultipleLocationProfileCostReport:
    def test_initialize(self):
        _report = MultiLocationProfileCostReport()
        assert isinstance(_report, MultiLocationProfileCostReport)
        assert not any(_report.locations)
        assert not _report.profile_cost_report
        assert not _report.profile_type_name
        assert math.isnan(_report.total_cost)
        assert math.isnan(_report.total_quantity)
        assert math.isnan(_report.cost_per_km)
