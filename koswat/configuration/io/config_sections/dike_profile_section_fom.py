import math
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class DikeProfileSectionFom(ConfigSectionFomProtocol, KoswatInputProfileBase):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "DikeProfileSectionFom":
        _section = cls()

        def _get_float(input_val: Optional[str]) -> float:
            if input_val is not None:
                return float(input_val)
            return math.nan if set_defaults else None

        _section.waterside_ground_level = _get_float(
            input_dict.get("buiten_maaiveld", None)
        )
        _section.waterside_slope = _get_float(input_dict.get("buiten_talud", None))
        _section.waterside_berm_height = _get_float(
            input_dict.get("buiten_berm_hoogte", None)
        )
        _section.waterside_berm_width = _get_float(
            input_dict.get("buiten_berm_lengte", None)
        )
        _section.crest_height = _get_float(input_dict.get("kruin_hoogte", None))
        _section.crest_width = _get_float(input_dict.get("kruin_breedte", None))
        _section.polderside_ground_level = _get_float(
            input_dict.get("binnen_maaiveld", None)
        )
        _section.polderside_slope = _get_float(input_dict.get("binnen_talud", None))
        _section.polderside_berm_height = _get_float(
            input_dict.get("binnen_berm_hoogte", None)
        )
        _section.polderside_berm_width = _get_float(
            input_dict.get("binnen_berm_lengte", None)
        )
        _section.ground_price_builtup = _get_float(
            input_dict.get("grondprijs_bebouwd", None)
        )
        _section.ground_price_unbuilt = _get_float(
            input_dict.get("grondprijs_onbebouwd", None)
        )
        _section.factor_settlement = _get_float(input_dict.get("factorzetting", None))
        _section.pleistocene = _get_float(input_dict.get("pleistoceen", None))
        _section.aquifer = _get_float(input_dict.get("aquifer", None))
        _section.thickness_cover_layer = _get_float(
            input_dict.get("dikte_deklaag", None)
        )
        _section.thickness_grass_layer = _get_float(
            input_dict.get("dikte_graslaag", None)
        )
        _section.thickness_clay_layer = _get_float(
            input_dict.get("dikte_kleilaag", None)
        )

        return _section
