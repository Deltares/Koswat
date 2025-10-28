import math
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class DikeProfileSectionFom(ConfigSectionFomProtocol, KoswatInputProfileBase):
    def _set_properties_from_dict(
        self, input_dict: dict[str, Any], set_def: bool
    ) -> None:
        def _get_float(input_val: Optional[str]) -> float:
            if input_val is not None:
                return float(input_val)
            return math.nan if set_def else None

        self.waterside_ground_level = _get_float(
            input_dict.get("buiten_maaiveld", None)
        )
        self.waterside_slope = _get_float(input_dict.get("buiten_talud", None))
        self.waterside_berm_height = _get_float(
            input_dict.get("buiten_berm_hoogte", None)
        )
        self.waterside_berm_width = _get_float(
            input_dict.get("buiten_berm_lengte", None)
        )
        self.crest_height = _get_float(input_dict.get("kruin_hoogte", None))
        self.crest_width = _get_float(input_dict.get("kruin_breedte", None))
        self.polderside_ground_level = _get_float(
            input_dict.get("binnen_maaiveld", None)
        )
        self.polderside_slope = _get_float(input_dict.get("binnen_talud", None))
        self.polderside_berm_height = _get_float(
            input_dict.get("binnen_berm_hoogte", None)
        )
        self.polderside_berm_width = _get_float(
            input_dict.get("binnen_berm_lengte", None)
        )
        self.ground_price_builtup = _get_float(
            input_dict.get("grondprijs_bebouwd", None)
        )
        self.ground_price_unbuilt = _get_float(
            input_dict.get("grondprijs_onbebouwd", None)
        )
        self.factor_settlement = _get_float(input_dict.get("factorzetting", None))
        self.pleistocene = _get_float(input_dict.get("pleistoceen", None))
        self.aquifer = _get_float(input_dict.get("aquifer", None))
        self.thickness_cover_layer = _get_float(input_dict.get("dikte_deklaag", None))
        self.thickness_grass_layer = _get_float(input_dict.get("dikte_graslaag", None))
        self.thickness_clay_layer = _get_float(input_dict.get("dikte_kleilaag", None))

    @classmethod
    def from_config(cls, input_dict: dict[str, Any]) -> "DikeProfileSectionFom":
        _section = cls()
        _section._set_properties_from_dict(input_dict, set_def=False)
        return _section

    @classmethod
    def from_config_set_defaults(
        cls, input_dict: dict[str, Any]
    ) -> "DikeProfileSectionFom":
        _section = cls()
        _section._set_properties_from_dict(input_dict, set_def=True)
        return _section

    def merge(self, other: "DikeProfileSectionFom") -> "DikeProfileSectionFom":
        if not isinstance(other, DikeProfileSectionFom):
            raise TypeError(
                "Can only merge with another DikeProfileSectionFom instance."
            )

        def _merge_attr(attr_name: str) -> None:
            this_value = getattr(self, attr_name)
            if this_value is None:
                setattr(self, attr_name, getattr(other, attr_name))

        for _attr in vars(self).keys():
            _merge_attr(_attr)

        return self
