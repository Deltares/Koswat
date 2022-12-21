import pytest

from koswat.core.io.csv.koswat_csv_fom import KoswatCsvFom
from koswat.core.io.csv.koswat_csv_writer import KoswatCsvWriter
from koswat.core.io.koswat_writer_protocol import KoswatWriterProtocol
from tests import get_test_results_dir


class TestKoswatCsvWriter:
    def test_initialize(self):
        _csv_writer = KoswatCsvWriter()
        assert isinstance(_csv_writer, KoswatCsvWriter)
        assert isinstance(_csv_writer, KoswatWriterProtocol)
        assert _csv_writer.separator == ";"

    def test_write(self, request: pytest.FixtureRequest):
        # 1. Define test data.
        _test_file = get_test_results_dir(request) / "test_data.csv"
        _csv_fom = KoswatCsvFom()
        _csv_fom.headers = ["a header", "another header"]
        _csv_fom.entries = [["row_0", "col_1"], ["row_1", "col_1"]]
        _expected_result = "a header;another header\nrow_0;col_1\nrow_1;col_1"

        # 2. Run test.
        KoswatCsvWriter().write(_csv_fom, _test_file)

        # 3. Verify expectations.
        assert _test_file.is_file()
        _text = _test_file.read_text()
        assert _text == _expected_result
