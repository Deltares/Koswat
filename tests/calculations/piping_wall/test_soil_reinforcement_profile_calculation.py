from typing import List

import pytest
from shapely.geometry.point import Point

from koswat.builder_protocol import BuilderProtocol
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile import (
    PipingWallReinforcementProfile,
)
from koswat.calculations.piping_wall.piping_wall_reinforcement_profile_calculation import (
    PipingWallReinforcementProfileCalculation,
)
from koswat.calculations.reinforcement_profile_calculation_protocol import (
    ReinforcementProfileCalculationProtocol,
)
from koswat.dike.layers.koswat_layers import KoswatLayers
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike.profile.koswat_profile import KoswatProfileBase
from koswat.dike.profile.koswat_profile_builder import KoswatProfileBuilder
from koswat.koswat_scenario import KoswatScenario
from tests.library_test_cases import (
    InputProfileCases,
    InputProfileScenarioLookup,
    LayersCases,
    ScenarioCases,
)


class TestPipingWallReinforcementProfileCalculation:
    def test_initialize(self):
        _calculation = PipingWallReinforcementProfileCalculation()
        assert _calculation
        assert not _calculation.base_profile
        assert not _calculation.scenario
        assert isinstance(_calculation, PipingWallReinforcementProfileCalculation)
        assert isinstance(_calculation, ReinforcementProfileCalculationProtocol)
        assert isinstance(_calculation, BuilderProtocol)
