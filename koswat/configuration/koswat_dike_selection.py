from typing import List

from koswat.configuration.koswat_config_protocol import KoswatConfigProtocol


class KoswatDikeSelection(KoswatConfigProtocol):
    dike_sections: List[str]

    def __init__(self) -> None:
        self.dike_sections = []

    def is_valid(self) -> bool:
        return self.dike_sections is not None and len(self.dike_sections) > 0
