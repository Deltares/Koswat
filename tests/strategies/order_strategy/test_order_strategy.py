import pytest
from koswat.dike.surroundings.point.point_surroundings import PointSurroundings
from koswat.dike_reinforcements.reinforcement_profile.outside_slope.cofferdam_reinforcement_profile import (
    CofferdamReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.soil_reinforcement_profile import (
    SoilReinforcementProfile,
)
from koswat.dike_reinforcements.reinforcement_profile.standard.stability_wall_reinforcement_profile import (
    StabilityWallReinforcementProfile,
)
from koswat.strategies.order_strategy.order_strategy import OrderStrategy
from koswat.strategies.strategy_input import StrategyInput
from koswat.strategies.strategy_location_reinforcement import (
    StrategyLocationReinforcement,
)


class TestOrderStrategy:
    def test_initialize(self):
        # This test is just to ensure the design principle
        # of parameterless constructors is met.
        _strategy = OrderStrategy()
        assert isinstance(_strategy, OrderStrategy)
        assert len(_strategy._order_reinforcement) == 4

    @pytest.fixture
    def example_strategy_input(self) -> StrategyInput:
        # This is the data defined in the docs\reference\koswat_strategies.md
        # as examples. DON'T MODIFY IT!
        _matrix = {
            PointSurroundings(traject_order=0): [SoilReinforcementProfile],
            PointSurroundings(traject_order=1): [SoilReinforcementProfile],
            PointSurroundings(traject_order=2): [SoilReinforcementProfile],
            PointSurroundings(traject_order=3): [StabilityWallReinforcementProfile],
            PointSurroundings(traject_order=4): [StabilityWallReinforcementProfile],
            PointSurroundings(traject_order=5): [SoilReinforcementProfile],
            PointSurroundings(traject_order=6): [SoilReinforcementProfile],
            PointSurroundings(traject_order=7): [SoilReinforcementProfile],
            # CofferDamReinforcementProfile will be set for those without available measures.
            PointSurroundings(traject_order=8): [],
            PointSurroundings(traject_order=9): [],
        }
        yield StrategyInput(
            locations_matrix=_matrix, structure_min_buffer=1, structure_min_length=5
        )

    def test_get_strategy_reinforcements_given_example(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _default_order = OrderStrategy.get_default_order_for_reinforcements()
        assert _default_order[-1] == CofferdamReinforcementProfile

        # 2. Run test.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.locations_matrix, _default_order
        )

        # 3. Verify expectations
        assert isinstance(_reinforcements, list)
        assert len(_reinforcements) == len(example_strategy_input.locations_matrix)

        def assert_subset_selected_measure(selected_measure: type, subset: list):
            assert all(_r.selected_measure == selected_measure for _r in subset)

        assert_subset_selected_measure(SoilReinforcementProfile, _reinforcements[:3])
        assert_subset_selected_measure(
            StabilityWallReinforcementProfile, _reinforcements[3:5]
        )
        assert_subset_selected_measure(SoilReinforcementProfile, _reinforcements[5:8])
        assert_subset_selected_measure(
            CofferdamReinforcementProfile, _reinforcements[8:]
        )

    @pytest.fixture
    def example_location_reinforcements_with_buffering(
        self, example_strategy_input: StrategyInput
    ) -> list[StrategyLocationReinforcement]:
        _result_after_buffering_idx = [0, 0, 2, 2, 2, 2, 0, 3, 3, 3]
        _measure_order = OrderStrategy.get_default_order_for_reinforcements()
        _location_reinforcements = []
        for _idx, _location in enumerate(
            example_strategy_input.locations_matrix.keys()
        ):
            _measure_idx = _result_after_buffering_idx[_idx]
            _location_reinforcements.append(
                StrategyLocationReinforcement(
                    location=_location,
                    selected_measure=_measure_order[_measure_idx],
                    available_measures=[],
                )
            )

        yield _location_reinforcements

    def test__get_reinforcement_clusters_given_example(
        self,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategy()
        _expected_clusters = [
            (0, example_location_reinforcements_with_buffering[:2]),
            (2, example_location_reinforcements_with_buffering[2:6]),
            (0, example_location_reinforcements_with_buffering[6:7]),
            (3, example_location_reinforcements_with_buffering[7:]),
        ]

        # 2. Run test.
        _result_clusters = _strategy._get_reinforcement_clusters(
            example_location_reinforcements_with_buffering
        )

        # 3. Verify expectations.
        assert _result_clusters == _expected_clusters

    def test__get_buffer_mask_given_example(
        self, example_strategy_input: StrategyInput
    ):
        # 1. Define test data.
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.locations_matrix,
            OrderStrategy.get_default_order_for_reinforcements(),
        )
        _strategy = OrderStrategy()
        _strategy._structure_min_buffer = example_strategy_input.structure_min_buffer

        # 2. Run test.
        _mask_result = _strategy._get_buffer_mask(_reinforcements)

        # 3. Verify expectations.
        assert _mask_result == [0, 0, 2, 2, 2, 2, 0, 3, 3, 3]

    def test__apply_buffer_given_example(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        _measure_order = OrderStrategy.get_default_order_for_reinforcements()
        _reinforcements = OrderStrategy.get_strategy_reinforcements(
            example_strategy_input.locations_matrix,
            _measure_order,
        )
        _strategy = OrderStrategy()
        _strategy._structure_min_buffer = example_strategy_input.structure_min_buffer
        _expected_result_idx = [0, 0, 2, 2, 2, 2, 0, 3, 3, 3]
        _expected_result = list(map(lambda x: _measure_order[x], _expected_result_idx))

        # 2. Run test.
        _strategy._apply_buffer(_reinforcements)

        # 3. Verify expectations.
        assert all(
            _r.selected_measure == _expected_result[_r_idx]
            for _r_idx, _r in enumerate(_reinforcements)
        )

    def test__apply_min_distance_to_clusters_given_example(
        self,
        example_strategy_input: StrategyInput,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategy()
        _strategy._structure_min_length = example_strategy_input.structure_min_length
        _input_cluster = [
            (0, example_location_reinforcements_with_buffering[:2]),
            (2, example_location_reinforcements_with_buffering[2:6]),
            (0, example_location_reinforcements_with_buffering[6:7]),
            (3, example_location_reinforcements_with_buffering[7:]),
        ]
        _expected_cluster_result = [
            (0, example_location_reinforcements_with_buffering[:2]),
            (2, example_location_reinforcements_with_buffering[2:7]),
            (2, []),
            (3, example_location_reinforcements_with_buffering[7:]),
        ]

        assert _input_cluster != _expected_cluster_result

        # 2. Run test.
        _exceptions_found = _strategy._apply_min_distance_to_clusters(_input_cluster)

        # 3. Verify expectations.
        assert _exceptions_found == 0
        assert _input_cluster == _expected_cluster_result

    def test__apply_min_distance_given_example(
        self,
        example_strategy_input: StrategyInput,
        example_location_reinforcements_with_buffering: list[
            StrategyLocationReinforcement
        ],
    ):
        # 1. Define test data.
        _strategy = OrderStrategy()
        _strategy._structure_min_length = example_strategy_input.structure_min_length

        # 2. Run test.
        _strategy._apply_min_distance(example_location_reinforcements_with_buffering)

        # 3. Verify expectations.
        assert all(
            _sr.selected_measure == SoilReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[0:2]
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[2:7]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in example_location_reinforcements_with_buffering[7:]
        )

    def test_apply_strategy_given_example(self, example_strategy_input: StrategyInput):
        # 1. Define test data.
        assert isinstance(example_strategy_input, StrategyInput)

        # 2. Run test.
        _strategy_result = OrderStrategy().apply_strategy(example_strategy_input)

        # 3. Verify final expectations.
        assert isinstance(_strategy_result, list)
        assert len(_strategy_result) == len(
            example_strategy_input.locations_matrix.keys()
        )
        assert all(
            isinstance(_sr, StrategyLocationReinforcement) for _sr in _strategy_result
        )
        
        # Basically the same checks as in `test__apply_min_distance_given_example`.
        assert all(
            _sr.selected_measure == SoilReinforcementProfile
            for _sr in _strategy_result[0:2]
        )
        assert all(
            _sr.selected_measure == StabilityWallReinforcementProfile
            for _sr in _strategy_result[2:7]
        )
        assert all(
            _sr.selected_measure == CofferdamReinforcementProfile
            for _sr in _strategy_result[7:]
        )
