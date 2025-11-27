from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class AnalysisSectionFom(KoswatJsonFomProtocol):
    dike_section_location_shp_file: Path
    dike_selection_txt_file: Path
    input_profiles_json_dir: Path
    scenarios_json_dir: Path
    costs_json_file: Path
    surroundings_database_dir: Path
    analysis_output_dir: Path
    include_taxes: bool

    @classmethod
    def from_config(cls, input_config: dict[str, Any], parent_path: Path) -> "AnalysisSectionFom":
        
        def resolve_path(input_path: str) -> Path:
            if not PurePath(input_path).is_absolute() and parent_path is not None and parent_path.exists():
                return Path(parent_path.joinpath(input_path))
            return Path(input_path)
        
        return cls(
            dike_section_location_shp_file=resolve_path(input_config["dijksectie_ligging"]),
            dike_selection_txt_file=resolve_path(input_config["dijksecties_selectie"]),
            input_profiles_json_dir=resolve_path(input_config["dijksectie_invoer"]),
            scenarios_json_dir=resolve_path(input_config["scenario_invoer"]),
            costs_json_file=resolve_path(input_config["eenheidsprijzen"]),
            surroundings_database_dir=resolve_path(input_config["omgevingsdatabases"]),
            analysis_output_dir=resolve_path(input_config["uitvoerfolder"]),
            include_taxes=SectionConfigHelper.get_bool(input_config["btw"]),
        )
