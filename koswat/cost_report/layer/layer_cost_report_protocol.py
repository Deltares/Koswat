from typing import Protocol

from koswat.cost_report.cost_report_protocol import CostReportProtocol
from koswat.dike.layers.koswat_layer_protocol import KoswatLayerProtocol


class LayerCostReportProtocol(CostReportProtocol, Protocol):
    new_layer: KoswatLayerProtocol
    old_layer: KoswatLayerProtocol
    added_layer: KoswatLayerProtocol
