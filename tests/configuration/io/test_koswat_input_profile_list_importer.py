from koswat.configuration.io.koswat_input_profile_list_importer import (
    KoswatInputProfileListImporter,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class TestKoswatInputProfileListImporter:
    def test_initialize(self):
        _importer = KoswatInputProfileListImporter()
        assert isinstance(_importer, KoswatInputProfileListImporter)
        assert isinstance(_importer, KoswatImporterProtocol)

    def test_get_koswat_input_profile_base(self):
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
            "pleistoceen": "-1.1",
            "aquifer": "-2.2",
        }

        # 2. Run test.
        _input_profile_base = _importer._get_koswat_input_profile_base(_test_fom_dict)

        # 3. Verify final expectations.
        assert isinstance(_input_profile_base, KoswatInputProfileBase)
        assert _input_profile_base.dike_section == "test_section"
        assert _input_profile_base.buiten_maaiveld == 1.1
        assert _input_profile_base.buiten_talud == 2.2
        assert _input_profile_base.buiten_berm_hoogte == 3.3
        assert _input_profile_base.buiten_berm_breedte == 4.4
        assert _input_profile_base.kruin_hoogte == 5.5
        assert _input_profile_base.kruin_breedte == 6.6
        assert _input_profile_base.binnen_talud == 7.7
        assert _input_profile_base.binnen_berm_hoogte == 8.8
        assert _input_profile_base.binnen_berm_breedte == 9.9
        assert _input_profile_base.binnen_maaiveld == 0.0
        assert _input_profile_base.pleistoceen == -1.1
        assert _input_profile_base.aquifer == -2.2
