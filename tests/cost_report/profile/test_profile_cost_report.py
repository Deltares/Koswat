import math

from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.quantity_cost_parameters import QuantityCostParameters


class TestProfileCostReport:
    def test_initialize(self):
        _report = ProfileCostReport()
        assert isinstance(_report, ProfileCostReport)
        assert not _report.reinforced_profile
        assert isinstance(_report.quantity_cost_parameters, QuantityCostParameters)
        assert not any(_report.layer_cost_reports)
        assert _report.total_cost == 0
        assert _report.total_quantity == 0
