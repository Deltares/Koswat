from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class TestKoswatSurroundingsCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatSurroundingsCsvFom()
        assert isinstance(_csv_fom, KoswatSurroundingsCsvFom)
        assert isinstance(_csv_fom, KoswatCsvFomProtocol)
        assert not _csv_fom.points_surroundings_list
        assert not _csv_fom.distances_list
        assert _csv_fom.section == ""
        assert not _csv_fom.is_valid()
