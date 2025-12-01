"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations

from typing import Any, Optional

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


class SectionScenarioFom(KoswatJsonFomProtocol):
    scenario_name: str
    d_h: float
    d_s: float
    d_p: float
    # If the following ones are not provided we should use the ones from the original profile
    waterside_slope: Optional[float]
    crest_width: Optional[float]

    @classmethod
    def from_config(
        cls, input_config: dict[str, Any], scenario_name: str
    ) -> SectionScenarioFom:
        _section = cls()
        # Retrieves the values as written (and expected) in the config file.
        _section.scenario_name = scenario_name
        _section.d_h = SectionConfigHelper.get_float(input_config["dh"])
        _section.d_s = SectionConfigHelper.get_float(input_config["ds"])
        _section.d_p = SectionConfigHelper.get_float(input_config["dp"])
        _section.waterside_slope = SectionConfigHelper.get_float(
            input_config.get("buitentalud", None)
        )
        _section.crest_width = SectionConfigHelper.get_float(
            input_config.get("kruinbreedte", None)
        )
        return _section


class KoswatSectionScenariosJsonFom(KoswatJsonFomProtocol):
    section_scenarios: list[SectionScenarioFom]
    scenario_dike_section: str

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> KoswatSectionScenariosJsonFom:
        _section_scenario_fom = cls()
        _section_scenario_fom.section_scenarios = []
        _section_scenario_fom.scenario_dike_section = ""
        _section_scenario_fom.section_scenarios = [
            SectionScenarioFom.from_config(
                input_config=input_config[_scenario_name], scenario_name=_scenario_name
            )
            for _scenario_name in input_config.keys()
        ]
        return _section_scenario_fom
