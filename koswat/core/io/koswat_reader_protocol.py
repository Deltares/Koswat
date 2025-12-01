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

from pathlib import Path
from typing import Protocol, runtime_checkable

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


@runtime_checkable
class KoswatReaderProtocol(Protocol):
    def supports_file(self, file_path: Path) -> bool:
        """
        Validates whether the current reader is capable of importing data from the provided file.

        Args:
            file_path (Path): Path to a file that should be imported.

        Returns:
            bool: Result of validation.
        """
        pass

    def read(self, file_path: Path) -> FileObjectModelProtocol:
        """
        Imports the data from the `file_path` into a concrete implementation of a `FileObjectModelProtocol`.

        Args:
            file_path (Path): Path to a file that should be imported.

        Returns:
            FileObjectModelProtocol: Model representing the data in the file.
        """
        pass
