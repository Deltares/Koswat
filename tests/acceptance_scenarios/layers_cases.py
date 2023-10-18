import pytest
from koswat.dike.material.koswat_material_type import KoswatMaterialType
from tests.acceptance_scenarios.acceptance_test_scenario_dataclasses import (
    LayersTestCase,
)
from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class LayersCases(CasesProtocol):
    without_layers = LayersTestCase(
        case_name="without_layers",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[],
        ),
    )
    with_clay = LayersTestCase(
        case_name="with_clay",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.CLAY, depth=0.75),
            ],
        ),
    )
    with_clay_and_grass = LayersTestCase(
        case_name="with_clay_and_grass",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.GRASS, depth=0.5),
                dict(material=KoswatMaterialType.CLAY, depth=0.75),
            ],
        ),
    )
    with_acceptance_criteria = LayersTestCase(
        case_name="with_default_layers",
        layers_dict=dict(
            base_layer=dict(material=KoswatMaterialType.SAND),
            coating_layers=[
                dict(material=KoswatMaterialType.GRASS, depth=0.3),
                dict(material=KoswatMaterialType.CLAY, depth=0.5),
            ],
        ),
    )

    # Only cases that should be 'realistic'.
    cases = [
        pytest.param(with_clay_and_grass.layers_dict, id="With grass and clay layer"),
        pytest.param(
            with_acceptance_criteria.layers_dict, id="With acceptance criteria"
        ),
    ]
