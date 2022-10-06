import math

import pytest

from koswat.koswat_report import (
    LayerCostReport,
    MultipleLocationProfileCostReport,
    ProfileCostReport,
)


class TestLayerCostReport:
    def test_initialize(self):
        _report = LayerCostReport()
        assert isinstance(_report, LayerCostReport)
        assert not _report.new_layer
        assert not _report.old_layer
        assert math.isnan(_report.total_volume)
        assert math.isnan(_report.total_cost)


class TestProfileCostReport:
    def test_initialize(self):
        _report = ProfileCostReport()
        assert isinstance(_report, ProfileCostReport)
        assert not _report.new_profile
        assert not _report.old_profile
        assert not any(_report.layer_cost_reports)
        assert math.isnan(_report.total_cost)
        assert math.isnan(_report.total_volume)


class TestMultipleLocationProfileCostReport:
    def test_initialize(self):
        _report = MultipleLocationProfileCostReport()
        assert isinstance(_report, MultipleLocationProfileCostReport)
        assert not any(_report.locations)
        assert not _report.profile_cost_report
        assert not _report.profile_type
        assert math.isnan(_report.total_cost)
        assert math.isnan(_report.total_volume)
        assert math.isnan(_report.cost_per_km)
