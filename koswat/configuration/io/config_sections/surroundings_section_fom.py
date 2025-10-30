from dataclasses import dataclass
from pathlib import Path
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


@dataclass
class SurroundingsSectionFom(KoswatIniFomProtocol):
    surroundings_database_dir: Path
    construction_distance: float
    construction_buffer: float
    waterside: bool
    buildings: bool
    railways: bool
    waters: bool

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurroundingsSectionFom":
        _section = cls(
            surroundings_database_dir=Path(input_config["omgevingsdatabases"]),
            construction_distance=SectionConfigHelper.get_float(
                input_config["constructieafstand"]
            ),
            construction_buffer=SectionConfigHelper.get_float(
                input_config["constructieovergang"]
            ),
            waterside=SectionConfigHelper.get_bool(input_config["buitendijks"]),
            buildings=SectionConfigHelper.get_bool(input_config["bebouwing"]),
            railways=SectionConfigHelper.get_bool("spoorwegen"),
            waters=SectionConfigHelper.get_bool("water"),
        )
        return _section
