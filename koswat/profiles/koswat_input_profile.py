from __future__ import annotations

from koswat.profiles.characteristic_points import CharacteristicPoints


class KoswatInputProfile:
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

    characteristic_points: CharacteristicPoints

    @classmethod
    def from_dict(cls, profile_data: dict) -> KoswatInputProfile:
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
        _input_profile.characteristic_points = CharacteristicPoints.from_tuple_list(
            profile_data.get("characteristic_points", [])
        )
        return _input_profile
