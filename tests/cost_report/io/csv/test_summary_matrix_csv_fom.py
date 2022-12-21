from koswat.core.io.csv.koswat_csv_fom_protocol import KoswatCsvFomProtocol
from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom


class TestSummaryMatrixCsvFom:
    def test_initialize(self):
        _fom = SummaryMatrixCsvFom()
        assert isinstance(_fom, SummaryMatrixCsvFom)
        assert isinstance(_fom, KoswatCsvFomProtocol)
        assert not _fom.headers
        assert not _fom.cost_rows
        assert not _fom.location_rows
        assert not _fom.is_valid()

    def test_is_valid(self):
        # 1. Define test data.
        _fom = SummaryMatrixCsvFom()
        _header = "Officia excepteur elit commodo aliquip id nisi."
        _fom.headers = [_header]
        _fom.cost_rows = [["a row in a list"]]
        _fom.location_rows = [["another row in a list"]]

        # 2. Run test
        assert _fom.is_valid()
