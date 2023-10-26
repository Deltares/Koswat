from koswat.cost_report.summary.koswat_summary import KoswatSummary


class TestKoswatSummary:
    def test_initialize(self):
        _summary = KoswatSummary()
        assert isinstance(_summary, KoswatSummary)
        assert not any(_summary.locations_profile_report_list)
        assert not any(_summary.reinforcement_per_locations)
