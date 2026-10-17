from dataclasses import dataclass, field

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)

from .road_class_2 import RoadClass2
from .road_class_7 import RoadClass7
from .road_class_24 import RoadClass24
from .road_class_47 import RoadClass47
from .road_class_protocol import RoadClassProtocol
from .road_class_unknown import RoadClassUnknown


@dataclass
class RoadClassBuilder:
    """
    Builder class for a road type class.
    """

    infrastructure_section: InfrastructureSectionFom
    infrastructure_costs: InfrastructureCostsSettings
    _type_collection: dict[type[RoadClassProtocol], tuple[str, str]] = field(
        default_factory=dict
    )

    @property
    def road_class_types(self) -> list[type[RoadClassProtocol]]:
        return [RoadClass2, RoadClass7, RoadClass24, RoadClass47, RoadClassUnknown]

    def __post_init__(self):
        self._type_collection = {
            x: (x.polderside_name, x.waterside_name) for x in self.road_class_types
        }

    def _get_road_class_width(self, road_class: type[RoadClassProtocol]) -> float:
        if road_class == RoadClass2:
            return self.infrastructure_section.roads_class2_width
        if road_class == RoadClass7:
            return self.infrastructure_section.roads_class7_width
        if road_class == RoadClass24:
            return self.infrastructure_section.roads_class24_width
        if road_class == RoadClass47:
            return self.infrastructure_section.roads_class47_width
        return self.infrastructure_section.roads_unknown_width

    def _get_road_class_costs(
        self, road_class: type[RoadClassProtocol]
    ) -> tuple[float, float]:
        if road_class == RoadClass2:
            return (
                self.infrastructure_costs.adding_roads_klasse2,
                self.infrastructure_costs.removing_roads_klasse2,
            )
        if road_class == RoadClass7:
            return (
                self.infrastructure_costs.adding_roads_klasse7,
                self.infrastructure_costs.removing_roads_klasse7,
            )
        if road_class == RoadClass24:
            return (
                self.infrastructure_costs.adding_roads_klasse24,
                self.infrastructure_costs.removing_roads_klasse24,
            )
        if road_class == RoadClass47:
            return (
                self.infrastructure_costs.adding_roads_klasse47,
                self.infrastructure_costs.removing_roads_klasse47,
            )
        return (
            self.infrastructure_costs.adding_roads_unknown,
            self.infrastructure_costs.removing_roads_unknown,
        )

    def build(self, name: str) -> RoadClassProtocol | None:
        """
        Build a road class instance based on the given name.

        Args:
            name (str): The name of the road class to build.

        Returns:
            RoadClassProtocol | None: An instance of the corresponding road class if found, otherwise None.
        """

        def get_road_class_type() -> tuple[type[RoadClassProtocol] | None, bool]:
            return next(
                (
                    (x, True) if x.polderside_name == name else (x, False)
                    for x in self.road_class_types
                    if x.polderside_name == name or x.waterside_name == name
                ),
                (None, False),
            )

        _road_class_type, _is_polderside = get_road_class_type()
        if not _road_class_type:
            return None

        _road_class = _road_class_type()
        _road_class.is_polderside = _is_polderside
        _road_class.width = self._get_road_class_width(_road_class_type)
        _road_class.adding_cost, _road_class.removing_cost = self._get_road_class_costs(
            _road_class_type
        )
        return _road_class
