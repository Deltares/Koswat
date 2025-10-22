from pathlib import Path

from koswat.configuration.io.koswat_input_profile_list_importer import (
    KoswatInputProfileListImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from tests import test_data_acceptance


class TestKoswatInputProfileListImporter:
    def test_initialize(self):
        _importer = KoswatInputProfileListImporter()
        assert isinstance(_importer, KoswatInputProfileListImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test__get_koswat_input_profile_base(self):
        # 1. Define test data.
        _importer = KoswatInputProfileListImporter()
        _test_fom_dict = {
            "dijksectie": "test_section",
            "buiten_maaiveld": "1.1",
            "buiten_talud": "2.2",
            "buiten_berm_hoogte": "3.3",
            "buiten_berm_lengte": "4.4",
            "kruin_hoogte": "5.5",
            "kruin_breedte": "6.6",
            "binnen_talud": "7.7",
            "binnen_berm_hoogte": "8.8",
            "binnen_berm_lengte": "9.9",
            "binnen_maaiveld": "0.0",
            "grondprijs_bebouwd": "111",
            "grondprijs_onbebouwd": "11",
            "factorzetting": "1.1",
            "pleistoceen": "-3.3",
            "aquifer": "-2.1",
            "dikte_deklaag": "1.2",
        }

        # 2. Run test.
        _input_profile_base = _importer._get_koswat_input_profile_base(_test_fom_dict)

        # 3. Verify final expectations.
        assert isinstance(_input_profile_base, KoswatInputProfileBase)
        assert _input_profile_base.dike_section == "test_section"
        assert _input_profile_base.waterside_ground_level == 1.1
        assert _input_profile_base.waterside_slope == 2.2
        assert _input_profile_base.waterside_berm_height == 3.3
        assert _input_profile_base.waterside_berm_width == 4.4
        assert _input_profile_base.crest_height == 5.5
        assert _input_profile_base.crest_width == 6.6
        assert _input_profile_base.polderside_slope == 7.7
        assert _input_profile_base.polderside_berm_height == 8.8
        assert _input_profile_base.polderside_berm_width == 9.9
        assert _input_profile_base.polderside_ground_level == 0.0
        assert _input_profile_base.ground_price_builtup == 111
        assert _input_profile_base.ground_price_unbuilt == 11
        assert _input_profile_base.factor_settlement == 1.1
        assert _input_profile_base.pleistocene == -3.3
        assert _input_profile_base.aquifer == -2.1
        assert _input_profile_base.top_layer_thickness == 1.2

    def test_import_from_without_files_imports_nothing(self):
        # 1. Define test data.
        _json_folder = Path(__file__).parent
        _importer = KoswatInputProfileListImporter(
            dike_selection=["10-1-1-A-1-A", "10-1-2-A-1-A"]
        )

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert _result == []

    def test_import_from_with_no_selection_imports_all(self):
        # 1. Define test data.
        _json_folder = test_data_acceptance.joinpath("json", "dikesection_input")
        _expected_count = len(list(_json_folder.glob("*.json")))
        _importer = KoswatInputProfileListImporter()

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert len(_result) == _expected_count

    def test_import_from_with_selection_imports_selected(self):
        # 1. Define test data.
        _json_folder = test_data_acceptance.joinpath("json", "dikesection_input")
        _dike_selection = ["10-1-1-A-1-A", "10-1-2-A-1-A"]
        _importer = KoswatInputProfileListImporter(dike_selection=_dike_selection)

        # 2. Run test.
        _result = _importer.import_from(_json_folder)

        # 3. Verify final expectations.
        assert len(_result) == len(_dike_selection)
        assert all(_profile.dike_section in _dike_selection for _profile in _result)
