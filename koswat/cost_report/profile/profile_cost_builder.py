from koswat.builder_protocol import BuilderProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.cost_report.layer.layer_cost_report_builder import LayerCostReportBuilder
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.dike.layers.koswat_layers import KoswatLayerProtocol
from koswat.dike.profile.koswat_profile import KoswatProfileBase


class ProfileCostReportBuilder(BuilderProtocol):
    base_profile: KoswatProfileBase
    calculated_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_layer_cost_report(
        self, base_layer: KoswatLayerProtocol, calculated_layer: KoswatLayerProtocol
    ) -> LayerCostReport:
        _builder = LayerCostReportBuilder()
        _builder.base_layer = base_layer
        _builder.calc_layer = calculated_layer
        return _builder.build()

    def _get_profile_cost_report(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _report.new_profile = self.calculated_profile
        _report.old_profile = self.base_profile
        if len(self.base_profile.layers._layers) != len(
            self.calculated_profile.layers._layers
        ):
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )
        _report.layer_cost_reports = [
            self._get_layer_cost_report(
                old_l, self.calculated_profile.layers._layers[idx_l]
            )
            for idx_l, old_l in enumerate(self.base_profile.layers._layers)
        ]
        return _report

    def build(self) -> ProfileCostReport:
        return self._get_profile_cost_report()