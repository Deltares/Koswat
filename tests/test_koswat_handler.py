from koswat.koswat_handler import KoswatHandler
from tests import test_data


class TestKoswatHandler:
    def test_koswat_handler_initialize(self):
        _handler = KoswatHandler()
        assert isinstance(_handler, KoswatHandler)

    def test_koswat_handler_run_analysis_given_valid_data(self):
        _handler = KoswatHandler()
        _ini_file = test_data / "acceptance" / "koswat_general.ini"
        assert _ini_file.is_file()

        _handler.run_analysis(_ini_file)
