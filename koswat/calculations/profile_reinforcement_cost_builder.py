from koswat.koswat_report import LayerCostReport, ProfileCostReport
from koswat.profiles.koswat_layers import KoswatLayer
from koswat.profiles.koswat_profile import KoswatProfile


class ProfileReinforcementCostBuilder:
    """
    TODO: This class (like many others) is still a work in progress.
    Not entirely sure yet which structure will be applied once we start using layers.
    """

    def get_layer_cost_report(
        old_layer: KoswatLayer, new_layer: KoswatLayer
    ) -> LayerCostReport:
        if old_layer.material != new_layer.material:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        _layer_report = LayerCostReport()
        _diff_geometry = old_layer.geometry - new_layer.geometry
        _layer_report.total_volume = _diff_geometry.area
        _layer_report.layer = new_layer
        return _layer_report

    def get_profile_cost_report(
        self, old_profile: KoswatProfile, new_profile: KoswatProfile
    ) -> ProfileCostReport:
        _report = ProfileCostReport()
        if old_profile.layers != new_profile.layers:
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )
        _report.layer_cost_reports = [
            self.get_layer_cost_report(old_l, new_profile.layers[idx_l])
            for idx_l, old_l in enumerate(old_profile.layers)
        ]
        return _report
