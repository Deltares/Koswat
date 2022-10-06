import math

from koswat.cost_report.reports.profile_cost_report import ProfileCostReport


class TestProfileCostReport:
    def test_initialize(self):
        _report = ProfileCostReport()
        assert isinstance(_report, ProfileCostReport)
        assert not _report.new_profile
        assert not _report.old_profile
        assert not any(_report.layer_cost_reports)
        assert math.isnan(_report.total_cost)
        assert math.isnan(_report.total_volume)
