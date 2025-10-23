from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatInputProfileJsonFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class TestKoswatInputProfileJsonFom:
    def test_initialize(self):
        _csv_fom = KoswatInputProfileJsonFom()
        assert isinstance(_csv_fom, KoswatInputProfileJsonFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert _csv_fom.input_profile_fom == {}
        assert not _csv_fom.is_valid()
