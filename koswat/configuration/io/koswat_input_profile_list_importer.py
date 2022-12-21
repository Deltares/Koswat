from pathlib import Path
from typing import List

from koswat.configuration.io.csv.koswat_input_profiles_csv_fom_builder import (
    KoswatProfileInputCsvFomBuilder,
)
from koswat.core.io.csv.koswat_csv_reader import KoswatCsvReader
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
        return _input_profile

    def import_from(self, from_path: Path) -> List[KoswatInputProfileBase]:
        _profile_input_list = KoswatCsvReader.with_builder_type(
            KoswatProfileInputCsvFomBuilder
        ).read(from_path)
        return list(
            map(
                self._get_koswat_input_profile_base,
                _profile_input_list.input_profile_fom_list,
            )
        )
