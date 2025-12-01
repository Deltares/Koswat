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

from shapefile import _Record
from shapely.geometry import Point

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class KoswatDikeLocationsShpFom(FileObjectModelProtocol):
    initial_point: Point
    end_point: Point
    record: _Record

    @property
    def dike_section(self) -> str:
        if not self.record:
            return ""
        try:
            return self.record.Dijksectie
        except Exception:
            return self.record.Sectie

    @property
    def dike_traject(self) -> str:
        if not self.record:
            return ""
        return self.record.Traject

    @property
    def dike_subtraject(self) -> str:
        if not self.record:
            return ""
        try:
            return self.record.Subtraject
        except Exception:
            return self.record.VAK

    def __init__(self) -> None:
        self.initial_point = None
        self.end_point = None
        self.record = None

    def is_valid(self) -> bool:
        if not self.initial_point or not self.end_point:
            return False
        return self.initial_point.is_valid and self.end_point.is_valid
