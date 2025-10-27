from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum


class VPSReinforcementSectionFom(ConfigSectionFomBase):
    active: bool
    polderside_berm_width_vps: float
    soil_surtax_factor: SurtaxFactorEnum
    constructive_surtax_factor: SurtaxFactorEnum
    land_purchase_surtax_factor: SurtaxFactorEnum

    _bool_mappings = dict(
        actief="active",
    )
    _float_mappings = dict(
        binnen_berm_breedte_vps="polderside_berm_width_vps",
    )
    _surtax_mappings = dict(
        opslag_factor_grond="soil_surtax_factor",
        opslagfactor_constructief="constructive_surtax_factor",
        opslagfactor_grondaankoop="land_purchase_surtax_factor",
    )
