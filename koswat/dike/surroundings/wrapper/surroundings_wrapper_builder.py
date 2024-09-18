from dataclasses import dataclass

from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.configuration.io.ini.koswat_general_ini_fom import (
    InfrastructureSectionFom,
    SurroundingsSectionFom,
)
from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.protocols.builder_protocol import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike.surroundings.point.point_surroundings_list_polderside_builder import (
    PointSurroundingsListPoldersideBuilder,
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

    def _get_polderside_surroundings_from_fom(
        self, csv_fom_name: str
    ) -> list[PointSurroundings]:
        if csv_fom_name not in self.surroundings_csv_fom_collection:
            return []
        return PointSurroundingsListPoldersideBuilder(
            koswat_shp_fom=self.location_shp_fom,
            koswat_csv_fom=self.surroundings_csv_fom_collection[csv_fom_name],
        ).build()

    def _get_obstacle_surroundings_wrapper(self) -> ObstacleSurroundingsWrapper:
        _obs_wrapper = ObstacleSurroundingsWrapper(
            reinforcement_min_separation=self.surroundings_section_fom.constructieafstand,
            reinforcement_min_buffer=self.surroundings_section_fom.constructieovergang,
            apply_waterside=self.surroundings_section_fom.buitendijks,
            apply_buildings=self.surroundings_section_fom.bebouwing,
            apply_railways=self.surroundings_section_fom.spoorwegen,
            apply_waters=self.surroundings_section_fom.water,
        )
        _obs_wrapper.buildings_polderside.points = (
            self._get_polderside_surroundings_from_fom("buildings_polderside")
        )
        _obs_wrapper.railways_polderside.points = (
            self._get_polderside_surroundings_from_fom("railways_polderside")
        )
        _obs_wrapper.waters_polderside.points = (
            self._get_polderside_surroundings_from_fom("waters_polderside")
        )

        return _obs_wrapper

    def _get_infrastructure_surroundings_wrapper(
        self,
    ) -> InfrastructureSurroundingsWrapper:
        _infra_wrapper = InfrastructureSurroundingsWrapper(
            infrastructures_considered=self.infrastructure_section_fom.infrastructuur,
            surtax_cost_factor=self.infrastructure_section_fom.opslagfactor_wegen,
            non_rising_dike_costs_factor=self.infrastructure_section_fom.infrakosten_0dh,
        )

        # Roads class 2
        _infra_wrapper.roads_class_2_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_2_polderside")
        )
        _infra_wrapper.roads_class_2_polderside.infrastructure_width = (
            self.infrastructure_section_fom.wegen_klasse2_breedte
        )

        # Roads class 7
        _infra_wrapper.roads_class_7_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_7_polderside")
        )
        _infra_wrapper.roads_class_2_polderside.infrastructure_width = (
            self.infrastructure_section_fom.wegen_klasse7_breedte
        )

        # Roads class 24
        _infra_wrapper.roads_class_24_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_24_polderside")
        )
        _infra_wrapper.roads_class_2_polderside.infrastructure_width = (
            self.infrastructure_section_fom.wegen_klasse24_breedte
        )

        # Rodas class 47
        _infra_wrapper.roads_class_47_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_47_polderside")
        )
        _infra_wrapper.roads_class_2_polderside.infrastructure_width = (
            self.infrastructure_section_fom.wegen_klasse47_breedte
        )

        # Roads class unknown
        _infra_wrapper.roads_class_unknown_polderside.points = (
            self._get_polderside_surroundings_from_fom("roads_class_unknown_polderside")
        )
        _infra_wrapper.roads_class_2_polderside.infrastructure_width = (
            self.infrastructure_section_fom.wegen_onbekend_breedte
        )

        return _infra_wrapper
