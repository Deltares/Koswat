import logging
from dataclasses import dataclass, field
from pathlib import Path

from koswat.configuration.io.json.koswat_input_profile_json_reader import (
    KoswatInputProfileJsonReader,
)
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol
from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase


@dataclass(kw_only=True)
class KoswatInputProfileListImporter(KoswatImporterProtocol):
    dike_selection: list[str] = field(default_factory=list)

    def _get_koswat_input_profile_base(
        self, fom_dict: dict[str, str | float]
    ) -> KoswatInputProfileBase:
        _input_profile = KoswatInputProfileBase()
        _input_profile.dike_section = fom_dict["dijksectie"]
        _input_profile.waterside_ground_level = float(fom_dict["buiten_maaiveld"])
        _input_profile.waterside_slope = float(fom_dict["buiten_talud"])
        _input_profile.waterside_berm_height = float(fom_dict["buiten_berm_hoogte"])
        _input_profile.waterside_berm_width = float(fom_dict["buiten_berm_lengte"])
        _input_profile.crest_height = float(fom_dict["kruin_hoogte"])
        _input_profile.crest_width = float(fom_dict["kruin_breedte"])
        _input_profile.polderside_slope = float(fom_dict["binnen_talud"])
        _input_profile.polderside_berm_height = float(fom_dict["binnen_berm_hoogte"])
        _input_profile.polderside_berm_width = float(fom_dict["binnen_berm_lengte"])
        _input_profile.polderside_ground_level = float(fom_dict["binnen_maaiveld"])
        _input_profile.ground_price_builtup = float(fom_dict["grondprijs_bebouwd"])
        _input_profile.ground_price_unbuilt = float(fom_dict["grondprijs_onbebouwd"])
        _input_profile.factor_settlement = float(fom_dict["factorzetting"])
        _input_profile.pleistocene = float(fom_dict["pleistoceen"])
        _input_profile.aquifer = float(fom_dict["aquifer"])
        _input_profile.top_layer_thickness = float(fom_dict["dikte_deklaag"])
        return _input_profile

    def import_from(self, from_path: Path) -> list[KoswatInputProfileBase]:
        _files = list(from_path.glob("*.json"))

        _profile_input_list = []
        for _section in self.dike_selection if self.dike_selection else []:
            if _section not in (_file.stem for _file in _files):
                logging.error(
                    "The selected dike section %s was not found in the input profile files.",
                    _section,
                )

            _file = from_path.joinpath(f"{_section}.json")
            if not _file.exists():
                continue

            _profile_input = KoswatInputProfileJsonReader().read(_file)
            _profile_input_list.append(
                self._get_koswat_input_profile_base(_profile_input.input_profile_fom)
            )

        return _profile_input_list
