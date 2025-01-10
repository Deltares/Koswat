from koswat.configuration.io.csv.koswat_surroundings_csv_fom import (
    KoswatSurroundingsWrapperCsvFom,
)
from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol


class TestKoswatSurroundingsWrapperCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatSurroundingsWrapperCsvFom()
        assert isinstance(_csv_fom, KoswatSurroundingsWrapperCsvFom)
        assert isinstance(_csv_fom, KoswatCsvFomProtocol)
        assert not _csv_fom.is_valid()
