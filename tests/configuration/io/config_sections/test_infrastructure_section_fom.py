import pytest

from koswat.configuration.io.config_sections.infrastructure_section_fom import (
    InfrastructureSectionFom,
)
from koswat.dike.surroundings.road_class import RoadClass


class TestInfrastructureSectionFom:
    @pytest.mark.parametrize(
        "road_class",
        [pytest.param(_rc, id=_rc.name) for _rc in RoadClass],
    )
    def test_when_get_roads_class_width_given_valid_road_class_then_width_returned(
        self, road_class: RoadClass
    ):
        # 1. Define test data
        _infrastructure_section_fom = InfrastructureSectionFom(
            active=True,
            surtax_factor_roads=None,
            infrastructure_costs_0dh=None,
            buffer_crest_waterside=None,
            roads_class2_width=2.0,
            roads_class24_width=24.0,
            roads_class47_width=47.0,
            roads_class7_width=7.0,
            roads_unknown_width=99.0,
        )

        # 2. Execute test
        _result = _infrastructure_section_fom.get_roads_class_width(road_class)

        # 3. Verify expectations
        assert isinstance(_result, float)

    def test_when_get_roads_class_width_given_invalid_road_class_then_raises_value_error(
        self,
    ):
        # 1. Define test data
        _infrastructure_section_fom = InfrastructureSectionFom(
            active=True,
            surtax_factor_roads=None,
            infrastructure_costs_0dh=None,
            buffer_crest_waterside=None,
            roads_class2_width=2.0,
            roads_class24_width=24.0,
            roads_class47_width=47.0,
            roads_class7_width=7.0,
            roads_unknown_width=99.0,
        )

        # 2. Execute test and verify expectations
        with pytest.raises(ValueError):
            _infrastructure_section_fom.get_roads_class_width("invalid")
