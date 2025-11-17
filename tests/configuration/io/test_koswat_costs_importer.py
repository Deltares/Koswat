import pytest

from koswat.configuration.io.koswat_costs_importer import KoswatCostsImporter
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from tests import test_data


class TestKoswatCostsImporter:
    def test_initialize(self):
        _importer = KoswatCostsImporter()
        assert isinstance(_importer, KoswatCostsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)
        assert _importer.include_taxes == None

    def test_import_from_without_path_raises_error(self):
        # 1. Define test data
        _importer = KoswatCostsImporter()
        _expected_err = "Costs json file not found at {}.".format(test_data)
        assert not test_data.is_file()

        # 2. Run test.
        with pytest.raises(FileNotFoundError) as exc_err:
            _importer.import_from(test_data)

        # 3. Verify expectations.
        assert _expected_err == str(exc_err.value)

    def test_import_from_with_invalid_properties_raises_error(self):
        # 1. Define test data
        _importer = KoswatCostsImporter()
        _expected_err = "A boolean value is expected for `include_taxes`."
        _test_file = test_data.joinpath("json_reader", "koswat_costs.json")
        assert _test_file.is_file()
        assert _importer.include_taxes == None

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _importer.import_from(_test_file)

        # 3. Verify expectations.
        assert _expected_err == str(exc_err.value)
