from dataclasses import dataclass

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
    Builder class for a road class instance.
    """

    infrastructure_section: InfrastructureSectionFom
    infrastructure_costs: InfrastructureCostsSettings

    @property
    def road_class_types(self) -> list[type[RoadClassProtocol]]:
        return [RoadClass2, RoadClass7, RoadClass24, RoadClass47, RoadClassUnknown]

    def _set_road_class_properties(self, road_class: RoadClassProtocol) -> None:
        if isinstance(road_class, RoadClass2):
            road_class.width = self.infrastructure_section.roads_class2_width
            road_class.adding_costs = self.infrastructure_costs.adding_roads_klasse2
            road_class.removing_costs = self.infrastructure_costs.removing_roads_klasse2
        elif isinstance(road_class, RoadClass7):
            road_class.width = self.infrastructure_section.roads_class7_width
            road_class.adding_costs = self.infrastructure_costs.adding_roads_klasse7
            road_class.removing_costs = self.infrastructure_costs.removing_roads_klasse7
        elif isinstance(road_class, RoadClass24):
            road_class.width = self.infrastructure_section.roads_class24_width
            road_class.adding_costs = self.infrastructure_costs.adding_roads_klasse24
            road_class.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse24
            )
        elif isinstance(road_class, RoadClass47):
            road_class.width = self.infrastructure_section.roads_class47_width
            road_class.adding_costs = self.infrastructure_costs.adding_roads_klasse47
            road_class.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse47
            )
        else:
            road_class.width = self.infrastructure_section.roads_unknown_width
            road_class.adding_costs = self.infrastructure_costs.adding_roads_unknown
            road_class.removing_costs = self.infrastructure_costs.removing_roads_unknown

    def _get_road_class(self, source_name: str) -> RoadClassProtocol | None:
        _road_class_type = next(
            (
                x
                for x in self.road_class_types
                if x.get_polderside_import_name() == source_name
                or x.get_waterside_import_name() == source_name
            ),
            None,
        )
        if not _road_class_type:
            return None

        _road_class = _road_class_type()
        _road_class.is_polderside = (
            source_name == _road_class.get_polderside_import_name()
        )
        self._set_road_class_properties(_road_class)
        return _road_class

    def build(self, source_name: str) -> RoadClassProtocol | None:
        """
        Build a road class instance based on the given name.

        Args:
            source_name (str): The name of the road class to build.

        Returns:
            RoadClassProtocol | None: An instance of the corresponding road class if found, otherwise None.
        """
        return self._get_road_class(source_name)
