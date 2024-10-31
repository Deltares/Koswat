from configparser import ConfigParser

from koswat.configuration.io.ini.koswat_section_scenarios_ini_fom import (
    KoswatSectionScenariosIniFom,
    SectionScenarioFom,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol

_test_dict = {
    "dH": "0.1",
    "dS": "1.2",
    "dP": "2.3",
    "Buitentalud": "3.4",
    "kruinbreedte": "4.5",
}


def _validate_test_section_scenario(
    ini_fom: SectionScenarioFom, expected_name: str
) -> None:
    assert isinstance(ini_fom, SectionScenarioFom)
    assert isinstance(ini_fom, KoswatIniFomProtocol)
    assert ini_fom.scenario_name == expected_name
    assert ini_fom.d_h == 0.1
    assert ini_fom.d_s == 1.2
    assert ini_fom.d_p == 2.3
    assert ini_fom.buiten_talud == 3.4
    assert ini_fom.kruin_breedte == 4.5


class TestKoswatSectionScenarioFom:
    def test_initialize(self):
        _ini_fom = SectionScenarioFom()
        assert isinstance(_ini_fom, SectionScenarioFom)
        assert isinstance(_ini_fom, KoswatIniFomProtocol)

    def test_from_config(self):
        # 1. Define test data.
        _parser = ConfigParser()
        _parser["default"] = _test_dict

        # 2. Run test
        _ini_fom = SectionScenarioFom.from_config(_parser["default"])

        # 3. Verify expectations.
        _validate_test_section_scenario(_ini_fom, "")


class TestKoswatSectionScenariosIniFom:
    def test_initialize(self):
        _ini_fom = KoswatSectionScenariosIniFom()
        assert isinstance(_ini_fom, KoswatSectionScenariosIniFom)
        assert isinstance(_ini_fom, KoswatIniFomProtocol)

    def test_from_config(self):
        # 1. Define test data.
        _parser = ConfigParser()
        _parser["test_section"] = _test_dict

        # 2. Run test
        _ini_fom = KoswatSectionScenariosIniFom.from_config(_parser)
        assert isinstance(_ini_fom, KoswatSectionScenariosIniFom)
        assert isinstance(_ini_fom, KoswatIniFomProtocol)
        assert _ini_fom.scenario_dike_section == ""
        assert len(_ini_fom.section_scenarios) == 1
        _validate_test_section_scenario(_ini_fom.section_scenarios[0], "test_section")
