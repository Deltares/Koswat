import math
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
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

        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            if input_val:
                return SurtaxFactorEnum[input_val.upper()]
            return SurtaxFactorEnum.NORMAAL if set_defaults else None

        _section.soil_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grond", None)
        )
        _section.constructive_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_constructief", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            if input_val is not None:
                return float(input_val)
            return math.nan if set_defaults else None

        _section.min_length_cofferdam = _get_float(
            input_dict.get("min_lengte_kistdam", None)
        )
        _section.max_length_cofferdam = _get_float(
            input_dict.get("max_lengte_kistdam", None)
        )
        return _section
