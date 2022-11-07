from shapely.geometry import Polygon

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.layer.base_layer_cost_report import BaseLayerCostReport
from koswat.cost_report.layer.outside_slope_weakening_layer_cost_report_builder import (
    OustideSlopeWeakeningLayerCostReportBuilder,
)
from koswat.cost_report.profile.profile_cost_report import ProfileCostReport
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class OutsideSlopeProfileCostReportBuilder(ProfileCostReportBuilderProtocol):
    base_profile: KoswatProfileProtocol
    calculated_profile: ReinforcementProfileProtocol

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calculated_profile = None

    def _get_layer_cost_report(
        self,
        base_layer: KoswatLayerProtocol,
        calc_layer: KoswatLayerProtocol,
        base_geom: Polygon,
        calc_geom: Polygon,
    ) -> BaseLayerCostReport:
        _builder = OustideSlopeWeakeningLayerCostReportBuilder()
        _builder.base_layer = base_layer
        _builder.calc_layer = calc_layer
        _builder.base_core_geometry = base_geom
        _builder.calc_core_geometry = calc_geom
        return _builder.build()

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

        _layers = list(
            zip(
                self.base_profile.layers_wrapper.layers,
                self.calculated_profile.layers_wrapper.layers,
            )
        )
        for idx, (_base_layer, _calc_layer) in enumerate(_layers):
            _core_idx = min(idx + 1, len(_layers) - 1)
            _base_core, _calc_core = _layers[_core_idx]
            _layer_report = self._get_layer_cost_report(
                _base_layer, _calc_layer, _base_core.geometry, _calc_core.geometry
            )
            _report.layer_cost_reports.append(_layer_report)
        return _report
