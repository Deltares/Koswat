from typing import Protocol

from shapely.geometry import Polygon
from typing_extensions import runtime_checkable

from koswat.builder_protocol import BuilderProtocol
from koswat.cost_report.layer.layer_cost_report_protocol import LayerCostReportProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol


@runtime_checkable
class LayerCostReportBuilderProtocol(BuilderProtocol, Protocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol
    base_core_geometry: Polygon

    def build(self) -> LayerCostReportProtocol:
        """
        Generates a `LayerCostReportProtocol` based on the required properties.

        Returns:
            LayerCostReportProtocol: Instance of a `LayerCostReportProtocol`.
        """
        pass
