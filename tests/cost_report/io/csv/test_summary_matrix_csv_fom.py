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
        _fom.headers = ["a header"]
        _fom.cost_rows = ["a row"]
        _fom.location_rows = ["another row"]

        # 2. Run test
        assert _fom.is_valid()
