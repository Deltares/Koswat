from koswat.cost_report.koswat_report import MultiLocationMultiProfileCostSummary


class TestKoswatSummary:
    def test_initialize(self):
        _summary = MultiLocationMultiProfileCostSummary()
        assert isinstance(_summary, MultiLocationMultiProfileCostSummary)
        assert not any(_summary.locations_profile_report_list)
