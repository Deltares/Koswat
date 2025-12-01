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

from pathlib import Path
from typing import Type

from koswat.core.io.koswat_reader_protocol import KoswatReaderProtocol
from koswat.core.io.txt.koswat_txt_fom_protocol import KoswatTxtFomProtocol


class KoswatTxtReader(KoswatReaderProtocol):

    koswat_txt_fom_type: Type[KoswatTxtFomProtocol]

    def __init__(self) -> None:
        self.koswat_txt_fom_type = None

    def supports_file(self, file_path: Path) -> bool:
        return isinstance(file_path, Path) and file_path.suffix.lower() == ".txt"

    def read(self, file_path: Path) -> KoswatTxtFomProtocol:
        if not self.supports_file(file_path):
            raise ValueError("Txt file should be provided")
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        if not self.koswat_txt_fom_type:
            raise ValueError("KoswatTxtFom type needs to be specified.")

        return self.koswat_txt_fom_type.from_text(file_path.read_text())
