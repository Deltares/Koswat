from __future__ import annotations

from typing import List

from koswat.io.txt.koswat_txt_fom_protocol import KoswatTxtFomProtocol


class KoswatDikeSelectionTxtFom(KoswatTxtFomProtocol):
    dike_sections: List[str]

    @classmethod
    def from_text(cls, file_text: str) -> KoswatDikeSelectionTxtFom:
        _ini_fom = cls()
        _ini_fom.dike_sections = file_text.splitlines(keepends=False)
        return _ini_fom

    def is_valid(self) -> bool:
        return self.dike_sections is not None and len(self.dike_sections) > 0
