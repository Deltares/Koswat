from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)


class CofferdamReinforcementSectionFom(
    ConfigSectionFomProtocol, KoswatCofferdamSettings
):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "CofferdamReinforcementSectionFom":
        _section = cls()

        _active = input_dict.get("actief", None)
        if set_defaults:
            _section.active = SectionConfigHelper.get_bool(_active)
        else:
            _section.active = SectionConfigHelper.get_bool_without_default(_active)

        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            if set_defaults:
                return SectionConfigHelper.get_enum(input_val)
            return SectionConfigHelper.get_enum_without_default(input_val)

        _section.soil_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grond", None)
        )
        _section.constructive_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_constructief", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            if set_defaults:
                return SectionConfigHelper.get_float(input_val)
            return SectionConfigHelper.get_float_without_default(input_val)

        _section.min_length_cofferdam = _get_float(
            input_dict.get("min_lengte_kistdam", None)
        )
        _section.max_length_cofferdam = _get_float(
            input_dict.get("max_lengte_kistdam", None)
        )
        return _section
