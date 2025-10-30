from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_fom_protocol import (
    ConfigSectionFomProtocol,
)
from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)


class VPSReinforcementSectionFom(ConfigSectionFomProtocol, KoswatVPSSettings):
    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any], set_defaults: bool
    ) -> "VPSReinforcementSectionFom":
        _section = cls()

        _section.active = SectionConfigHelper.get_bool(
            input_dict.get("actief", None), set_defaults
        )

        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            return SectionConfigHelper.get_enum(input_val, set_defaults)

        _section.soil_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grond", None)
        )
        _section.constructive_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_constructief", None)
        )
        _section.land_purchase_surtax_factor = _get_enum(
            input_dict.get("min_lengte_kistdam", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            return SectionConfigHelper.get_float(input_val, set_defaults)

        _section.polderside_berm_width_vps = _get_float(
            input_dict.get("binnen_berm_breedte_vps", None)
        )

        return _section
