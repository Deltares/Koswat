from koswat.builder_protocol import BuilderProtocol
from koswat.koswat_report import LayerCostReport, ProfileCostReport
from koswat.profiles.koswat_layers import KoswatLayerProtocol
from koswat.profiles.koswat_profile import KoswatProfileBase


class ProfileCostBuilder(BuilderProtocol):
    base_profile: KoswatProfileBase
    calculated_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.surroundings = None
        self.base_profile = None
        self.calc_profile = None

    def _get_layer_cost_report(
        self, base_layer: KoswatLayerProtocol, calculated_layer: KoswatLayerProtocol
    ) -> LayerCostReport:
        if base_layer.material.name != calculated_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        _layer_report = LayerCostReport()
        _diff_geometry = calculated_layer.geometry.difference(base_layer.geometry)
        _layer_report.total_volume = _diff_geometry.area
        _layer_report.new_layer = calculated_layer
        return _layer_report

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
