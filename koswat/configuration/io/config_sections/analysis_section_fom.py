from dataclasses import dataclass
from pathlib import Path
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class AnalysisSectionFom(KoswatJsonFomProtocol):
    dike_selection_txt_file: Path
    dike_section_location_shp_file: Path
    input_profiles_json_dir: Path
    scenarios_ini_dir: Path
    costs_ini_file: Path
    analysis_output_dir: Path
    include_taxes: bool

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "AnalysisSectionFom":
        return cls(
            dike_selection_txt_file=Path(input_config["dijksecties_selectie"]),
            dike_section_location_shp_file=Path(input_config["dijksectie_ligging"]),
            input_profiles_json_dir=Path(input_config["dijksectie_invoer"]),
            scenarios_ini_dir=Path(input_config["scenario_invoer"]),
            costs_ini_file=Path(input_config["eenheidsprijzen"]),
            analysis_output_dir=Path(input_config["uitvoerfolder"]),
            include_taxes=SectionConfigHelper.get_bool(input_config["btw"]),
        )
