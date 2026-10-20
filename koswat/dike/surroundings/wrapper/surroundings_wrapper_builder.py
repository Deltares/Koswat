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
from koswat.dike.surroundings.point.point_surroundings_list_builder import (
    PointSurroundingsListBuilder,
)
from koswat.dike.surroundings.road_classes import RoadClassProtocol
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
    obstacles: KoswatSurroundingsCsvFom
    infrastructures: dict[RoadClassProtocol, KoswatSurroundingsCsvFom]

    def build(self) -> SurroundingsWrapper:
        return SurroundingsWrapper(
            dike_section=self.location_shp_fom.dike_section,
            traject=self.location_shp_fom.dike_traject,
            subtraject=self.location_shp_fom.dike_subtraject,
            obstacle_surroundings_wrapper=self._get_obstacle_surroundings_wrapper(),
            infrastructure_surroundings_wrapper=self._get_infrastructure_surroundings_wrapper(),
            max_polderside_extension=self.surroundings_section_fom.max_polderside_extension,
            max_waterside_extension=self.surroundings_section_fom.max_waterside_extension,
        )

    def _get_obstacle_surroundings_wrapper(self) -> ObstacleSurroundingsWrapper:
        _obs_wrapper = ObstacleSurroundingsWrapper(
            reinforcement_min_separation=self.surroundings_section_fom.construction_distance,
            reinforcement_min_buffer=self.surroundings_section_fom.construction_buffer,
        )

        _obs_wrapper.obstacles.points = PointSurroundingsListBuilder(
            koswat_shp_fom=self.location_shp_fom,
            koswat_csv_fom=self.obstacles,
        ).build()

        # At least 1 obstacle type should be present to determine the location coordinates.
        if not any(_obs_wrapper.obstacles.points):
            raise ValueError(
                "At least 1 obstacle type should be present to determine the location coordinates."
            )

        return _obs_wrapper

    def _get_infrastructure_surroundings_wrapper(
        self,
    ) -> InfrastructureSurroundingsWrapper:
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=self.infrastructure_section_fom.active,
            surtax_cost_factor=self.infrastructure_section_fom.surtax_factor_roads,
            non_rising_dike_costs_factor=self.infrastructure_section_fom.infrastructure_costs_0dh,
            buffer_crest_waterside=self.infrastructure_section_fom.buffer_crest_waterside,
            infrastructures_collection={},
        )

        if self.infrastructure_section_fom.active:
            _infra_wrapper.infrastructures_collection = {
                _road_class.class_name: SurroundingsInfrastructure(
                    infrastructure_type=_road_class,
                    points=PointSurroundingsListBuilder(
                        koswat_shp_fom=self.location_shp_fom,
                        koswat_csv_fom=_points,
                    ).build(),
                )
                for _road_class, _points in self.infrastructures.items()
            }

        return _infra_wrapper
