from koswat.configuration.io.json.koswat_dike_section_input_json_fom import (
    KoswatDikeSectionInputJsonFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class TestKoswatInputProfileJsonFom:
    def test_initialize(self):
        # 1. Execute test
        _csv_fom = KoswatDikeSectionInputJsonFom()

        # 2. Verify expectations
        assert isinstance(_csv_fom, KoswatDikeSectionInputJsonFom)
        assert isinstance(_csv_fom, FileObjectModelProtocol)
        assert not _csv_fom.is_valid()
