from __future__ import annotations

import math
from typing import List

from shapely.geometry.polygon import Polygon

from koswat.profiles.koswat_layers import KoswatLayer
from koswat.profiles.koswat_profile import KoswatProfile


class LayerCostReport:
    layer: KoswatLayer = None
    total_volume: float = math.nan

    @property
    def total_cost(self) -> float:
        return self.total_volume * self.layer.material.cost


class ProfileCostReport:
    layer_reports: List[LayerCostReport] = []

    @property
    def total_cost(self) -> float:
        if not self.layer_reports:
            return math.nan
        return sum(lr.total_cost for lr in self.layer_reports)

    @property
    def total_volume(self) -> float:
        if not self.layer_reports:
            return math.nan
        return sum(lr.toal_volume for lr in self.layer_reports)


class CostReportBuilder:
    @staticmethod
    def get_layer_cost_report(
        old_layer: KoswatLayer, new_layer: KoswatLayer
    ) -> LayerCostReport:
        if old_layer.material != new_layer.material:
            raise ValueError("Material differs between layers. Cannot compute costs.")
        _layer_report = LayerCostReport()
        _diff_geometry = old_layer.geometry - new_layer.geometry
        _layer_report.total_volume = _diff_geometry.area
        return _layer_report

    @staticmethod
    def get_profile_cost_report(
        old_profile: KoswatProfile, new_profile: KoswatProfile
    ) -> ProfileCostReport:
        _report = ProfileCostReport()
        if old_profile.layers != new_profile.layers:
            raise ValueError(
                "Layers not matching between old and new profile. Calculation of costs cannot be computed."
            )
        _report.layer_reports = [
            CostReportBuilder.get_layer_cost_report(old_l, new_profile.layers[idx_l])
            for idx_l, old_l in enumerate(old_profile.layers)
        ]
        return _report
