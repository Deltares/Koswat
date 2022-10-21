from koswat.cost_report.layer.layer_cost_report_builder import (
    LayerCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol


class LayerCostReportBuilderFactory:
    @staticmethod
    def get_builder(
        koswat_profile: KoswatProfileProtocol,
    ) -> LayerCostReportBuilderProtocol:
        pass
