from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol
from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionCostsSettings,
    ConstructionFactors,
)
from koswat.configuration.settings.koswat_general_settings import ConstructionTypeEnum


class TestConstructionCostsSettings:
    def test_initialize(self):
        _construction_costs_settings = ConstructionCostsSettings()
        assert isinstance(_construction_costs_settings, ConstructionCostsSettings)
        assert isinstance(_construction_costs_settings, KoswatConfigProtocol)

    def test_valid_costs_settings(self):
        def _populate_construction_factors(
            factor_values: list[float],
        ) -> ConstructionFactors:
            _factors = ConstructionFactors()
            _factors.c_factor = factor_values[0]
            _factors.d_factor = factor_values[1]
            _factors.z_factor = factor_values[2]
            _factors.f_factor = factor_values[3]
            _factors.g_factor = factor_values[4]
            return _factors

        # 1. Define test data
        _construction_costs_settings = ConstructionCostsSettings()
        _construction_costs_settings.vzg = _populate_construction_factors(
            list(range(5))
        )
        _construction_costs_settings.cb_damwand = _populate_construction_factors(
            list(range(5))
        )
        _construction_costs_settings.damwand_onverankerd = (
            _populate_construction_factors(list(range(5)))
        )
        _construction_costs_settings.damwand_verankerd = _populate_construction_factors(
            list(range(5))
        )
        _construction_costs_settings.diepwand = _populate_construction_factors(
            list(range(5))
        )
        _construction_costs_settings.kistdam = _populate_construction_factors(
            list(range(5))
        )

        # 2. Run test
        _is_valid = _construction_costs_settings.is_valid()

        # 3. Verify expectations
        assert _is_valid

    def test_get_construction_factors(self):
        # 1. Define test data
        _construction_type = ConstructionTypeEnum.CB_DAMWAND
        _construction_costs_settings = ConstructionCostsSettings()
        _construction_costs_settings.cb_damwand = ConstructionFactors(
            c_factor=0.1, d_factor=1.2, z_factor=2.3, f_factor=3.4, g_factor=4.5
        )

        # 2. Run test
        _construction_factors = _construction_costs_settings.get_construction_factors(
            _construction_type
        )

        # 3. Verify expectations
        assert _construction_factors.c_factor == 0.1
        assert _construction_factors.d_factor == 1.2
        assert _construction_factors.z_factor == 2.3
        assert _construction_factors.f_factor == 3.4
        assert _construction_factors.g_factor == 4.5
