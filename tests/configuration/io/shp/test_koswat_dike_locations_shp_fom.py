from koswat.configuration.io.shp.koswat_dike_locations_shp_fom import (
    KoswatDikeLocationsShpFom,
)
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class TestKoswatDikeLocationsShpFom:
    def test_initialize(self):
        _shp_fom = KoswatDikeLocationsShpFom()

        assert isinstance(_shp_fom, KoswatDikeLocationsShpFom)
        assert isinstance(_shp_fom, FileObjectModelProtocol)
        assert _shp_fom.initial_point == None
        assert _shp_fom.end_point == None
        assert _shp_fom.record == None
        assert _shp_fom.dike_section == ""
        assert _shp_fom.dike_traject == ""
        assert _shp_fom.dike_subtraject == ""
        assert not _shp_fom.is_valid()
