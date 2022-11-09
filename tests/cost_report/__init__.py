from typing import Type

from shapely.geometry import Point

from koswat.calculations.outside_slope_reinforcement.cofferdam.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.cost_report.profile.profile_cost_report_builder_protocol import (
    ProfileCostReportBuilderProtocol,
)
from koswat.dike.layers.koswat_layers_wrapper import (
    KoswatBaseLayer,
    KoswatLayersWrapper,
)
from koswat.dike.material.koswat_material import KoswatMaterial
from koswat.dike.profile.koswat_profile import KoswatProfileBase


def get_valid_profile_builder(
    builder_type: Type[ProfileCostReportBuilderProtocol],
) -> ProfileCostReportBuilderProtocol:
    _builder = builder_type()
    _ref_point = Point(4.2, 2.4)
    _material_name = "Vibranium"
    _builder.base_profile = KoswatProfileBase()
    _base_layer = KoswatBaseLayer()
    _base_layer.material = KoswatMaterial()
    _base_layer.material.name = _material_name
    _base_layer.geometry = _ref_point.buffer(2)
    _builder.base_profile.layers_wrapper = KoswatLayersWrapper()
    _builder.base_profile.layers_wrapper.base_layer = _base_layer
    _builder.calculated_profile = CofferdamReinforcementProfile()
    _calc_layer = KoswatBaseLayer()
    _calc_layer.material = KoswatMaterial()
    _calc_layer.material.name = _material_name
    _calc_layer.geometry = _ref_point.buffer(4)
    _builder.calculated_profile.layers_wrapper = KoswatLayersWrapper()
    _builder.calculated_profile.layers_wrapper.base_layer = _calc_layer
    return _builder
