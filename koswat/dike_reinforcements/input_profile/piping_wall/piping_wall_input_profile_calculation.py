from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.piping_wall.piping_wall_input_profile import (
    PipingWallInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class PipingWallInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_length_piping_wall(
        self,
        old_data: KoswatInputProfileBase,
        piping_wall_settings: KoswatPipingWallSettings,
        seepage_length: float,
    ) -> float:
        if seepage_length == 0:
            # No wall is needed.
            return 0
        _length_piping = (
            (seepage_length / 6)
            + (old_data.polderside_ground_level - old_data.aquifer)
            + 1
        )
        return round(
            min(
                max(
                    _length_piping,
                    piping_wall_settings.min_length_piping_wall,
                ),
                piping_wall_settings.max_length_piping_wall,
            ),
            1,
        )

    def _determine_construction_type(
        self, overgang: float, construction_length: float
    ) -> ConstructionTypeEnum | None:
        if construction_length == 0:
            return None
        elif construction_length <= overgang:
            return ConstructionTypeEnum.CB_DAMWAND
        else:
            return ConstructionTypeEnum.DAMWAND_ONVERANKERD

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        soil_settings: KoswatSoilSettings,
        piping_wall_settings: KoswatPipingWallSettings,
        scenario: KoswatScenario,
    ) -> PipingWallInputProfile:
        _new_data = PipingWallInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.waterside_ground_level = base_data.waterside_ground_level
        _new_data.polderside_ground_level = base_data.polderside_ground_level
        _new_data.waterside_slope = scenario.waterside_slope
        _new_data.waterside_berm_height = (
            self._calculate_soil_new_waterside_berm_height(base_data, scenario)
        )
        _new_data.waterside_berm_width = base_data.waterside_berm_width
        _new_data.crest_height = self._calculate_soil_new_crest_height(
            base_data, scenario
        )
        _new_data.crest_width = scenario.crest_width

        _dike_height_old = base_data.crest_height - base_data.polderside_ground_level
        _berm_height_old = (
            base_data.polderside_berm_height - base_data.polderside_ground_level
        )
        _berm_factor_old = _berm_height_old / _dike_height_old

        if _berm_factor_old > soil_settings.max_berm_height_factor:
            _berm_old_is_stability = True
        else:
            _berm_old_is_stability = False

        _dikebase_stability_old = (
            base_data.crest_width
            + _dike_height_old * base_data.polderside_slope
            + _berm_old_is_stability * base_data.polderside_berm_width
        )
        _dikebase_piping_old = (
            base_data.crest_width
            + _dike_height_old * base_data.polderside_slope
            + base_data.polderside_berm_width
        )

        _dike_height_new = _new_data.crest_height - _new_data.polderside_ground_level
        _dikebase_heigth_new = (
            scenario.d_h * _new_data.waterside_slope
            + _new_data.crest_width
            + _dike_height_new * base_data.polderside_slope
        )
        _dikebase_stability_new = _dikebase_stability_old + scenario.d_s
        _dikebase_piping_new = max(
            _dikebase_piping_old, _dikebase_heigth_new, _dikebase_stability_new
        )
        _dikebase_piping_needed = _dikebase_piping_old + scenario.d_p
        _seepage_length = max(_dikebase_piping_needed - _dikebase_piping_new, 0)

        # Is a berm for piping neccesary --> Maybe there was an old one??
        if _dikebase_piping_new > max(_dikebase_heigth_new, _dikebase_stability_new):
            _new_data.polderside_berm_width = _dikebase_piping_new - max(
                _dikebase_heigth_new, _dikebase_stability_new
            )
            _new_data.polderside_slope = self._calculate_soil_new_polderside_slope(
                base_data, scenario, _dikebase_heigth_new, _dikebase_stability_new
            )
            # extend existing berm?
            if base_data.polderside_berm_width > 0 and _dikebase_piping_old > max(
                _dikebase_heigth_new, _dikebase_stability_new
            ):
                _new_data.polderside_berm_height = (
                    self._calculate_soil_new_polderside_berm_height_piping(
                        base_data, _new_data, soil_settings, True
                    )
                )
            else:
                _new_data.polderside_berm_height = (
                    self._calculate_soil_new_polderside_berm_height_piping(
                        base_data, _new_data, soil_settings, False
                    )
                )
        else:
            # Is measure for stability neccesary?
            if _dikebase_stability_new > _dikebase_heigth_new:
                # in case of existing stab berm
                if _berm_old_is_stability:
                    _new_data.polderside_berm_width = (
                        _dikebase_stability_new - _dikebase_heigth_new
                    )
                    _new_data.polderside_berm_height = (
                        _berm_factor_old * _dike_height_new
                        + _new_data.polderside_ground_level
                    )
                    _new_data.polderside_slope = base_data.polderside_slope
                else:
                    _new_data.polderside_berm_width = 0
                    _new_data.polderside_berm_height = base_data.polderside_ground_level
                    _new_data.polderside_slope = (
                        self._calculate_soil_new_polderside_slope(
                            base_data,
                            scenario,
                            _dikebase_heigth_new,
                            _dikebase_stability_new,
                        )
                    )
            else:
                _new_data.polderside_berm_width = 0
                _new_data.polderside_berm_height = base_data.polderside_ground_level
                _new_data.polderside_slope = base_data.polderside_slope

        _new_data.ground_price_builtup = base_data.ground_price_builtup
        _new_data.ground_price_unbuilt = base_data.ground_price_unbuilt
        _new_data.factor_settlement = base_data.factor_settlement
        _new_data.pleistocene = base_data.pleistocene
        _new_data.aquifer = base_data.aquifer
        _new_data.construction_length = self._calculate_length_piping_wall(
            base_data, piping_wall_settings, _seepage_length
        )
        _new_data.construction_type = self._determine_construction_type(
            piping_wall_settings.transition_cbwall_sheetpile,
            _new_data.construction_length,
        )
        _new_data.soil_surtax_factor = piping_wall_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = (
            piping_wall_settings.constructive_surtax_factor
        )
        _new_data.land_purchase_surtax_factor = (
            piping_wall_settings.land_purchase_surtax_factor
        )
        return _new_data

    def build(self) -> PipingWallInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.soil_settings,
            self.reinforcement_settings.piping_wall_settings,
            self.scenario,
        )
