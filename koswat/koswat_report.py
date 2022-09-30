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

    def as_dict(self) -> dict:
        return dict(
            material=self.layer.material.name,
            total_volume=self.total_volume,
            total_cost=self.total_cost,
        )


class ProfileCostReport:
    layer_cost_reports: List[LayerCostReport] = []

    @property
    def total_cost(self) -> float:
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_cost for lr in self.layer_cost_reports)

    @property
    def total_volume(self) -> float:
        if not self.layer_cost_reports:
            return math.nan
        return sum(lr.total_volume for lr in self.layer_cost_reports)

    def as_dict(self) -> dict:
        return dict(
            total_cost=self.total_cost,
            total_volume=self.total_volume,
            per_layer=[lcr.as_dict() for lcr in self.layer_cost_reports],
        )
