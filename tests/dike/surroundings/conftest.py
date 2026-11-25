from collections.abc import Callable, Iterator

import pytest
from shapely import Point

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.configuration.settings.costs.infastructure_costs_settings import (
    InfrastructureCostsSettings,
)
from koswat.configuration.settings.koswat_general_settings import (
    InfraCostsEnum,
    SurtaxFactorEnum,
)
from koswat.dike.surroundings.point import PointInfrastructureSurroundings


@pytest.fixture(name="distances_to_surrounding_point_builder")
def get_distances_as_surrounding_point_builder() -> (
    Iterator[Callable[[Point, list[float]], PointInfrastructureSurroundings]]
):
    """
    Gets a builder to generate `PointInfrastructureSurroundings` with a location and a valid
    `surroundings_matrix` which could relate to an `ObstacleSurrounding`.

    Yields:
        Iterator[ Callable[[Point, list[float]], PointInfrastructureSurroundings] ]: Yields a builder of `PointInfrastructureSurroundings`.
    """

    def build_point_surroundings(
        location: Point, distances_list: list[float]
    ) -> PointInfrastructureSurroundings:
        return PointInfrastructureSurroundings(
            location=location, polderside_surroundings={_d: 1 for _d in distances_list}
        )

    yield build_point_surroundings


@pytest.fixture(name="infrastructure_section_fom_fixture")
def _get_infrastructure_section_fom() -> Iterator[InfrastructureSectionFom]:
    yield InfrastructureSectionFom(
        active=True,
        surtax_factor_roads=SurtaxFactorEnum.NORMAAL,
        infrastructure_costs_0dh=InfraCostsEnum.GEEN,
        buffer_crest_waterside=0.42,
        roads_class2_width=2.4,
        roads_class24_width=4.2,
        roads_class47_width=24,
        roads_class7_width=42,
        roads_unknown_width=0.67,
    )


@pytest.fixture(name="infrastructure_costs_settings_fixture")
def _get_infrastructure_costs_settings() -> Iterator[InfrastructureCostsSettings]:
    yield InfrastructureCostsSettings(
        removing_roads_klasse2=1.0,
        removing_roads_klasse24=2.0,
        removing_roads_klasse47=3.0,
        removing_roads_klasse7=4.0,
        removing_roads_unknown=5.0,
        adding_roads_klasse2=2.0,
        adding_roads_klasse24=4.0,
        adding_roads_klasse47=5.0,
        adding_roads_klasse7=6.0,
        adding_roads_unknown=10.0,
    )
