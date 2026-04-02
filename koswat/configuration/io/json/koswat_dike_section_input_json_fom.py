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

from dataclasses import dataclass, field

from koswat.configuration.io.config_sections import (
    CofferdamReinforcementSectionFom,
    DikeProfileSectionFom,
    PipingWallReinforcementSectionFom,
    SoilReinforcementSectionFom,
    StabilityWallCrestReinforcementSectionFom,
    StabilityWallToeReinforcementSectionFom,
    VPSReinforcementSectionFom,
    WatersideSoilReinforcementSectionFom,
)
from koswat.configuration.io.config_sections.surroundings_section_fom import (
    SurroundingsSectionFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@dataclass
class KoswatDikeSectionInputJsonFom(FileObjectModelProtocol):
    dike_section: str = ""
    input_profile: DikeProfileSectionFom = field(default_factory=DikeProfileSectionFom)
    soil_measure: SoilReinforcementSectionFom = field(
        default_factory=SoilReinforcementSectionFom
    )
    waterside_soil_measure: WatersideSoilReinforcementSectionFom = field(
        default_factory=WatersideSoilReinforcementSectionFom
    )
    vps: VPSReinforcementSectionFom = field(default_factory=VPSReinforcementSectionFom)
    piping_wall: PipingWallReinforcementSectionFom = field(
        default_factory=PipingWallReinforcementSectionFom
    )
    stability_wall_toe: StabilityWallToeReinforcementSectionFom = field(
        default_factory=StabilityWallToeReinforcementSectionFom
    )
    stability_wall_crest: StabilityWallCrestReinforcementSectionFom = field(
        default_factory=StabilityWallCrestReinforcementSectionFom
    )
    cofferdam: CofferdamReinforcementSectionFom = field(
        default_factory=CofferdamReinforcementSectionFom
    )
    surroundings: SurroundingsSectionFom = field(
        default_factory=lambda: SurroundingsSectionFom.from_config({}, False)
    )

    def is_valid(self) -> bool:
        return self.dike_section != ""
