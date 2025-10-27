from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class StabilitywallReinforcementSectionFom(ConfigSectionFomBase):
    active: bool
    steepening_polderside_slope: float
    min_length_stability_wall: float
    transition_sheetpile_diaphragm_wall: float
    max_length_stability_wall: float
    soil_surtax_factor: SurtaxFactorEnum
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _bool_mappings = dict(
        actief="active",
    )
    _float_mappings = dict(
        versteiling_binnentalud="steepening_polderside_slope",
        min_lengte_stabiliteitswand="min_length_stability_wall",
        overgang_damwand_diepwand="transition_sheetpile_diaphragm_wall",
        max_lengte_stabiliteitswand="max_length_stability_wall",
    )
    _surtax_mappings = dict(
        opslagfactor_grond="soil_surtax_factor",
        opslagfactor_constructief="constructive_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )
