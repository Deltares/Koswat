from __future__ import annotations

import math
from typing import List, Protocol

from koswat.profiles.koswat_layers import KoswatLayerProtocol
from koswat.profiles.koswat_profile import KoswatProfileBase
from koswat.surroundings.koswat_buildings_polderside import PointSurroundings


class ReportProtocol(Protocol):
    total_cost: float
    total_volume: float

    def __init__(self) -> None:
        self.total_cost = math.nan
        self.total_volume = math.nan

    def as_dict(self) -> float:
        pass


class LayerCostReport(ReportProtocol):
    new_layer: KoswatLayerProtocol
    old_layer: KoswatLayerProtocol
    total_volume: float

    def __init__(self) -> None:
        self.new_layer = None
        self.old_layer = None
        self.total_volume = math.nan

    @property
    def total_cost(self) -> float:
        if not self.new_layer:
            return math.nan
        return self.total_volume * self.new_layer.material.cost

    def as_dict(self) -> dict:
        return dict(
            material=self.new_layer.material.name,
            total_volume=self.total_volume,
            total_cost=self.total_cost,
        )


class ProfileCostReport(ReportProtocol):
    layer_cost_reports: List[LayerCostReport]
    new_profile: KoswatProfileBase
    old_profile: KoswatProfileBase

    def __init__(self) -> None:
        self.layer_cost_reports = []
        self.new_profile = None
        self.old_profile = None

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


class MultiLocationProfileCostReport(ReportProtocol):
    locations: List[PointSurroundings]
    profile_cost_report: ProfileCostReport

    def __init__(self) -> None:
        self.locations = []
        self.profile_cost_report = None

    @property
    def cost_per_km(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost * 1000

    @property
    def total_cost(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_cost * len(self.locations)

    @property
    def total_volume(self) -> float:
        if not self.profile_cost_report or not self.locations:
            return math.nan
        return self.profile_cost_report.total_volume * len(self.locations)

    @property
    def profile_type(self) -> str:
        if not self.profile_cost_report or not self.profile_cost_report.new_profile:
            return ""
        return str(self.profile_cost_report.new_profile)

    def as_dict(self) -> float:
        return dict(
            total_cost=self.total_cost,
            total_volume=self.total_volume,
            profile_type=self.profile_type,
            locations=[_loc.location for _loc in self.locations],
        )


class MultiLocationMultiProfileCostSummary:
    locations_profile_report_list: List[MultiLocationProfileCostReport]

    def __init__(self) -> None:
        self.locations_profile_report_list = []
