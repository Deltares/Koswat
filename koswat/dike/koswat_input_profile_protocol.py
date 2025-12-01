"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

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

from typing import Protocol, runtime_checkable

from koswat.core.protocols.data_object_model_protocol import DataObjectModelProtocol


@runtime_checkable
class KoswatInputProfileProtocol(DataObjectModelProtocol, Protocol):
    dike_section: str
    waterside_ground_level: float
    waterside_slope: float
    waterside_berm_height: float
    waterside_berm_width: float
    crest_height: float
    crest_width: float
    polderside_slope: float
    polderside_berm_height: float
    polderside_berm_width: float
    polderside_ground_level: float
    ground_price_builtup: float
    ground_price_unbuilt: float
    factor_settlement: float
    pleistocene: float
    aquifer: float

    @property
    def ground_price(self) -> float:
        pass
