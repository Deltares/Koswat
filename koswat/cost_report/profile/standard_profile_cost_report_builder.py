
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class StandardProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None

    def build(self) -> ProfileCostReport:
        if self.base_layer.material.name != self.calc_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        raise NotImplementedError()
