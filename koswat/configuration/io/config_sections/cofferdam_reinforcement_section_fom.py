from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class CofferdamReinforcementSectionFom(ConfigSectionFomBase):
    active: bool
    min_length_cofferdam: float
    max_length_cofferdam: float
    soil_surtax_factor: SurtaxFactorEnum
    constructive_surtax_factor: SurtaxFactorEnum

    _bool_mappings = dict(
        actief="active",
    )
    _float_mappings = dict(
        min_lengte_kistdam="min_length_cofferdam",
        max_lengte_kistdam="max_length_cofferdam",
    )
    _surtax_mappings = dict(
        opslagfactor_grond="soil_surtax_factor",
        opslagfactor_constructief="constructive_surtax_factor",
    )
