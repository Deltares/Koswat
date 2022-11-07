import math

from koswat.cost_report.layer.base_layer_cost_report import BaseLayerCostReport


class TestBaseLayerCostReport:
    def test_initialize(self):
        _report = BaseLayerCostReport()
        assert isinstance(_report, BaseLayerCostReport)
        assert not _report.new_layer
        assert not _report.old_layer
        assert not _report.added_layer
        assert math.isnan(_report.total_volume)
        assert math.isnan(_report.total_cost)
