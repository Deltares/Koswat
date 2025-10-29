import pytest

from koswat.configuration.settings.reinforcements.koswat_soil_settings import (
    KoswatSoilSettings,
)


class TestKoswatSoilSettings:

    @pytest.fixture
    def empty_soil_settings(self) -> KoswatSoilSettings:
        return KoswatSoilSettings(
            soil_surtax_factor=None,
            land_purchase_surtax_factor=None,
            min_berm_height=None,
            max_berm_height_factor=None,
            factor_increase_berm_height=None,
        )

    def _get_filled_soil_settings(self) -> KoswatSoilSettings:
        return KoswatSoilSettings()

    @pytest.fixture
    def filled_soil_settings(self) -> KoswatSoilSettings:
        return self._get_filled_soil_settings()

    @pytest.mark.parametrize(
        "instance, defaults",
        [
            pytest.param(
                "empty_soil_settings", "filled_soil_settings", id="Filled to Empty"
            ),
            pytest.param(
                "filled_soil_settings", "filled_soil_settings", id="Filled to Filled"
            ),
            pytest.param(
                "filled_soil_settings", "empty_soil_settings", id="Empty to Filled"
            ),
        ],
    )
    def test_set_defaults(
        self,
        request: pytest.FixtureRequest,
        instance: str,
        defaults: str,
    ):
        # 1. Define test data
        _instance: KoswatSoilSettings = request.getfixturevalue(instance)
        _defaults = request.getfixturevalue(defaults)
        _expected_results = self._get_filled_soil_settings()

        # 2. Execute test
        _result = _instance.set_defaults(_defaults)

        # 3. Verify expectations
        assert _result == _expected_results
