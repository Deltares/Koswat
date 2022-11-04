from koswat.calculations import ReinforcementProfileProtocol
from koswat.cost_report.layer.base_layer_cost_report_builder import (
    BaseLayerCostReportBuilder,
)
from koswat.cost_report.layer.layer_cost_report_protocol import LayerCostReportProtocol
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.cost_report.layer.standard_layer_cost_report_builder import (
    StandardLayerCostReportBuilder,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


class StandardProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_layer_cost_report(
        self,
        old_layer: KoswatLayerProtocol,
        new_layer: KoswatLayerProtocol,
        latest_report: LayerCostReportProtocol,
    ) -> LayerCostReportProtocol:
        _layer_report_builder = StandardLayerCostReportBuilder()
        _layer_report_builder.base_layer = old_layer
        _layer_report_builder.calc_layer = new_layer
        _layer_report_builder.base_core_geometry = latest_report.old_layer.geometry
        _layer_report_builder.calc_core_geometry = latest_report.new_layer.geometry
        return _layer_report_builder.build()

    def build(self) -> ProfileCostReport:
        _report = ProfileCostReport()
        _report.new_profile = self.calculated_profile
        _report.old_profile = self.base_profile
        if len(self.base_profile.layers_wrapper.layers) != len(
            self.calculated_profile.layers_wrapper.layers
        ):
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )

        _core_report_builder = BaseLayerCostReportBuilder()
        _core_report_builder.base_layer = self.base_profile.layers_wrapper.base_layer
        _core_report_builder.calc_layer = (
            self.calculated_profile.layers_wrapper.base_layer
        )
        _report.layer_cost_reports.append(_core_report_builder.build())
        # Get x_layer_removal and x_layer_added
        for idx_l, _old_coating_layer in reversed(
            list(enumerate(self.base_profile.layers_wrapper.coating_layers))
        ):
            _layer_cost_report = self._get_layer_cost_report(
                _old_coating_layer,
                self.calculated_profile.layers_wrapper.coating_layers[idx_l],
                _report.layer_cost_reports[-1],
            )

            # Add it to collection
            _report.layer_cost_reports.append(_layer_cost_report)

        return _report
