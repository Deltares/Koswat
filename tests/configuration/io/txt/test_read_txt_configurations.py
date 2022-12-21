from koswat.configuration.io.txt.koswat_dike_selection_txt_fom import (
    KoswatDikeSelectionTxtFom,
)
from koswat.core.io.txt.koswat_txt_reader import KoswatTxtReader
from tests import test_data

test_ini_reader_data = test_data / "txt_reader"


class TestReadTxtConfigurations:
    def test_koswat_ini_read_dike_selection_ini(self):
        # 1. Define test data.
        _test_file_path = test_ini_reader_data / "koswat_dike_selection.txt"
        _ini_reader = KoswatTxtReader()
        _ini_reader.koswat_txt_fom_type = KoswatDikeSelectionTxtFom

        # 2. Run test
        _txt_fom = _ini_reader.read(_test_file_path)

        # 3. Validate expectations.
        assert isinstance(_txt_fom, KoswatDikeSelectionTxtFom)

        # Dijksecties
        assert len(_txt_fom.dike_sections) == 3
        assert _txt_fom.dike_sections[0] == "10-1-1-A-1-A"
        assert _txt_fom.dike_sections[1] == "10-1-2-A-1-A"
        assert _txt_fom.dike_sections[2] == "10-1-3-A-1-B-1"
