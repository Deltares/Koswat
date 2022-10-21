from typing import Protocol

from koswat.builder_protocol import BuilderProtocol
from koswat.cost_report.layer.layer_cost_report import LayerCostReport
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


class LayerCostReportBuilderProtocol(BuilderProtocol, Protocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None

    def build(self) -> LayerCostReport:
        pass
