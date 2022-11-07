from shapely.geometry import Polygon

from koswat.cost_report.layer.layer_cost_report_builder_protocol import (
    LayerCostReportBuilderProtocol,
)
from koswat.cost_report.layer.standard_layer_cost_report import StandardLayerCostReport
from koswat.dike.layers.koswat_coating_layer import KoswatCoatingLayer
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayerProtocol
from koswat.geometries.calc_library import (
    get_polygon_coordinates,
    get_polygon_surface_points,
)


class StandardLayerCostReportBuilder(LayerCostReportBuilderProtocol):
    base_layer: KoswatLayerProtocol
    calc_layer: KoswatLayerProtocol
    base_core_geometry: Polygon
    wrapped_calc_geometry: Polygon
    wrapped_base_geometry: Polygon

    def __init__(self) -> None:
        self.base_layer = None
        self.calc_layer = None
        self.base_core_geometry = None
        self.wrapped_calc_geometry = None
        self.wrapped_base_geometry = None

    def build(self) -> StandardLayerCostReport:
        if self.base_layer.material.name != self.calc_layer.material.name:
            raise ValueError("Material differs between layers. Cannot compute costs.")

        # Layer cost report
        _layer_report = StandardLayerCostReport()
        _layer_report.new_layer = self.calc_layer
        _layer_report.old_layer = self.base_layer

        # Removed Layer
        _layer_report.removed_layer = KoswatCoatingLayer()
        _layer_report.removed_layer.material = self.calc_layer.material
        _removed_layer_geometry = self.base_layer.geometry.difference(
            self.base_core_geometry
        )
        if self.wrapped_base_geometry:
            # TODO: Improve this logic.
            _removed_layer_geometry = _removed_layer_geometry.difference(
                self.wrapped_base_geometry
            )
        _layer_report.removed_layer.geometry = _removed_layer_geometry

        # Added layer
        _layer_report.added_layer = KoswatCoatingLayer()
        _layer_report.added_layer.material = self.calc_layer.material
        _added_geometry = self.calc_layer.geometry.difference(
            self.base_core_geometry.union(self.wrapped_calc_geometry)
        )
        _layer_report.added_layer.geometry = _added_geometry
        _layer_report.added_layer.layer_points = get_polygon_coordinates(
            _added_geometry
        )
        _layer_report.added_layer.upper_points = get_polygon_surface_points(
            _added_geometry
        )
        return _layer_report
