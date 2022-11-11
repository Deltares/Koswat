from __future__ import annotations

from koswat.calculations.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.cost_report.profile.volume_cost_parameters_calculator import (
    VolumeCostParametersCalculator,
)


class VolumeCostParameter:
    volume: float
    cost: float


class VolumeCostParameters:
    reused_grass_volume: VolumeCostParameter
    aanleg_grass_volume: VolumeCostParameter
    aanleg_clay_volume: VolumeCostParameter
    reused_core_volume: VolumeCostParameter
    aanleg_core_volume: VolumeCostParameter
    removed_material_volume: VolumeCostParameter
    new_grass_layer_surface: VolumeCostParameter
    new_clay_layer_surface: VolumeCostParameter
    new_core_layer_surface: VolumeCostParameter
    new_maaiveld_surface: VolumeCostParameter

    @classmethod
    def from_reinforced_profile(
        cls, reinforced_profile: ReinforcementProfileProtocol
    ) -> VolumeCostParameters:
        def _create(volume: float, cost: float) -> VolumeCostParameter:
            _vp = VolumeCostParameter()
            _vp.volume = volume
            _vp.cost = cost
            return _vp

        _volume_parameters = cls()
        _vcp = VolumeCostParametersCalculator.from_reinforced_profile(
            reinforced_profile
        )
        _volume_parameters.reused_grass_volume = _create(
            _vcp.get_reused_grass_volume(), 6.04
        )
        _volume_parameters.aanleg_grass_volume = _create(
            _vcp.get_aanleg_grass_volume(), 12.44
        )
        _volume_parameters.aanleg_clay_volume = _create(
            _vcp.get_aanleg_clay_volume(), 18.05
        )
        _volume_parameters.reused_core_volume = _create(
            _vcp.get_reused_core_volume(), 4.67
        )
        _volume_parameters.aanleg_core_volume = _create(
            _vcp.get_aanleg_core_volume(), 10.98
        )
        _volume_parameters.removed_material_volume = _create(
            _vcp.get_removed_material_volume(), 7.07
        )
        _volume_parameters.new_grass_layer_surface = _create(
            _vcp.new_grass_layer_surface, 0.88
        )
        _volume_parameters.new_clay_layer_surface = _create(
            _vcp.new_clay_layer_surface, 0.65
        )
        _volume_parameters.new_core_layer_surface = _create(
            _vcp.new_core_layer_surface, 0.6
        )
        _volume_parameters.new_maaiveld_surface = _create(
            _vcp.new_maaiveld_surface, 0.25
        )
        return _volume_parameters
