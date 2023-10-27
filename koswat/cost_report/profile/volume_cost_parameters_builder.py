import logging
from typing import Union

from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.koswat_costs import KoswatCostsSettings
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.profile.volume_cost_parameters import (
    VolumeCostParameter,
    VolumeCostParameters,
)
from koswat.cost_report.profile.volume_cost_parameters_calculator import (
    VolumeCostParametersCalculator,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class VolumeCostParametersBuilder(BuilderProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    koswat_costs: KoswatCostsSettings

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.koswat_costs = None

    def build(self) -> VolumeCostParameters:
        if not self.reinforced_profile:
            raise ValueError("No reinforced profile provided.")
        if not self.koswat_costs:
            raise ValueError("No koswat costs provided.")

        _volume_parameters = VolumeCostParameters()
        self._set_volume_cost_parameters(
            _volume_parameters, self.koswat_costs.dike_profile_costs
        )
        return _volume_parameters

    def _get_volume_cost_calculator(
        self,
    ) -> Union[VolumeCostParametersCalculator, None]:
        _calculator = VolumeCostParametersCalculator()
        if len(self.reinforced_profile.layers_wrapper.layers) != 3:
            logging.error(
                "Only supported reinforcement profiles with 3 layers (Sand - Clay - Grass)."
            )
            return None
        _grass_layer = self.reinforced_profile.layers_wrapper.get_layer(
            KoswatMaterialType.GRASS
        )
        _clay_layer = self.reinforced_profile.layers_wrapper.get_layer(
            KoswatMaterialType.CLAY
        )
        _core_layer = self.reinforced_profile.layers_wrapper.base_layer
        _calculator.grass_layer_removal_volume = (
            _grass_layer.removal_layer_geometry.area
        )
        _calculator.clay_layer_removal_volume = _clay_layer.removal_layer_geometry.area
        _calculator.new_core_layer_volume = _core_layer.new_layer_geometry.area
        _calculator.new_core_layer_surface = _core_layer.new_layer_surface.length
        _calculator.new_clay_layer_volume = _clay_layer.new_layer_geometry.area
        _calculator.new_clay_layer_surface = _clay_layer.new_layer_surface.length
        _calculator.new_grass_layer_volume = _grass_layer.new_layer_geometry.area
        _calculator.new_grass_layer_surface = _grass_layer.new_layer_surface.length
        _calculator.new_maaiveld_surface = (
            self.reinforced_profile.new_ground_level_surface
        )
        _calculator.construction_length = (
            self.reinforced_profile.input_data.construction_length
        )
        return _calculator

    def _get_volume_cost_parameter(
        self, volume: float, cost: float
    ) -> VolumeCostParameter:
        _vp = VolumeCostParameter()
        _vp.volume = volume
        _vp.cost = cost
        return _vp

    def _set_volume_cost_parameters(
        self,
        vc_parameters: VolumeCostParameters,
        dike_profile_costs: DikeProfileCostsSettings,
    ) -> None:
        _vcp = self._get_volume_cost_calculator()
        if not _vcp:
            return
        vc_parameters.reused_grass_volume = self._get_volume_cost_parameter(
            _vcp.get_reused_grass_volume(), dike_profile_costs.reused_layer_grass_m3
        )
        vc_parameters.aanleg_grass_volume = self._get_volume_cost_parameter(
            _vcp.get_aanleg_grass_volume(), dike_profile_costs.added_layer_grass_m3
        )
        vc_parameters.aanleg_clay_volume = self._get_volume_cost_parameter(
            _vcp.get_aanleg_clay_volume(), dike_profile_costs.added_layer_clay_m3
        )
        vc_parameters.reused_core_volume = self._get_volume_cost_parameter(
            _vcp.get_reused_core_volume(), dike_profile_costs.reused_layer_core_m3
        )
        vc_parameters.aanleg_core_volume = self._get_volume_cost_parameter(
            _vcp.get_aanleg_core_volume(), dike_profile_costs.added_layer_sand_m3
        )
        vc_parameters.removed_material_volume = self._get_volume_cost_parameter(
            _vcp.get_removed_material_volume(), dike_profile_costs.disposed_material_m3
        )
        vc_parameters.new_grass_layer_surface = self._get_volume_cost_parameter(
            _vcp.new_grass_layer_surface, dike_profile_costs.profiling_layer_grass_m2
        )
        vc_parameters.new_clay_layer_surface = self._get_volume_cost_parameter(
            _vcp.new_clay_layer_surface, dike_profile_costs.profiling_layer_clay_m2
        )
        vc_parameters.new_core_layer_surface = self._get_volume_cost_parameter(
            _vcp.new_core_layer_surface, dike_profile_costs.profiling_layer_sand_m2
        )
        vc_parameters.new_maaiveld_surface = self._get_volume_cost_parameter(
            _vcp.new_maaiveld_surface, dike_profile_costs.bewerken_maaiveld_m2
        )
        # TODO: KOSWAT issue #104
        vc_parameters.construction_length = self._get_volume_cost_parameter(
            _vcp.construction_length, 0
        )
        return vc_parameters
