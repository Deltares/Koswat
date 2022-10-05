from __future__ import annotations

import math
from typing import List, Optional, Protocol

from koswat.profiles.koswat_layers import KoswatLayerProtocol
from koswat.profiles.koswat_profile import KoswatProfile


class ReportProtocol(Protocol):
    total_cost: float
    total_volume: float

    def as_dict(self) -> float:
        pass


class LayerCostReport(ReportProtocol):
    layer: KoswatLayerProtocol = None
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


class ProfileCostReport(ReportProtocol):
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


class MultipleProfileCostReport(ReportProtocol):
    profile_list_reports: List[ProfileCostReport] = []

    @property
    def total_cost(self) -> float:
        if not self.profile_list_reports:
            return math.nan
        return sum(plr.total_cost for plr in self.profile_list_reports)

    @property
    def total_volume(self) -> float:
        if not self.profile_list_reports:
            return math.nan
        return sum(plr.total_volume for plr in self.profile_list_reports)

    def as_dict(self) -> float:
        return dict(
            total_cost=self.total_cost,
            total_volume=self.total_volume,
            per_layer=[lcr.as_dict() for lcr in self.profile_list_reports],
        )
