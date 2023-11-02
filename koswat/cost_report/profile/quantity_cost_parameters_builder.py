import logging

from koswat.configuration.settings.costs.dike_profile_costs_settings import (
    DikeProfileCostsSettings,
)
from koswat.configuration.settings.costs.koswat_costs_settings import (
    KoswatCostsSettings,
)
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.core.protocols import BuilderProtocol
from koswat.cost_report.profile.quantity_cost_parameters import (
    ConstructionCostParameter,
    QuantityCostParameters,
    SoilCostParameter,
)
from koswat.cost_report.profile.quantity_cost_parameters_calculator import (
    QuantityCostParametersCalculator,
)
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_protocol import (
    ReinforcementInputProfileProtocol,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)


class QuantityCostParametersBuilder(BuilderProtocol):
    reinforced_profile: ReinforcementProfileProtocol
    koswat_costs_settings: KoswatCostsSettings

    def __init__(self) -> None:
        self.reinforced_profile = None
        self.koswat_costs_settings = None

    def build(self) -> QuantityCostParameters:
        if not self.reinforced_profile:
            raise ValueError("No reinforced profile provided.")
        if not self.koswat_costs_settings:
            raise ValueError("No koswat costs settings provided.")

        _quantity_parameters = QuantityCostParameters()
        self._set_quantity_cost_parameters(
            _quantity_parameters, self.koswat_costs_settings.dike_profile_costs
        )
        return _quantity_parameters

    def _get_quantity_cost_calculator(
        self,
    ) -> QuantityCostParametersCalculator | None:
        _calculator = QuantityCostParametersCalculator()
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
        _calculator.construction_type = (
            self.reinforced_profile.input_data.construction_type
        )
        return _calculator

    def _get_surtaxes(self) -> tuple[float, float, float]:
        if not self.reinforced_profile:
            return (1, 1, 1)
        _soil_surtax = self.koswat_costs_settings.surtax_costs.get_soil_surtax(
            self.reinforced_profile.input_data.soil_surtax_factor
        )
        _constructive_surtax = (
            self.koswat_costs_settings.surtax_costs.get_constructive_surtax(
                self.reinforced_profile.input_data.constructive_surtax_factor
            )
        )
        _land_purchase_surtax = (
            self.koswat_costs_settings.surtax_costs.get_land_purchase_surtax(
                self.reinforced_profile.input_data.land_purchase_surtax_factor
            )
        )
        return (_soil_surtax, _constructive_surtax, _land_purchase_surtax)

    def _get_soil_cost_parameter(
        self, quantity: float, cost: float
    ) -> SoilCostParameter:
        _scp = SoilCostParameter()
        _scp.quantity = quantity
        _scp.cost = cost
        _scp.surtax = self.koswat_costs_settings.surtax_costs.get_soil_surtax(
            self.reinforced_profile.input_data.soil_surtax_factor
        )

        return _scp

    def _get_land_purchase_cost_parameter(
        self, quantity: float, input_data: ReinforcementInputProfileProtocol
    ) -> SoilCostParameter:
        _lpcp = SoilCostParameter()
        _lpcp.quantity = quantity
        if input_data.reinforcement_domain_name == "Grondmaatregel profiel":
            _lpcp.cost = input_data.grondprijs_onbebouwd
        else:
            _lpcp.cost = input_data.grondprijs_bebouwd
        _lpcp.surtax = self.koswat_costs_settings.surtax_costs.get_land_purchase_surtax(
            self.reinforced_profile.input_data.land_purchase_surtax_factor
        )

        return _lpcp

    def _get_construction_cost_parameter(
        self, length: float, construction_type: ConstructionTypeEnum | None
    ) -> ConstructionCostParameter:
        _ccp = ConstructionCostParameter()
        _ccp.quantity = length
        if not self.koswat_costs_settings.construction_costs:
            _ccp.factors = None
        else:
            _ccp.factors = (
                self.koswat_costs_settings.construction_costs.get_construction_factors(
                    construction_type
                )
            )
        _ccp.surtax = self.koswat_costs_settings.surtax_costs.get_constructive_surtax(
            self.reinforced_profile.input_data.constructive_surtax_factor
        )

        return _ccp

    def _set_quantity_cost_parameters(
        self,
        qc_parameters: QuantityCostParameters,
        dike_profile_costs: DikeProfileCostsSettings,
    ) -> None:
        _qcp = self._get_quantity_cost_calculator()
        if not _qcp:
            return
        qc_parameters.reused_grass_volume = self._get_soil_cost_parameter(
            _qcp.get_reused_grass_volume(), dike_profile_costs.reused_layer_grass_m3
        )
        qc_parameters.new_grass_volume = self._get_soil_cost_parameter(
            _qcp.get_aanleg_grass_volume(), dike_profile_costs.added_layer_grass_m3
        )
        qc_parameters.new_clay_volume = self._get_soil_cost_parameter(
            _qcp.get_aanleg_clay_volume(), dike_profile_costs.added_layer_clay_m3
        )
        qc_parameters.reused_core_volume = self._get_soil_cost_parameter(
            _qcp.get_reused_core_volume(), dike_profile_costs.reused_layer_core_m3
        )
        qc_parameters.new_core_volume = self._get_soil_cost_parameter(
            _qcp.get_aanleg_core_volume(), dike_profile_costs.added_layer_sand_m3
        )
        qc_parameters.removed_material_volume = self._get_soil_cost_parameter(
            _qcp.get_removed_material_volume(), dike_profile_costs.disposed_material_m3
        )
        qc_parameters.new_grass_layer_surface = self._get_soil_cost_parameter(
            _qcp.new_grass_layer_surface, dike_profile_costs.profiling_layer_grass_m2
        )
        qc_parameters.new_clay_layer_surface = self._get_soil_cost_parameter(
            _qcp.new_clay_layer_surface, dike_profile_costs.profiling_layer_clay_m2
        )
        qc_parameters.new_core_layer_surface = self._get_soil_cost_parameter(
            _qcp.new_core_layer_surface, dike_profile_costs.profiling_layer_sand_m2
        )
        qc_parameters.new_maaiveld_surface = self._get_soil_cost_parameter(
            _qcp.new_maaiveld_surface, dike_profile_costs.bewerken_maaiveld_m2
        )
        qc_parameters.land_purchase_surface = self._get_land_purchase_cost_parameter(
            _qcp.new_maaiveld_surface, self.reinforced_profile.input_data
        )
        qc_parameters.construction_length = self._get_construction_cost_parameter(
            _qcp.construction_length, _qcp.construction_type
        )
