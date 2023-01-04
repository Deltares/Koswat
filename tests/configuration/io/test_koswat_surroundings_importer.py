from pathlib import Path

import pytest

from koswat.configuration.io.koswat_surroundings_importer import (
    KoswatSurroundingsImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol


class TestKoswatSurroundingsImporter:
    def test_initialize(self):
        _importer = KoswatSurroundingsImporter()
        assert isinstance(_importer, KoswatSurroundingsImporter)
        assert isinstance(_importer, KoswatImporterProtocol)
        assert _importer.traject_loc_shp_file == None
        assert _importer.selected_locations == []

    def test_import_from_raises_when_from_path_not_given(self):
        # 1. Define test data.
        _importer = KoswatSurroundingsImporter()
        _expected_error = "No surroundings csv directory path given."

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _importer.import_from(None)

        # 3. Verify expectations.
        assert _expected_error == str(exc_err.value)

    def test_import_from_raises_when_traject_loc_shp_file_not_given(self):
        # 1. Define test data.
        _importer = KoswatSurroundingsImporter()
        _expected_error = "No traject shp file path given."

        # 2. Run test.
        with pytest.raises(ValueError) as exc_err:
            _importer.import_from(Path())

        # 3. Verify expectations.
        assert _expected_error == str(exc_err.value)
