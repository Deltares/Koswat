from typing import List

import pytest
from shapely.geometry import Point

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.layers.koswat_layers_wrapper import KoswatLayersWrapper


def almost_equal(left_value: float, right_value: float) -> bool:
    return abs(left_value - right_value) <= 0.01


def _compare_points(new_points: List[Point], expected_points: List[Point]) -> List[str]:
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
    new_profile: KoswatInputProfileProtocol,
    expected_profile: KoswatInputProfileProtocol,
) -> List[str]:
    _new_data_dict = new_profile.__dict__
    _expected_data_dict = expected_profile.__dict__
    assert len(_new_data_dict) >= 10
    assert len(_new_data_dict) == len(_expected_data_dict)
    return [
        f"Values differ for {key}, expected {value}, got: {_new_data_dict[key]}"
        for key, value in _expected_data_dict.items()
        if not almost_equal(_new_data_dict[key], value)
    ]


def _compare_koswat_layers(
    new_layers: KoswatLayersWrapper, expected_layers: KoswatLayersWrapper
) -> List[str]:
    _tolerance = 0.001
    if not new_layers.base_layer.geometry.almost_equals(
        expected_layers.base_layer.geometry, _tolerance
    ):
        return [f"Geometries differ for base_layer."]
    _layers_errors = []
    for _idx, _c_layer in enumerate(expected_layers.coating_layers):
        _new_layer = new_layers.coating_layers[_idx]
        if not _new_layer.geometry.almost_equals(_c_layer.geometry, _tolerance):
            _layers_errors.append(
                f"Geometries differ for layer {_c_layer.material.name}"
            )

    return _layers_errors


def compare_koswat_profiles(
    new_profile: KoswatProfileProtocol, expected_profile: KoswatProfileProtocol
):
    _found_errors = _compare_koswat_input_profile(
        new_profile.input_data, expected_profile.input_data
    )
    _found_errors.extend(
        _compare_koswat_layers(
            new_profile.layers_wrapper, expected_profile.layers_wrapper
        )
    )
    _found_errors.extend(_compare_points(new_profile.points, expected_profile.points))
    if _found_errors:
        _mssg = "\n".join(_found_errors)
        pytest.fail(_mssg)
