import pytest
from shapely.geometry import Point, Polygon

from koswat.dike_reinforcements.reinforcement_layers.reinforcement_layers_wrapper import (
    ReinforcementLayersWrapper,
)
from koswat.dike_reinforcements.reinforcement_profile.reinforcement_profile_protocol import (
    ReinforcementProfileProtocol,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


def almost_equal(left_value: float, right_value: float) -> bool:
    return abs(left_value - right_value) <= 0.01


def _compare_points(new_points: list[Point], expected_points: list[Point]) -> list[str]:
    _new_points = [(p.x, p.y) for p in new_points]
    _expected_points = [(p.x, p.y) for p in expected_points]
    _wrong_points = []
    for idx, (x, y) in enumerate(_expected_points):
        _new_x, _new_y = _new_points[idx]
        if not (almost_equal(_new_x, x) and almost_equal(_new_y, y)):
            _wrong_points.append(
                f"Point {idx + 1} differs expected: ({x},{y}), got: ({_new_x},{_new_y})"
            )
    return _wrong_points


def _compare_koswat_input_profile(
    reinforced_input_profile: KoswatInputProfileProtocol,
    expected_input_profile: KoswatInputProfileProtocol,
) -> list[str]:
    _new_data_dict = reinforced_input_profile.__dict__
    _exp_data_dict = expected_input_profile.__dict__
    assert len(_new_data_dict) >= 10
    assert len(_new_data_dict) == len(_exp_data_dict)
    return [
        f"Values differ for {key}, expected {value}, got: {_new_data_dict[key]}"
        for key, value in _exp_data_dict.items()
        if key != "dike_section" and not almost_equal(_new_data_dict[key], value)
    ]


def _compare_koswat_layers(
    new_layers: ReinforcementLayersWrapper, expected_layers: ReinforcementLayersWrapper
) -> list[str]:
    _tolerance = 0.001
    if not new_layers.base_layer.outer_geometry.almost_equals(
        expected_layers.base_layer.outer_geometry, _tolerance
    ):
        return [f"Geometries differ for base_layer."]
    _layers_errors = []
    for _idx, _c_layer in enumerate(expected_layers.coating_layers):
        _new_layer = new_layers.coating_layers[_idx]
        if not _new_layer.outer_geometry.almost_equals(
            Polygon(_c_layer.outer_geometry), _tolerance
        ):
            _layers_errors.append(
                "Geometries differ for layer {}".format(_c_layer.material_type.name)
            )

    return _layers_errors


def validated_reinforced_profile(
    reinforced_profile: ReinforcementProfileProtocol,
    expected_profile: ReinforcementProfileProtocol,
):
    _found_errors = _compare_koswat_input_profile(
        reinforced_profile.input_data, expected_profile.input_data
    )
    _found_errors.extend(
        _compare_points(reinforced_profile.points, expected_profile.points)
    )
    _found_errors.extend(
        _compare_koswat_layers(
            reinforced_profile.layers_wrapper, expected_profile.layers_wrapper
        )
    )
    if _found_errors:
        _mssg = "\n".join(_found_errors)
        pytest.fail(_mssg)
