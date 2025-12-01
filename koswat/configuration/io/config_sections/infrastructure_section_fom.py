"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
    active: bool
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
            active=SectionConfigHelper.get_bool(input_config["actief"]),
            surtax_factor_roads=SurtaxFactorEnum[
                input_config["opslagfactor_wegen"].upper()
            ],
            infrastructure_costs_0dh=InfraCostsEnum[
                input_config["infrakosten_0dh"].upper()
            ],
            buffer_waterside=SectionConfigHelper.get_float(
                input_config["buffer_buitendijks"]
            ),
            roads_class2_width=SectionConfigHelper.get_float(
                input_config["wegen_klasse2_breedte"]
            ),
            roads_class24_width=SectionConfigHelper.get_float(
                input_config["wegen_klasse24_breedte"]
            ),
            roads_class47_width=SectionConfigHelper.get_float(
                input_config["wegen_klasse47_breedte"]
            ),
            roads_class7_width=SectionConfigHelper.get_float(
                input_config["wegen_klasse7_breedte"]
            ),
            roads_unknown_width=SectionConfigHelper.get_float(
                input_config["wegen_onbekend_breedte"]
            ),
        )
