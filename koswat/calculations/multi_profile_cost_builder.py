from koswat.builder_protocol import BuilderProtocol
from koswat.koswat_report import MultipleProfileCostReport
from koswat.surroundings.koswat_surroundings import KoswatSurroundings


class MultiProfileCostBuilder(BuilderProtocol):
    surroundings: KoswatSurroundings

    def build(self) -> MultipleProfileCostReport:
        return super().build()
