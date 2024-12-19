from typing import Iterator

import pytest

from koswat.configuration.settings.koswat_scenario import KoswatScenario
from koswat.configuration.settings.reinforcements.koswat_cofferdam_settings import (
    KoswatCofferdamSettings,
)
from koswat.configuration.settings.reinforcements.koswat_piping_wall_settings import (
    KoswatPipingWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_reinforcement_settings import (
    KoswatReinforcementSettings,
)
from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)
from koswat.configuration.settings.reinforcements.koswat_stability_wall_settings import (
    KoswatStabilityWallSettings,
)
from koswat.configuration.settings.reinforcements.koswat_vps_settings import (
    KoswatVPSSettings,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from koswat.dike_reinforcements.reinforcement_profile.berm_calculator.piping_berm_calculator import (
    PipingBermCalculator,
)


@pytest.fixture(name="valid_scenario")
def _get_valid_scenario_fixture() -> Iterator[KoswatScenario]:
    yield KoswatScenario(
        scenario_name="Test Scenario",
        scenario_section="Test Section",
        d_h=1.5,
        d_s=2.0,
        d_p=3.0,
        crest_width=4.0,
        waterside_slope=0.3,
    )


@pytest.fixture(name="valid_reinforcement_settings")
def _get_valid_reinforcement_settings_fixture() -> Iterator[
    KoswatReinforcementSettings
]:
    yield KoswatReinforcementSettings(
        soil_settings=KoswatSoilSettings(),
        vps_settings=KoswatVPSSettings(polderside_berm_width_vps=10),
        piping_wall_settings=KoswatPipingWallSettings(
            transition_cbwall_sheetpile=10.0,
        ),
        stability_wall_settings=KoswatStabilityWallSettings(
            transition_sheetpile_diaphragm_wall=15.0,
        ),
        cofferdam_settings=KoswatCofferdamSettings(),
    )


@pytest.fixture
def valid_input_profile() -> Iterator[KoswatInputProfileBase]:
    yield KoswatInputProfileBase(
        crest_height=5.0,
        waterside_ground_level=0.0,
        waterside_berm_height=3.0,
        waterside_slope=0.3,
        waterside_berm_width=2.0,
        polderside_ground_level=1.0,
        polderside_berm_height=2.0,
        polderside_slope=0.4,
        polderside_berm_width=8.0,
    )


@pytest.fixture
def valid_piping_berm_calculator(
    valid_scenario: KoswatScenario,
    valid_reinforcement_settings: KoswatReinforcementSettings,
) -> Iterator[PipingBermCalculator]:
    yield PipingBermCalculator(
        scenario=valid_scenario,
        reinforcement_settings=valid_reinforcement_settings,
        dikebase_piping_old=12.0,
        dikebase_piping_new=14.0,
        dikebase_height_new=15.0,
        dikebase_stability_new=16.0,
        dike_height_new=7.0,
    )
