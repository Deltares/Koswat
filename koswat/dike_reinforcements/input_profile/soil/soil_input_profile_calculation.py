from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import KoswatReinforcementSettings
from koswat.configuration.settings.reinforcements.koswat_soil_settings import KoswatSoilSettings
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import ReinforcementInputProfileCalculationBase
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import ReinforcementInputProfileCalculationProtocol
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import SoilInputProfile

class SoilInputProfileCalculation(ReinforcementInputProfileCalculationBase, ReinforcementInputProfileCalculationProtocol):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None
        
    def _calculate_new_input_profile(self, base_data: KoswatInputProfileBase, soil_settings: KoswatSoilSettings, scenario: KoswatScenario) -> KoswatInputProfileBase:
        _new_data = SoilInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _new_data.buiten_talud = scenario.buiten_talud
        _new_data.buiten_berm_hoogte = self._calculate_soil_new_buiten_berm_hoogte(base_data, scenario)
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_breedte = scenario.kruin_breedte
        _new_data.kruin_hoogte = self._calculate_soil_new_kruin_hoogte(base_data, scenario)
        
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
        _dikebase_piping_new = _dikebase_piping_old + scenario.d_p

        # Is a berm for piping neccesary?
        if _dikebase_piping_new > max(_dikebase_heigth_new,_dikebase_stability_new):
            _new_data.binnen_berm_breedte = _dikebase_piping_new - max(_dikebase_heigth_new,_dikebase_stability_new)
            _new_data.binnen_talud = self._calculate_soil_new_binnen_talud(base_data, scenario, _dikebase_heigth_new, _dikebase_stability_new)
            # extend existing berm?
            if base_data.binnen_berm_breedte > 0 and _dikebase_piping_old > max(_dikebase_heigth_new, _dikebase_stability_new):
                _new_data.binnen_berm_hoogte = self._calculate_soil_new_binnen_berm_hoogte_piping(base_data, _new_data, scenario, soil_settings, True)
            else:
                _new_data.binnen_berm_hoogte = self._calculate_soil_new_binnen_berm_hoogte_piping(base_data, _new_data, scenario, soil_settings, False)
        else:
            # Is measure for stability neccesary?
            if _dikebase_stability_new > _dikebase_heigth_new:
                # in case of existing stab berm
                if _berm_old_is_stability:
                    _new_data.binnen_berm_breedte = _dikebase_stability_new - _dikebase_heigth_new
                    _new_data.binnen_berm_hoogte = _berm_factor_old * _dike_height_new + _new_data.binnen_maaiveld
                    _new_data.binnen_talud = base_data.binnen_talud
                else:
                    _new_data.binnen_berm_breedte = 0
                    _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
                    _new_data.binnen_talud = self._calculate_soil_new_binnen_talud(base_data, scenario, _dikebase_heigth_new, _dikebase_stability_new)
            else:
                _new_data.binnen_berm_breedte = 0
                _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
                _new_data.binnen_talud = base_data.binnen_talud

        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        _new_data.soil_surtax_factor = soil_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = None
        _new_data.land_purchase_surtax_factor = (soil_settings.land_purchase_surtax_factor)
        return _new_data

    def build(self) -> SoilInputProfile:
        return self._calculate_new_input_profile(self.base_profile.input_data, self.reinforcement_settings.soil_settings, self.scenario)
