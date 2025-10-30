from dataclasses import dataclass
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class InfrastructureSectionFom(KoswatJsonFomProtocol):
    infrastructure: bool
    surtax_factor_roads: SurtaxFactorEnum
    infrastructure_costs_0dh: InfraCostsEnum
    buffer_waterside: float
    roads_class2_width: float
    roads_class24_width: float
    roads_class47_width: float
    roads_class7_width: float
    roads_unknown_width: float

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "InfrastructureSectionFom":
        return cls(
            infrastructure=SectionConfigHelper.get_bool(input_config["infrastructuur"]),
            surtax_factor_roads=SurtaxFactorEnum[
                input_config["opslagfactor_wegen"].upper()
            ],
            infrastructure_costs_0dh=InfraCostsEnum[
                input_config["infrakosten_0dh"].upper()
            ],
            buffer_waterside=SectionConfigHelper.get_float(["buffer_buitendijks"]),
            roads_class2_width=SectionConfigHelper.get_float(["wegen_klasse2_breedte"]),
            roads_class24_width=SectionConfigHelper.get_float(
                ["wegen_klasse24_breedte"]
            ),
            roads_class47_width=SectionConfigHelper.get_float(
                ["wegen_klasse47_breedte"]
            ),
            roads_class7_width=SectionConfigHelper.get_float(["wegen_klasse7_breedte"]),
            roads_unknown_width=SectionConfigHelper.get_float(
                ["wegen_onbekend_breedte"]
            ),
        )
