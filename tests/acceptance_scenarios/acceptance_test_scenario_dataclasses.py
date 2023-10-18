from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.dike.koswat_profile_protocol import KoswatProfileProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from itertools import product
from koswat.dike.profile.koswat_profile import KoswatProfileBase

from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from tests import test_data


@dataclass
class LayersTestCase:
    layers_dict: dict
    case_name: str


@dataclass
class AcceptanceTestScenario:
    profile_case: KoswatProfileProtocol
    scenario_case: KoswatScenario
    layer_case: LayersTestCase

    @property
    def case_name(self) -> str:
        return "case_{}_{}_{}".format(
            self.profile_case.input_data.dike_section,
            self.scenario_case.scenario_name,
            self.layer_case.case_name,
        )

    @property
    def reference_data_dir(self) -> Path:
        return test_data.joinpath("acceptance_reference_data", self.case_name)


@dataclass
class AcceptanceTestScenarioCombinations:
    profile_case: KoswatInputProfileBase
    layers_cases: list[LayersTestCase]
    scenario_cases: list[KoswatScenario]

    def get_test_cases(self) -> list[pytest.param]:
        def to_pytest_case(
            test_scenario: tuple[KoswatInputProfileBase, LayersTestCase, KoswatScenario]
        ) -> pytest.param:
            _profile_case, _layer_case, _scenario_case = test_scenario
            _input_profile_case = KoswatProfileBuilder.with_data(
                dict(
                    input_profile_data=_profile_case,
                    layers_data=_layer_case.layers_dict,
                    profile_type=KoswatProfileBase,
                )
            ).build()
            _test_case = AcceptanceTestScenario(
                profile_case=_input_profile_case,
                layer_case=_layer_case,
                scenario_case=_scenario_case,
            )
            return pytest.param(_test_case, id=_test_case.case_name)

        _cases = [
            [self.profile_case],
            self.layers_cases,
            self.scenario_cases,
        ]
        return list(map(to_pytest_case, product(*_cases)))

    @staticmethod
    def get_all_cases(
        list_combinations: list[AcceptanceTestScenarioCombinations],
    ) -> list[pytest.param]:
        # Gets all cases available.
        # Python trick by using the `sum` operator to flatten lists.
        return sum(map(lambda x: x.get_test_cases(), list_combinations), [])
