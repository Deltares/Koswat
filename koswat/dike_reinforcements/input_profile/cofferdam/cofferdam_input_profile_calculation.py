from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_soil_settings import KoswatSoilSettings
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import KoswatCofferdamSettings
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import KoswatReinforcementSettings
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import CofferDamInputProfile
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import ReinforcementInputProfileCalculationBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import ReinforcementInputProfileCalculationProtocol

class CofferdamInputProfileCalculation(ReinforcementInputProfileCalculationBase, ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_new_buiten_talud(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario) -> float:
        _operand = (base_data.kruin_hoogte - base_data.buiten_maaiveld) * base_data.buiten_talud
        _dividend = base_data.kruin_hoogte - base_data.buiten_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_new_binnen_berm_hoogte(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario) -> float:
        _dike_height_old = base_data.kruin_hoogte - base_data.binnen_maaiveld
        _berm_height_old = base_data.binnen_berm_hoogte - base_data.binnen_maaiveld
        _berm_factor_old = _berm_height_old/_dike_height_old
        return base_data.binnen_berm_hoogte + _berm_factor_old * scenario.d_h

    def _calculate_new_binnen_talud(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario) -> float:
        _operand = (base_data.kruin_hoogte - base_data.binnen_maaiveld) * base_data.binnen_talud
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_length_coffer_dam(self, old_data: KoswatInputProfileProtocol, cofferdam_settings: KoswatCofferdamSettings, seepage_length: float, new_kruin_hoogte: float) -> float:
        _length_stability = (new_kruin_hoogte - 0.5) - (old_data.pleistoceen - 1)
        if seepage_length == 0:
            # Length of wall is not determined by piping.
            _length_piping = 0.0
        else:
            _length_piping = (
                (seepage_length / 6)
                + (new_kruin_hoogte - 0.5)
                - old_data.aquifer
            )
        
        return round(
            min(
                max(
                    _length_piping,
                    _length_stability,
                    cofferdam_settings.min_lengte_kistdam,
                ),
                cofferdam_settings.max_lengte_kistdam,
            ),
            1,
        )

    def _determine_construction_type(
        self,
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        else:
            return ConstructionTypeEnum.KISTDAM

    def _calculate_new_input_profile(self, base_data: KoswatInputProfileBase, soil_settings: KoswatSoilSettings, cofferdam_settings: KoswatCofferdamSettings, scenario: KoswatScenario) -> CofferDamInputProfile:
        _new_data = CofferDamInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte   # maintain current berm waterside
        _new_data.buiten_berm_hoogte = self._calculate_soil_new_buiten_berm_hoogte(base_data, scenario)
        _new_data.buiten_talud = self._calculate_new_buiten_talud(base_data, scenario)
        _new_data.kruin_hoogte = self._calculate_soil_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = base_data.kruin_breedte   # no widening of crest allowed
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.binnen_berm_breedte = base_data.binnen_berm_breedte   # maintain current berm polderside
        _new_data.binnen_berm_hoogte = self._calculate_new_binnen_berm_hoogte(base_data, scenario)
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        
        _seepage_length = scenario.d_p
        _new_data.construction_length = self._calculate_length_coffer_dam(base_data, cofferdam_settings, _seepage_length, _new_data.kruin_hoogte)
        _new_data.construction_type = self._determine_construction_type(_new_data.construction_length)
        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        _new_data.soil_surtax_factor = cofferdam_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = cofferdam_settings.constructive_surtax_factor
        _new_data.land_purchase_surtax_factor = None
        return _new_data

    def build(self) -> CofferDamInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.soil_settings,
            self.reinforcement_settings.cofferdam_settings,
            self.scenario,
        )
