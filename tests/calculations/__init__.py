from typing import List, Type

import pytest
from shapely.geometry import Point, Polygon

from koswat.calculations import (
    ReinforcementLayersWrapper,
    ReinforcementProfileBuilderFactory,
    ReinforcementProfileProtocol,
)
from koswat.calculations.outside_slope_reinforcement import (
    OutsideSlopeReinforcementLayersWrapperBuilder,
    OutsideSlopeReinforcementProfile,
)
from koswat.calculations.standard_reinforcement import (
    StandardReinforcementLayersWrapperBuilder,
    StandardReinforcementProfile,
)
from koswat.dike.characteristic_points.characteristic_points_builder import (
    CharacteristicPointsBuilder,
)
from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol
from koswat.dike.layers.layers_wrapper import (
    KoswatLayersWrapperBuilder,
    KoswatLayersWrapperBuilderProtocol,
    KoswatLayersWrapperProtocol,
)


def almost_equal(left_value: float, right_value: float) -> bool:
    return abs(left_value - right_value) <= 0.01


def get_reinforced_profile(
    type_reinforcement: Type[ReinforcementProfileProtocol], reinforced_data: dict
) -> ReinforcementProfileProtocol:
    _reinforcement = type_reinforcement()
    # Input profile data.
    _reinforcement.input_data = (
        ReinforcementProfileBuilderFactory.get_reinforcement_input_profile(
            type_reinforcement
        ).from_dict(reinforced_data["input_profile_data"])
    )
    # Char points
    _char_points_builder = CharacteristicPointsBuilder()
    _char_points_builder.input_profile = _reinforcement.input_data
    _char_points_builder.p4_x_coordinate = reinforced_data["p4_x_coordinate"]
    _reinforcement.characteristic_points = _char_points_builder.build()

    # layers
    def _get_layers(
        builder: KoswatLayersWrapperBuilderProtocol,
        layers_data: dict,
        char_points,
    ) -> KoswatLayersWrapperProtocol:
        builder.layers_data = layers_data
        builder.profile_points = char_points
        return builder.build()

    _layers_wrapper_builder: KoswatLayersWrapperBuilderProtocol = None
    if isinstance(_reinforcement, StandardReinforcementProfile):
        _layers_wrapper_builder = StandardReinforcementLayersWrapperBuilder()
    elif isinstance(_reinforcement, OutsideSlopeReinforcementProfile):
        _layers_wrapper_builder = OutsideSlopeReinforcementLayersWrapperBuilder()

    _initial_layers_wrapper = _get_layers(
        KoswatLayersWrapperBuilder(),
        reinforced_data["layers_data"],
        _reinforcement.characteristic_points.points,
    )
    _reinforcement.layers_wrapper = _get_layers(
        _layers_wrapper_builder,
        _initial_layers_wrapper.as_data_dict(),
        _reinforcement.characteristic_points.points,
    )

    return _reinforcement


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
    reinforced_input_profile: KoswatInputProfileProtocol,
    expected_input_profile: KoswatInputProfileProtocol,
) -> List[str]:
    _new_data_dict = reinforced_input_profile.__dict__
    _exp_data_dict = expected_input_profile.__dict__
    assert len(_new_data_dict) >= 10
    assert len(_new_data_dict) == len(_exp_data_dict)
    return [
        f"Values differ for {key}, expected {value}, got: {_new_data_dict[key]}"
        for key, value in _exp_data_dict.items()
        if not almost_equal(_new_data_dict[key], value)
    ]


def _compare_koswat_layers(
    new_layers: ReinforcementLayersWrapper, expected_layers: ReinforcementLayersWrapper
) -> List[str]:
    _tolerance = 0.001
    if not new_layers.base_layer.geometry.almost_equals(
        expected_layers.base_layer.geometry, _tolerance
    ):
        return [f"Geometries differ for base_layer."]
    _layers_errors = []
    for _idx, _c_layer in enumerate(expected_layers.coating_layers):
        _new_layer = new_layers.coating_layers[_idx]
        if not _new_layer.geometry.almost_equals(
            Polygon(_c_layer.geometry), _tolerance
        ):
            _layers_errors.append(
                "Geometries differ for layer {}".format(_c_layer.material.name)
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
