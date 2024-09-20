from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.cost_report.infrastructure.infrastructure_location_profile_cost_report import (
    InfrastructureLocationProfileCostReport,
)


class TestInfrastructureLocationProfileCostReport:
    def test_initialize(self):
        # 1. Define test data.
        _report = InfrastructureLocationProfileCostReport(
            reinforced_profile=None,
            infrastructure=None,
            infrastructure_location_costs=None,
        )

        # 2. Verify expectations.
        assert isinstance(_report, InfrastructureLocationProfileCostReport)
        assert isinstance(_report, CostReportProtocol)

        # Verify fallback values.
        assert not _report.location
        assert _report.total_cost == 0
        assert _report.total_cost_with_surtax == 0
