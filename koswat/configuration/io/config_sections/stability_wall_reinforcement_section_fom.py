import math
from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)


class StabilitywallReinforcementSectionFom(
    ConfigSectionFomProtocol, KoswatStabilityWallSettings
):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "StabilitywallReinforcementSectionFom":
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

        _section.steepening_polderside_slope = _get_float(
            input_dict.get("versteiling_binnentalud", None)
        )
        _section.min_length_stability_wall = _get_float(
            input_dict.get("min_lengte_stabiliteitswand", None)
        )
        _section.transition_sheetpile_diaphragm_wall = _get_float(
            input_dict.get("overgang_damwand_diepwand", None)
        )
        _section.max_length_stability_wall = _get_float(
            input_dict.get("max_lengte_stabiliteitswand", None)
        )

        return _section
