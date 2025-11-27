from dataclasses import dataclass
import os
from pathlib import Path, PosixPath, WindowsPath
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
        # We build the paths relative to the parent path of the main config file.
        # UNLESS they are already absolute paths.

        def is_absolute_path(input_path: str) -> bool:
            if os.name == "nt":
                # On Windows we need to check for both PosixPath and WindowsPath
                 return WindowsPath(input_path).is_absolute()
            return PosixPath(input_path).is_absolute() 

        def resolve_path(input_path: str) -> Path:
            if is_absolute_path(input_path):
                # Using a windows path in a unix system will return false here.
                return Path(input_path)
            return parent_path.joinpath(input_path)
        
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
