from __future__ import annotations

from typing import Protocol, runtime_checkable

from koswat.core.protocols.data_object_model_protocol import DataObjectModelProtocol


@runtime_checkable
class KoswatInputProfileProtocol(DataObjectModelProtocol, Protocol):
    dike_section: str
    buiten_maaiveld: float
    buiten_talud: float
    buiten_berm_hoogte: float
    buiten_berm_breedte: float
    kruin_hoogte: float
    kruin_breedte: float
    binnen_talud: float
    binnen_berm_hoogte: float
    binnen_berm_breedte: float
    binnen_maaiveld: float
    pleistoceen: float
    aquifer: float
