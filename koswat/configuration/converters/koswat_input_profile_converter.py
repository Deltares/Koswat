from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom import (
    KoswatInputProfilesCsvFom,
)
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class KoswatInputProfileConverter:
    @staticmethod
    def fom_to_dom(
        input_profile_fom: KoswatInputProfilesCsvFom,
    ) -> List[KoswatInputProfileBase]:
        _dom_list = []
        for _csv_fom in input_profile_fom.input_profile_fom_list:
            _input_profile = KoswatInputProfileBase()
            _input_profile.dike_section = _csv_fom.get("dikesection", "")
            _input_profile.buiten_maaiveld = _csv_fom["buiten_maaiveld"]
            _input_profile.buiten_talud = _csv_fom["buiten_talud"]
            _input_profile.buiten_berm_hoogte = _csv_fom["buiten_berm_hoogte"]
            _input_profile.buiten_berm_breedte = _csv_fom["buiten_berm_lengte"]  #
            _input_profile.kruin_hoogte = _csv_fom["kruin_hoogte"]
            _input_profile.kruin_breedte = _csv_fom["kruin_breedte"]
            _input_profile.binnen_talud = _csv_fom["binnen_talud"]
            _input_profile.binnen_berm_hoogte = _csv_fom["binnen_berm_hoogte"]
            _input_profile.binnen_berm_breedte = _csv_fom["binnen_berm_lengte"]  #
            _input_profile.binnen_maaiveld = _csv_fom["binnen_maaiveld"]
            _dom_list.append(_input_profile)
        return _dom_list
