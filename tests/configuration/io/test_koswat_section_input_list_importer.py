from pathlib import Path

from koswat.configuration.io.koswat_dike_section_input_list_importer import (
    KoswatDikeSectionInputListImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from tests import test_data_acceptance


class TestKoswatDikeSectionInputListImporter:
    def test_initialize(self):
        _importer = KoswatDikeSectionInputListImporter()
        assert isinstance(_importer, KoswatDikeSectionInputListImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test_import_from_without_files_imports_nothing(self, empty_dir: Path):
        # 1. Define test data.
        _json_folder = empty_dir
        _importer = KoswatDikeSectionInputListImporter(
            dike_selection=["10-1-1-A-1-A", "10-1-2-A-1-A"]
        )

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_from_with_no_selection_imports_nothing(self):
        # 1. Define test data.
        _json_folder = test_data_acceptance.joinpath("json", "dikesection_input")
        _importer = KoswatDikeSectionInputListImporter()

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_from_with_selection_imports_selected(self):
        # 1. Define test data.
        _json_folder = test_data_acceptance.joinpath("json", "dikesection_input")
        _dike_selection = ["10-1-1-A-1-A", "10-1-2-A-1-A"]
        _expected_count = len(_dike_selection)
        _importer = KoswatDikeSectionInputListImporter(dike_selection=_dike_selection)

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert len(_result) == _expected_count
        assert all(_profile.dike_section in _dike_selection for _profile in _result)
