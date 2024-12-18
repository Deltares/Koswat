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
from koswat.dike_reinforcements.input_profile.cofferdam.cofferdam_input_profile import (
    CofferDamInputProfile,
)
from koswat.dike_reinforcements.input_profile.soil.soil_input_profile import (
    SoilInputProfile,
)
from koswat.dike_reinforcements.input_profile.stability_wall.stability_wall_input_profile import (
    StabilityWallInputProfile,
)


@pytest.fixture
def valid_scenario() -> Iterator[KoswatScenario]:
    yield KoswatScenario(
        scenario_name="Test Scenario",
        scenario_section="Test Section",
        d_h=1.0,
        d_s=2.0,
        d_p=3.0,
        crest_width=4.0,
        waterside_slope=0.3,
    )


@pytest.fixture
def valid_reinforcement_settings() -> Iterator[KoswatReinforcementSettings]:
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
def valid_soil_input_profile() -> Iterator[SoilInputProfile]:
    yield SoilInputProfile(
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
def valid_stability_wall_input_profile() -> Iterator[StabilityWallInputProfile]:
    yield StabilityWallInputProfile(
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
def valid_cofferdam_input_profile() -> Iterator[CofferDamInputProfile]:
    yield CofferDamInputProfile(
        crest_height=5.0,
        waterside_ground_level=0.0,
        waterside_berm_height=3.0,
        waterside_slope=0.3,
        waterside_berm_width=0.0,
        polderside_ground_level=1.0,
        polderside_berm_height=2.0,
        polderside_slope=0.4,
        polderside_berm_width=0.0,
    )
