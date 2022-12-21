from koswat.core.protocols import BuilderProtocol
from koswat.dike.surroundings.point.point_surroundings_builder import (
    PointSurroundingsBuilder,
)


class TestPointSurroundingsBuilder:
    def test_initialize(self):
        _builder = PointSurroundingsBuilder()
        assert isinstance(_builder, PointSurroundingsBuilder)
        assert isinstance(_builder, BuilderProtocol)
        assert not _builder.point_surroundings_data
