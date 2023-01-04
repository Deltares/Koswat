from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class TestKoswatInputProfilesCsvFom:
    def test_initialize(self):
        _csv_fom = KoswatInputProfilesCsvFom()
        assert isinstance(_csv_fom, KoswatInputProfilesCsvFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert _csv_fom.input_profile_fom_list == []
        assert not _csv_fom.is_valid()