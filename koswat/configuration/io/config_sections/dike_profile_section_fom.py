import math
from configparser import SectionProxy
from typing import Any

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class DikeProfileSectionFom(ConfigSectionFomBase, KoswatInputProfileBase):

    _bool_mappings = dict()
    _float_mappings = dict(
        buiten_maaiveld="waterside_ground_level",
        buiten_talud="waterside_slope",
        buiten_berm_hoogte="waterside_berm_height",
        buiten_berm_lengte="waterside_berm_width",
        kruin_hoogte="crest_height",
        kruin_breedte="crest_width",
        binnen_maaiveld="polderside_ground_level",
        binnen_talud="polderside_slope",
        binnen_berm_hoogte="polderside_berm_height",
        binnen_berm_lengte="polderside_berm_width",
        grondprijs_bebouwd="ground_price_builtup",
        grondprijs_onbebouwd="ground_price_unbuilt",
        factorzetting="factor_settlement",
        pleistoceen="pleistocene",
        aquifer="aquifer",
        dikte_deklaag="thickness_cover_layer",
        dikte_graslaag="thickness_grass_layer",
        dikte_kleilaag="thickness_clay_layer",
    )

    @classmethod
    def from_ini(cls, ini_config: SectionProxy) -> "DikeProfileSectionFom":
        _section = cls()
        _section._set_float_values(dict(ini_config), cls._float_mappings, math.nan)
        return _section

    @classmethod
    def from_dict(cls, input_dict: dict[str, Any]) -> "DikeProfileSectionFom":
        _section = cls()
        _section._set_float_values(input_dict, cls._float_mappings, None)
        return _section
