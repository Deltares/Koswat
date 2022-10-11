from __future__ import annotations

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class PipingWallInputProfile(KoswatInputProfileBase):
    length_piping_wall: float

    @classmethod
    def from_dict(cls, profile_data: dict) -> PipingWallInputProfile:
        _input_profile = cls()
        _input_profile.buiten_maaiveld = profile_data["buiten_maaiveld"]
        _input_profile.buiten_talud = profile_data["buiten_talud"]
        _input_profile.buiten_berm_hoogte = profile_data["buiten_berm_hoogte"]
        _input_profile.buiten_berm_breedte = profile_data["buiten_berm_breedte"]
        _input_profile.kruin_hoogte = profile_data["kruin_hoogte"]
        _input_profile.kruin_breedte = profile_data["kruin_breedte"]
        _input_profile.binnen_talud = profile_data["binnen_talud"]
        _input_profile.binnen_berm_hoogte = profile_data["binnen_berm_hoogte"]
        _input_profile.binnen_berm_breedte = profile_data["binnen_berm_breedte"]
        _input_profile.binnen_maaiveld = profile_data["binnen_maaiveld"]
        _input_profile.length_piping_wall = profile_data["length_piping_wall"]
        return _input_profile
