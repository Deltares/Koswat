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
from typing import Protocol, runtime_checkable

from koswat.core.protocols.data_object_model_protocol import DataObjectModelProtocol


@runtime_checkable
class KoswatImporterProtocol(Protocol):
    def import_from(
        self, from_path: Path
    ) -> DataObjectModelProtocol | list[DataObjectModelProtocol]:
        """
        Generates a valid instance of a `DataObjectModelProtocol` based on the contents from the provided path.

        Args:
            from_path (Path): Path containing data to be read (file or directory).

        Returns:
            DataObjectModelProtocol | list[DataObjectModelProtocol]: Either a single __valid__ instance of a `DataObjectModelProtocol` or a list of them.
        """
        pass
