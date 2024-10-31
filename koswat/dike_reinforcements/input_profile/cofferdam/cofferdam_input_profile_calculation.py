from koswat.configuration.settings import KoswatScenario
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_base import (
    ReinforcementInputProfileCalculationBase,
)
from koswat.dike_reinforcements.input_profile.reinforcement_input_profile_calculation_protocol import (
    ReinforcementInputProfileCalculationProtocol,
)


class CofferdamInputProfileCalculation(
    ReinforcementInputProfileCalculationBase,
    ReinforcementInputProfileCalculationProtocol,
):
    base_profile: KoswatProfileProtocol
    reinforcement_settings: KoswatReinforcementSettings
    scenario: KoswatScenario

    def __init__(self) -> None:
        self.base_profile = None
        self.scenario = None

    def _calculate_new_kruin_hoogte(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        return base_data.kruin_hoogte + scenario.d_h

    def _calculate_new_binnen_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        ( Kruin_Breedte_Oud
            + (Kruin_Hoogte_Oud-Binnen_Maaiveld_Oud)
                *Binnen_Talud_Oud-Kruin_Breedte_Nieuw)
        /(Kruin_Hoogte_Oud+dH)
        """
        _mid_operand = base_data.binnen_talud * (
            base_data.kruin_hoogte - base_data.binnen_maaiveld
        )
        _operand = base_data.kruin_breedte + _mid_operand - scenario.crest_width
        _dividend = base_data.kruin_hoogte - base_data.binnen_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_new_buiten_talud(
        self, base_data: KoswatInputProfileBase, scenario: KoswatScenario
    ) -> float:
        """
        Kruin_Hoogte_Oud*Buiten_Talud_Oud
        /(Kruin_Hoogte_Oud+dH)
        """
        _operand = (
            base_data.kruin_hoogte - base_data.buiten_maaiveld
        ) * base_data.buiten_talud
        _dividend = base_data.kruin_hoogte - base_data.buiten_maaiveld + scenario.d_h
        return _operand / _dividend

    def _calculate_length_coffer_dam(
        self,
        old_data: KoswatInputProfileProtocol,
        cofferdam_settings: KoswatCofferdamSettings,
        soil_binnen_berm_breedte: float,
        new_kruin_hoogte: float,
    ) -> float:
        """
        Identical to calculation of Stability wall
        """
        if soil_binnen_berm_breedte == 0:
            # Length of wall is not determined by piping.
            _length_piping = 0.0
        else:
            _length_piping = (
                (soil_binnen_berm_breedte / 6)
                + (new_kruin_hoogte - 0.5)
                - old_data.aquifer
            )
        _length_stability = (new_kruin_hoogte - 0.5) - (old_data.pleistoceen - 1)
        return round(
            min(
                max(
                    _length_piping,
                    _length_stability,
                    cofferdam_settings.min_length_cofferdam,
                ),
                cofferdam_settings.max_length_cofferdam,
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

    def _calculate_new_input_profile(
        self,
        base_data: KoswatInputProfileBase,
        cofferdam_settings: KoswatCofferdamSettings,
        scenario: KoswatScenario,
    ) -> CofferDamInputProfile:
        _new_data = CofferDamInputProfile()
        _new_data.dike_section = base_data.dike_section
        _new_data.buiten_maaiveld = base_data.buiten_maaiveld
        _new_data.buiten_talud = self._calculate_new_buiten_talud(base_data, scenario)
        _new_data.buiten_berm_hoogte = base_data.buiten_berm_hoogte
        _new_data.buiten_berm_breedte = base_data.buiten_berm_breedte
        _new_data.kruin_hoogte = self._calculate_new_kruin_hoogte(base_data, scenario)
        _new_data.kruin_breedte = scenario.crest_width
        _new_data.binnen_talud = self._calculate_new_binnen_talud(base_data, scenario)
        _new_data.binnen_berm_breedte = 0
        _new_data.binnen_berm_hoogte = base_data.binnen_maaiveld
        _new_data.binnen_maaiveld = base_data.binnen_maaiveld
        _soil_binnen_berm_breedte = self._calculate_soil_binnen_berm_breedte(
            base_data, _new_data, scenario
        )
        _new_data.grondprijs_bebouwd = base_data.grondprijs_bebouwd
        _new_data.grondprijs_onbebouwd = base_data.grondprijs_onbebouwd
        _new_data.factor_zetting = base_data.factor_zetting
        _new_data.pleistoceen = base_data.pleistoceen
        _new_data.aquifer = base_data.aquifer
        _new_data.construction_length = self._calculate_length_coffer_dam(
            base_data,
            cofferdam_settings,
            _soil_binnen_berm_breedte,
            _new_data.kruin_hoogte,
        )
        _new_data.construction_type = self._determine_construction_type(
            _new_data.construction_length
        )
        _new_data.soil_surtax_factor = cofferdam_settings.soil_surtax_factor
        _new_data.constructive_surtax_factor = (
            cofferdam_settings.constructive_surtax_factor
        )
        _new_data.land_purchase_surtax_factor = None
        return _new_data

    def build(self) -> CofferDamInputProfile:
        return self._calculate_new_input_profile(
            self.base_profile.input_data,
            self.reinforcement_settings.cofferdam_settings,
            self.scenario,
        )
