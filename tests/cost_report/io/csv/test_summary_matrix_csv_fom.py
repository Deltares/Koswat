from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom
from koswat.io.file_object_model_protocol import FileObjectModelProtocol


class TestSummaryMatrixCsvFom:
    def test_initialize(self):
        _fom = SummaryMatrixCsvFom()
        assert isinstance(_fom, SummaryMatrixCsvFom)
        assert isinstance(_fom, FileObjectModelProtocol)
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

    def test_get_lines(self):
        # 1. Define test data.
        _fom = SummaryMatrixCsvFom()
        _header = "Amet nisi ad duis nostrud irure proident dolore nisi culpa."
        _fom.headers = [_header]
        _fom.cost_rows = [["a", "b"], ["c", "d"]]
        _fom.location_rows = [["1", "2"], ["3", "4"]]
        _expected_result = [_header, "a;b", "c;d", "1;2", "3;4"]

        # 2. Run test
        _lines = _fom.get_lines()

        # 3. Verify expectations.
        assert len(_lines) == 5
        assert _lines == _expected_result
