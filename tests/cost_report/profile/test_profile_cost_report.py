import math

from koswat.cost_report.profile.profile_cost_report import ProfileCostReport


class TestProfileCostReport:
    def test_initialize(self):
        _report = ProfileCostReport()
        assert isinstance(_report, ProfileCostReport)
        assert not _report.reinforced_profile
        assert not _report.volume_calculation_parameters
        assert not any(_report.layer_cost_reports)
        assert math.isnan(_report.total_cost)
        assert math.isnan(_report.total_volume)
