from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_reader import (
    KoswatInputProfilesCsvReader,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


class KoswatInputProfileListImporter(KoswatImporterProtocol):
    def _get_koswat_input_profile_base(self, fom_dict: dict) -> KoswatInputProfileBase:
        _input_profile = KoswatInputProfileBase()
        _input_profile.dike_section = fom_dict["dijksectie"]
        _input_profile.buiten_maaiveld = float(fom_dict["buiten_maaiveld"])
        _input_profile.buiten_talud = float(fom_dict["buiten_talud"])
        _input_profile.buiten_berm_hoogte = float(fom_dict["buiten_berm_hoogte"])
        _input_profile.buiten_berm_breedte = float(fom_dict["buiten_berm_lengte"])
        _input_profile.kruin_hoogte = float(fom_dict["kruin_hoogte"])
        _input_profile.kruin_breedte = float(fom_dict["kruin_breedte"])
        _input_profile.binnen_talud = float(fom_dict["binnen_talud"])
        _input_profile.binnen_berm_hoogte = float(fom_dict["binnen_berm_hoogte"])
        _input_profile.binnen_berm_breedte = float(fom_dict["binnen_berm_lengte"])
        _input_profile.binnen_maaiveld = float(fom_dict["binnen_maaiveld"])
        _input_profile.grondprijs_bebouwd = float(fom_dict["grondprijs_bebouwd"])
        _input_profile.grondprijs_onbebouwd = float(fom_dict["grondprijs_onbebouwd"])
        _input_profile.factor_zetting = float(fom_dict["factorzetting"])
        _input_profile.pleistoceen = float(fom_dict["pleistoceen"])
        _input_profile.aquifer = float(fom_dict["aquifer"])
        return _input_profile

    def import_from(self, from_path: Path) -> List[KoswatInputProfileBase]:
        _profile_input_list = KoswatInputProfilesCsvReader().read(from_path)
        return list(
            map(
                self._get_koswat_input_profile_base,
                _profile_input_list.input_profile_fom_list,
            )
        )
