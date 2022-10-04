from koswat.surroundings.koswat_buildings_polderside import (
    KoswatBuildingsPolderside,
    PointSurroundings,
)


class TestPointSurroundings:
    def test_initialize_point_surroundings(self):
        _p_s = PointSurroundings()
        assert isinstance(_p_s, PointSurroundings)
        assert not _p_s.section
        assert not _p_s.location
        assert not _p_s.distance_to_buildings


class TestKoswatBuildingsPolderside:
    def test_initialize_koswat_buildings_polderside(self):
        _kbp = KoswatBuildingsPolderside()
        assert isinstance(_kbp, KoswatBuildingsPolderside)
        assert not _kbp.conflicting_points
