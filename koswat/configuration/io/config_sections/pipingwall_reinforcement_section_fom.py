from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class PipingwallReinforcementSectionFom(ConfigSectionFomBase):
    min_length_piping_wall: float
    transition_cbwall_sheetpile: float
    max_length_piping_wall: float
    soil_surtax_factor: SurtaxFactorEnum
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _float_mappings = dict(
        min_lengte_pijpwand="min_length_piping_wall",
        overgang_cbwand_damwand="transition_cbwall_sheetpile",
        max_lengte_pijpwand="max_length_piping_wall",
    )
    _surtax_mappings = dict(
        opslagfactor_grond="soil_surtax_factor",
        opslagfactor_constructief="constructive_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )
