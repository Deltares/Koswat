from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatTrajectSurroundingsCsvFom,
    KoswatTrajectSurroundingsWrapperCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class TestKoswatTrajectSurroundingsCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatTrajectSurroundingsCsvFom()
        assert isinstance(_csv_fom, KoswatTrajectSurroundingsCsvFom)
        assert isinstance(_csv_fom, KoswatCsvFomProtocol)
        assert _csv_fom.points_surroundings_list == []
        assert _csv_fom.distances_list == []
        assert _csv_fom.traject == ""
        assert not _csv_fom.is_valid()


class TestKoswatTrajectSurroundingsWrapperCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatTrajectSurroundingsWrapperCsvFom()
        assert isinstance(_csv_fom, KoswatTrajectSurroundingsWrapperCsvFom)
        assert isinstance(_csv_fom, KoswatCsvFomProtocol)
        assert not _csv_fom.is_valid()
