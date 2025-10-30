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
