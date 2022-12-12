from __future__ import annotations

from typing import List

from koswat.configuration.models.koswat_dike_selection import KoswatDikeSelection
from koswat.io.txt.koswat_txt_fom_protocol import KoswatTxtFomProtocol


class KoswatDikeSelectionTxtFom(KoswatDikeSelection, KoswatTxtFomProtocol):
    dike_sections: List[str]

    @classmethod
    def from_text(cls, file_text: str) -> KoswatDikeSelectionTxtFom:
        _ini_fom = cls()
        _ini_fom.dike_sections = file_text.splitlines(keepends=False)
        return _ini_fom
