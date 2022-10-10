from __future__ import annotations

from typing import Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class KoswatInputProfileProtocol(Protocol):
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

    @classmethod
    def from_dict(cls, profile_data: dict) -> KoswatInputProfileProtocol:
        """
        Generates a `KoswatInputProfileProtocol` with the given profile data.

        Returns:
            KoswatInputProfileProtocol: Initialized instance of `KoswatInputProfileProtocol`.
        """
        pass
