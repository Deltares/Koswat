from dataclasses import dataclass

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)

from .infrastructure_type_protocol import InfrastructureTypeProtocol
from .road_class_base import RoadClassBase
from .road_classes import (
    RoadClass2,
    RoadClass7,
    RoadClass24,
    RoadClass47,
    RoadClassUnknown,
)


@dataclass
class InfrastructureTypeBuilder:
    """
    Builder class for an infrastructure type instance.
    """

    infrastructure_section: InfrastructureSectionFom
    infrastructure_costs: InfrastructureCostsSettings

    @property
    def infrastructure_types(self) -> list[type[RoadClassBase]]:
        return [RoadClass2, RoadClass7, RoadClass24, RoadClass47, RoadClassUnknown]

    def _set_infrastructure_type_properties(
        self, infrastructure_type: InfrastructureTypeProtocol
    ) -> None:
        if isinstance(infrastructure_type, RoadClass2):
            infrastructure_type.width = self.infrastructure_section.roads_class2_width
            infrastructure_type.adding_costs = (
                self.infrastructure_costs.adding_roads_klasse2
            )
            infrastructure_type.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse2
            )
        elif isinstance(infrastructure_type, RoadClass7):
            infrastructure_type.width = self.infrastructure_section.roads_class7_width
            infrastructure_type.adding_costs = (
                self.infrastructure_costs.adding_roads_klasse7
            )
            infrastructure_type.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse7
            )
        elif isinstance(infrastructure_type, RoadClass24):
            infrastructure_type.width = self.infrastructure_section.roads_class24_width
            infrastructure_type.adding_costs = (
                self.infrastructure_costs.adding_roads_klasse24
            )
            infrastructure_type.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse24
            )
        elif isinstance(infrastructure_type, RoadClass47):
            infrastructure_type.width = self.infrastructure_section.roads_class47_width
            infrastructure_type.adding_costs = (
                self.infrastructure_costs.adding_roads_klasse47
            )
            infrastructure_type.removing_costs = (
                self.infrastructure_costs.removing_roads_klasse47
            )
        else:
            infrastructure_type.width = self.infrastructure_section.roads_unknown_width
            infrastructure_type.adding_costs = (
                self.infrastructure_costs.adding_roads_unknown
            )
            infrastructure_type.removing_costs = (
                self.infrastructure_costs.removing_roads_unknown
            )

    def _get_infrastructure_type_instance(
        self, source_name: str
    ) -> InfrastructureTypeProtocol | None:
        _infrastructure_type = next(
            (
                x
                for x in self.infrastructure_types
                if x.get_polderside_import_name() == source_name
                or x.get_waterside_import_name() == source_name
            ),
            None,
        )
        if not _infrastructure_type:
            return None

        _infrastructure_type_instance = _infrastructure_type()
        _infrastructure_type_instance.is_polderside = (
            source_name == _infrastructure_type_instance.get_polderside_import_name()
        )
        self._set_infrastructure_type_properties(_infrastructure_type_instance)
        return _infrastructure_type_instance

    def build(self, source_name: str) -> InfrastructureTypeProtocol | None:
        """
        Build an infrastructure type instance based on the given name.

        Args:
            source_name (str): The name of the road class to build.

        Returns:
            InfrastructureTypeProtocol | None: An instance of the corresponding infrastructure type if found, otherwise None.
        """
        return self._get_infrastructure_type_instance(source_name)
