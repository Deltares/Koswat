from dataclasses import dataclass

from koswat.configuration.io.config_sections import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_list_polderside_builder import (
    PointSurroundingsListBuilder,
)
from koswat.dike.surroundings.surroundings_enum import SurroundingsEnum
from koswat.dike.surroundings.surroundings_infrastructure import (
    SurroundingsInfrastructure,
)
from koswat.dike.surroundings.wrapper.infrastructure_surroundings_wrapper import (
    InfrastructureSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.obstacle_surroundings_wrapper import (
    ObstacleSurroundingsWrapper,
)
from koswat.dike.surroundings.wrapper.surroundings_wrapper import SurroundingsWrapper


@dataclass
class SurroundingsWrapperBuilder(BuilderProtocol):
    surroundings_section_fom: SurroundingsSectionFom
    infrastructure_section_fom: InfrastructureSectionFom
    location_shp_fom: KoswatDikeLocationsShpFom
    surroundings_csv_fom_collection: dict[str, KoswatSurroundingsCsvFom]

    def build(self) -> SurroundingsWrapper:
        return SurroundingsWrapper(
            dike_section=self.location_shp_fom.dike_section,
            traject=self.location_shp_fom.dike_traject,
            subtraject=self.location_shp_fom.dike_subtraject,
            obstacle_surroundings_wrapper=self._get_obstacle_surroundings_wrapper(),
            infrastructure_surroundings_wrapper=self._get_infrastructure_surroundings_wrapper(),
        )

    def _get_surroundings_from_fom(
        self, csv_fom_name: SurroundingsEnum
    ) -> list[PointSurroundings]:
        if csv_fom_name.name not in self.surroundings_csv_fom_collection:
            return []
        return PointSurroundingsListBuilder(
            koswat_shp_fom=self.location_shp_fom,
            koswat_csv_fom=self.surroundings_csv_fom_collection[csv_fom_name.name],
        ).build()

    def _get_obstacle_surroundings_wrapper(self) -> ObstacleSurroundingsWrapper:
        _obs_wrapper = ObstacleSurroundingsWrapper(
            reinforcement_min_separation=self.surroundings_section_fom.construction_distance,
            reinforcement_min_buffer=self.surroundings_section_fom.construction_buffer,
        )
        # Buildings polderside should always be present to determine the location coordinates.
        _obs_wrapper.buildings.points = self._get_surroundings_from_fom(
            SurroundingsEnum.BUILDINGS
        )
        if self.surroundings_section_fom.railways:
            _obs_wrapper.railways.points = self._get_surroundings_from_fom(
                SurroundingsEnum.RAILWAYS
            )
        if self.surroundings_section_fom.waters:
            _obs_wrapper.waters.points = self._get_surroundings_from_fom(
                SurroundingsEnum.WATERS
            )

        if any(self.surroundings_section_fom.custom_obstacles):
            _obs_wrapper.custom_obstacles.points = self._get_surroundings_from_fom(
                SurroundingsEnum.CUSTOM
            )

        return _obs_wrapper

    def _get_surroundings_infrastructure(
        self, surrounding_enum: SurroundingsEnum
    ) -> SurroundingsInfrastructure:
        _mapped_name = (
            surrounding_enum.name.lower()
            .replace("_polderside", "_width")
            .replace("class_unknown", "unknown")
            .replace("class_", "class")
        )
        return SurroundingsInfrastructure(
            infrastructure_name=_mapped_name,
            points=self._get_surroundings_from_fom(surrounding_enum),
            infrastructure_width=getattr(self.infrastructure_section_fom, _mapped_name),
        )

    def _get_infrastructure_surroundings_wrapper(
        self,
    ) -> InfrastructureSurroundingsWrapper:
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=self.infrastructure_section_fom.active,
            surtax_cost_factor=self.infrastructure_section_fom.surtax_factor_roads,
            non_rising_dike_costs_factor=self.infrastructure_section_fom.infrastructure_costs_0dh,
        )
        if self.infrastructure_section_fom.active:
            _infra_wrapper.roads_class_2_polderside = (
                self._get_surroundings_infrastructure(
                    SurroundingsEnum.ROADS_CLASS_2_POLDERSIDE
                )
            )
            _infra_wrapper.roads_class_7_polderside = (
                self._get_surroundings_infrastructure(
                    SurroundingsEnum.ROADS_CLASS_7_POLDERSIDE
                )
            )
            _infra_wrapper.roads_class_24_polderside = (
                self._get_surroundings_infrastructure(
                    SurroundingsEnum.ROADS_CLASS_24_POLDERSIDE
                )
            )
            _infra_wrapper.roads_class_47_polderside = (
                self._get_surroundings_infrastructure(
                    SurroundingsEnum.ROADS_CLASS_47_POLDERSIDE
                )
            )
            _infra_wrapper.roads_class_unknown_polderside = (
                self._get_surroundings_infrastructure(
                    SurroundingsEnum.ROADS_CLASS_UNKNOWN_POLDERSIDE
                )
            )
        return _infra_wrapper
