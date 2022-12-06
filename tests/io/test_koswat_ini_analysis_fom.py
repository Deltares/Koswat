import pytest

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini import KoswatIniAnalysisFom, KoswatIniAnalysisFomBuilder
from koswat.io.koswat_reader_protocol import FileObjectModelProtocol


class TestKoswatIniAnalysisFom:
    def test_initialize_koswat_ini_analysis_fom(self):
        _ini_analysis_fom = KoswatIniAnalysisFom()
        assert isinstance(_ini_analysis_fom, KoswatIniAnalysisFom)
        assert isinstance(_ini_analysis_fom, FileObjectModelProtocol)
        assert not _ini_analysis_fom.dijksectiesSelectie
        assert not _ini_analysis_fom.dijksectieLigging
        assert not _ini_analysis_fom.dijksectieInvoer
        assert not _ini_analysis_fom.scenarioInvoer
        assert not _ini_analysis_fom.eenheidsprijzen
        assert not _ini_analysis_fom.uitvoerfolder
        assert not _ini_analysis_fom.BTW
        assert not _ini_analysis_fom.is_valid()


class TestKoswatIniAnalysisFomBuilder:
    def test_initialize_empty_koswat_ini_analysis_fom_builder(self):
        fom_builder = KoswatIniAnalysisFomBuilder()
        assert isinstance(fom_builder, KoswatIniAnalysisFomBuilder) == True
        assert isinstance(fom_builder, BuilderProtocol) == True
        assert not fom_builder.section
        assert not fom_builder._is_valid()

    def test_initialize_with_dict_koswat_ini_analysis_fom_builder(self):
        fom_builder = KoswatIniAnalysisFomBuilder()
        fom_builder.section = dict(
            {
                "Dijksecties_Selectie": "Dijksectie_Selectie1",
                "Dijksectie_Ligging": "Dijksectie_Ligging1",
                "Dijksectie_Invoer": "Dijksectie_Invoer1",
                "Scenario_Invoer": "Scenario_Invoer1",
                "Eenheidsprijzen": "Eenheidsprijzen1",
                "Uitvoerfolder": "Uitvoerfolder1",
                "BTW": "True",
            }
        )
        fom = fom_builder.build()
        assert fom.dijksectiesSelectie == "Dijksectie_Selectie1"
        assert fom.dijksectieLigging == "Dijksectie_Ligging1"
        assert fom.dijksectieInvoer == "Dijksectie_Invoer1"
        assert fom.scenarioInvoer == "Scenario_Invoer1"
        assert fom.eenheidsprijzen == "Eenheidsprijzen1"
        assert fom.uitvoerfolder == "Uitvoerfolder1"
        assert fom.BTW == True
        assert fom.is_valid()

    def test_initialize_with_half_dict_koswat_ini_analysis_fom_builder(self):
        fom_builder = KoswatIniAnalysisFomBuilder()
        fom_builder.section = dict(
            {
                "Dijksecties_Selectie": "DijksectieSelectie1",
                "Dijksectie_Ligging": "DijksectieLigging1",
            }
        )
        fom = fom_builder.build()
        assert not fom.is_valid()
