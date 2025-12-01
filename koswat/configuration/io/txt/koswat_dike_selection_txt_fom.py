"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from typing import List

from koswat.core.io.txt.koswat_txt_fom_protocol import KoswatTxtFomProtocol


class KoswatDikeSelectionTxtFom(KoswatTxtFomProtocol):
    dike_sections: List[str]

    @classmethod
    def from_text(cls, file_text: str) -> KoswatDikeSelectionTxtFom:
        _txt_fom = cls()
        _txt_fom.dike_sections = file_text.splitlines(keepends=False)
        return _txt_fom
