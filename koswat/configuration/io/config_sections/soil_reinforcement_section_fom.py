from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)


class SoilReinforcementSectionFom(ConfigSectionFomProtocol, KoswatSoilSettings):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "SoilReinforcementSectionFom":
        _section = cls()

        _section.active = SectionConfigHelper.get_bool(
            input_dict.get("actief", None), set_defaults
        )

        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            return SectionConfigHelper.get_enum(input_val, set_defaults)

        _section.soil_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grond", None)
        )
        _section.land_purchase_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grondaankoop", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            return SectionConfigHelper.get_float(input_val, set_defaults)

        _section.min_berm_height = _get_float(input_dict.get("min_bermhoogte", None))
        _section.max_berm_height_factor = _get_float(
            input_dict.get("max_bermhoogte_factor", None)
        )
        _section.factor_increase_berm_height = _get_float(
            input_dict.get("factor_toename_bermhoogte", None)
        )

        return _section
