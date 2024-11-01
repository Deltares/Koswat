from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import KoswatReinforcementSettings
from koswat.configuration.settings.reinforcements.koswat_soil_settings import KoswatSoilSettings
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import KoswatStabilityWallSettings
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import ReinforcementInputProfileCalculationBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import ReinforcementInputProfileCalculationProtocol
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile import StabilityWallInputProfile

class StabilityWallInputProfileCalculation(ReinforcementInputProfileCalculationBase, ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_stability_wall(self, old_data: KoswatInputProfileProtocol, stability_wall_settings: KoswatStabilityWallSettings, seepage_length: float, stab_wall: bool, new_kruin_hoogte: float) -> float:
        if stab_wall:
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
        else:
            _length_stability = 0
            if seepage_length == 0:                                          
                # Length of wall is not determined by piping.
                _length_piping = 0.0
            else:
                # Length of wall zoals bij kwelscherm
                _length_piping = (
                    (seepage_length / 6)
                    + (old_data.binnen_maaiveld - old_data.aquifer)
                    + 1  # 1 m in bestaande dijklichaam
                )

        return round(
            min(
                max(
                    _length_piping,
                    _length_stability,
                    stability_wall_settings.min_lengte_stabiliteitswand,
                ),
                stability_wall_settings.max_lengte_stabiliteitswand,
            ),
            1,
        )

    def _calculate_new_binnen_talud(self, base_data: KoswatInputProfileBase, scenario: KoswatScenario, stability_wall_settings: KoswatStabilityWallSettings, _dikebase_piping_old: float) -> float:
        _operand = _dikebase_piping_old - scenario.d_h * scenario.buiten_talud - scenario.kruin_breedte
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        return max(stability_wall_settings.versteiling_binnentalud, _operand/_dividend)

    def _determine_construction_type(
        self,
        overgang: float,
        construction_length: float,
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        elif construction_length <= overgang:
            return ConstructionTypeEnum.DAMWAND_VERANKERD
        else:
            return ConstructionTypeEnum.DIEPWAND

    def _calculate_new_input_profile(self, base_data: KoswatInputProfileProtocol, soil_settings: KoswatSoilSettings, stability_wall_settings: KoswatStabilityWallSettings, scenario: KoswatScenario) -> StabilityWallInputProfile:
        _new_data = StabilityWallInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = self._calculate_soil_new_buiten_berm_hoogte(base_data, scenario)
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_soil_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.kruin_breedte
        
        _dike_height_old = base_data.kruin_hoogte - base_data.binnen_maaiveld
        _berm_height_old = base_data.binnen_berm_hoogte - base_data.binnen_maaiveld
        _berm_factor_old = _berm_height_old/_dike_height_old
        
        if _berm_factor_old > soil_settings.max_bermhoogte_factor:
            _berm_old_is_stability = True
        else:
            _berm_old_is_stability = False

        _dikebase_stability_old = base_data.kruin_breedte + _dike_height_old*base_data.binnen_talud + _berm_old_is_stability*base_data.binnen_berm_breedte
        _dikebase_piping_old = base_data.kruin_breedte + _dike_height_old*base_data.binnen_talud + base_data.binnen_berm_breedte

        _dike_height_new = _new_data.kruin_hoogte-_new_data.binnen_maaiveld
        _dikebase_heigth_new = scenario.d_h*_new_data.buiten_talud + _new_data.kruin_breedte + _dike_height_new*base_data.binnen_talud        
        _dikebase_stability_new = _dikebase_stability_old + scenario.d_s
        _dikebase_piping_new = max(_dikebase_piping_old, _dikebase_heigth_new, _dikebase_stability_new)
        _dikebase_piping_needed = _dikebase_piping_old + scenario.d_p

        # stab measure fits within the current profile, no stab wall neccesary, but wall might be needed for piping    
        if _dikebase_piping_new > max(_dikebase_heigth_new,_dikebase_stability_new):
            _stab_wall = False
            _new_data.binnen_berm_breedte = _dikebase_piping_new - max(_dikebase_heigth_new,_dikebase_stability_new)
            _new_data.binnen_talud = self._calculate_soil_new_binnen_talud(base_data, scenario, _dikebase_heigth_new, _dikebase_stability_new)
            # extend existing berm?
            if base_data.binnen_berm_breedte > 0 and _dikebase_piping_old > max(_dikebase_heigth_new, _dikebase_stability_new):
                _new_data.binnen_berm_hoogte = self._calculate_soil_new_binnen_berm_hoogte_piping(base_data, _new_data, scenario, soil_settings, True)
            else:
                _new_data.binnen_berm_hoogte = self._calculate_soil_new_binnen_berm_hoogte_piping(base_data, _new_data, scenario, soil_settings, False)
        else:
            # stab measure doesn't fit within current profile, extend with steepening of binnen talud
            _stab_wall = True
            _new_data.binnen_berm_breedte = 0
            _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
            _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario, stability_wall_settings, _dikebase_piping_old)
            
        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        
        _dikebase_piping_realized = scenario.d_h * _new_data.buiten_talud + _new_data.kruin_breedte + _dike_height_new * _new_data.binnen_talud + _new_data.binnen_berm_breedte
        _seepage_length = max(_dikebase_piping_needed - _dikebase_piping_realized, 0)
        _new_data.construction_length = self._calculate_length_stability_wall(base_data, stability_wall_settings, _seepage_length, _stab_wall, _new_data.kruin_hoogte)
        _new_data.construction_type = self._determine_construction_type(stability_wall_settings.overgang_damwand_diepwand, _new_data.construction_length)
        _new_data.soil_surtax_factor = stability_wall_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = stability_wall_settings.constructive_surtax_factor
        _new_data.land_purchase_surtax_factor = stability_wall_settings.land_purchase_surtax_factor
        return _new_data

    def build(self) -> StabilityWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.soil_settings,
            self.reinforcement_settings.stability_wall_settings,
            self.scenario,
        )
