from dataclasses import dataclass, field
from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


@dataclass
class SurroundingsSectionFom(KoswatJsonFomProtocol):
    construction_distance: float
    construction_buffer: float
    waterside: bool
    buildings: bool
    railways: bool
    waters: bool
    custom_obstacles: list[str] = field(default_factory=list)

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurroundingsSectionFom":
        _types = [
            _type.lower().strip() for _type in input_config.get("omgevingtypes", [])
        ]

        def pop_surrounding_type(type_name: str) -> bool:
            if type_name in _types:
                _types.remove(type_name)
                return True
            return False

        _section = cls(
            construction_distance=SectionConfigHelper.get_float(
                input_config["constructieafstand"]
            ),
            construction_buffer=SectionConfigHelper.get_float(
                input_config["constructieovergang"]
            ),
            waterside=pop_surrounding_type("buitendijks"),
            buildings=pop_surrounding_type("bebouwing"),
            railways=pop_surrounding_type("spoorwegen"),
            waters=pop_surrounding_type("water"),
            custom_obstacles=[name for name in _types],
        )
        return _section
