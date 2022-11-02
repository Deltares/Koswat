import math

from koswat.cost_report.layer.layer_cost_report import LayerCostReport


class TestLayerCostReport:
    def test_initialize(self):
        _report = LayerCostReport()
        assert isinstance(_report, LayerCostReport)
        assert not _report.new_layer
        assert not _report.old_layer
        assert not _report.added_layer
        assert math.isnan(_report.total_volume)
        assert math.isnan(_report.total_cost)
