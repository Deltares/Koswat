import math
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)


class PipingWallReinforcementSectionFom(
    ConfigSectionFomProtocol, KoswatPipingWallSettings
):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "PipingWallReinforcementSectionFom":
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
        _section.land_purchase_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grondaankoop", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            if input_val is not None:
                return float(input_val)
            return math.nan if set_defaults else None

        _section.min_length_piping_wall = _get_float(
            input_dict.get("min_lengte_kwelscherm", None)
        )
        _section.transition_cbwall_sheetpile = _get_float(
            input_dict.get("overgang_cbwand_damwand", None)
        )
        _section.max_length_piping_wall = _get_float(
            input_dict.get("max_lengte_kwelscherm", None)
        )

        return _section
