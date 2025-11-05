from configparser import ConfigParser

from koswat.configuration.io.json.koswat_section_scenario_json_fom import (
    KoswatSectionScenariosJsonFom,
    SectionScenarioFom,
)
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol

_test_dict = {
    "dh": "0.1",
    "ds": "1.2",
    "dp": "2.3",
    "buitentalud": "3.4",
    "kruinbreedte": "4.5",
}


def _validate_test_section_scenario(
    input_fom: SectionScenarioFom, expected_name: str
) -> None:
    assert isinstance(input_fom, SectionScenarioFom)
    assert isinstance(input_fom, KoswatIniFomProtocol)
    assert input_fom.scenario_name == expected_name
    assert input_fom.d_h == 0.1
    assert input_fom.d_s == 1.2
    assert input_fom.d_p == 2.3
    assert input_fom.waterside_slope == 3.4
    assert input_fom.crest_width == 4.5


class TestKoswatSectionScenarioJsonFom:
    def test_initialize(self):
        _input_fom = SectionScenarioFom()
        assert isinstance(_input_fom, SectionScenarioFom)
        assert isinstance(_input_fom, KoswatJsonFomProtocol)

    def test_from_config(self):
        # 1. Run test
        _ini_fom = SectionScenarioFom.from_config(_test_dict)

        # 2. Verify expectations
        _validate_test_section_scenario(_ini_fom, "")


class TestKoswatSectionScenariosJsonFom:
    def test_initialize(self):
        _input_fom = KoswatSectionScenariosJsonFom()
        assert isinstance(_input_fom, KoswatSectionScenariosJsonFom)
        assert isinstance(_input_fom, KoswatIniFomProtocol)

    def test_from_config(self):
        # 1. Define test data
        _input_dict = {"test_section": _test_dict}

        # 2. Run test
        _ini_fom = KoswatSectionScenariosJsonFom.from_config(_input_dict)

        # 3. Verify expectations
        assert isinstance(_ini_fom, KoswatSectionScenariosJsonFom)
        assert isinstance(_ini_fom, KoswatIniFomProtocol)
        assert _ini_fom.scenario_dike_section == ""
        assert len(_ini_fom.section_scenarios) == 1
        _validate_test_section_scenario(_ini_fom.section_scenarios[0], "test_section")
