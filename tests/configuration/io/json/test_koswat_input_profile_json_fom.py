from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatDikeSectionInputJsonFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class TestKoswatInputProfileJsonFom:
    def test_initialize(self):
        _csv_fom = KoswatDikeSectionInputJsonFom()
        assert isinstance(_csv_fom, KoswatDikeSectionInputJsonFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert _csv_fom.input_profile == {}
        assert not _csv_fom.is_valid()
