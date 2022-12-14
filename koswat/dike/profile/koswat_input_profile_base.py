from __future__ import annotations

from koswat.dike.koswat_input_profile_protocol import KoswatInputProfileProtocol


class KoswatInputProfileBase(KoswatInputProfileProtocol):
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
