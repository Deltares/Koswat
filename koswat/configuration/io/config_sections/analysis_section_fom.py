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
from pathlib import Path, PurePosixPath, PureWindowsPath
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
        def resolve_path(input_path: str) -> Path:
            if PureWindowsPath(input_path).is_absolute() or PurePosixPath(input_path).is_absolute():
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
