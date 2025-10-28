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
    def _set_properties_from_dict(
        self, input_dict: dict[str, Any], set_def: bool
    ) -> None:
        def _get_bool(input_val: Optional[str]) -> bool:
            if input_val is not None:
                return bool(input_val)
            return False if set_def else None
        
        self.active = _get_bool(input_dict.get("actief", None))
        
        def _get_enum(input_val: Optional[str]) -> SurtaxFactorEnum:
            if input_val:
                return SurtaxFactorEnum[input_val.upper()]
            return SurtaxFactorEnum.NORMAAL if set_def else None

        self.soil_surtax_factor = _get_enum(input_dict.get("opslagfactor_grond", None))
        self.constructive_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_constructief", None)
        )
        self.land_purchase_surtax_factor = _get_enum(
            input_dict.get("opslagfactor_grondaankoop", None)
        )

        def _get_float(input_val: Optional[str]) -> float:
            if input_val is not None:
                return float(input_val)
            return math.nan if set_def else None

        self.min_length_piping_wall = _get_float(
            input_dict.get("min_lengte_kwelscherm", None)
        )
        self.transition_cbwall_sheetpile = _get_float(
            input_dict.get("overgang_cbwand_damwand", None)
        )
        self.max_length_piping_wall = _get_float(
            input_dict.get("max_lengte_kwelscherm", None)
        )

    @classmethod
    def from_config(
        cls, input_dict: dict[str, Any]
    ) -> "PipingWallReinforcementSectionFom":
        _section = cls()
        _section._set_properties_from_dict(input_dict, set_def=False)
        return _section

    @classmethod
    def from_config_set_defaults(
        cls, input_dict: dict[str, Any]
    ) -> "PipingWallReinforcementSectionFom":
        _section = cls()
        _section._set_properties_from_dict(input_dict, set_def=True)
        return _section

    def merge(
        self, other: "PipingWallReinforcementSectionFom|KoswatPipingWallSettings"
    ) -> "PipingWallReinforcementSectionFom":
        if not isinstance(
            other, (PipingWallReinforcementSectionFom, KoswatPipingWallSettings)
        ):
            raise TypeError(
                "Can only merge with another PipingWallReinforcementSectionFom instance."
            )

        def _merge_attr(attr_name: str) -> None:
            this_value = getattr(self, attr_name)
            if this_value is None:
                setattr(self, attr_name, getattr(other, attr_name))

        for _attr in vars(self).keys():
            _merge_attr(_attr)

        return self
