import re
from typing import Dict

from koswat.builder_protocol import BuilderProtocol
from koswat.io.ini.koswat_ini_analysis_fom import KoswatIniAnalysisFom


class KoswatIniAnalysisFomBuilder(BuilderProtocol):
    section = Dict[str, str]

    def __init__(self) -> None:
        self.section = []

    def _is_valid(self) -> bool:
        if not self.section:
            return False
        # TODO consider lenght test on dict?
        return True

    def build(self) -> KoswatIniAnalysisFom:
        if not self._is_valid():
            raise ValueError("Not valid input.")
        # First three columns are section x and y coordinate.
        self.section.setdefault("")
        _koswat_fom = KoswatIniAnalysisFom()
        _koswat_fom.dijksectiesSelectie = self.section.get("Dijksecties_Selectie")
        _koswat_fom.dijksectieLigging = self.section.get("Dijksectie_Ligging")
        _koswat_fom.dijksectieInvoer = self.section.get("Dijksectie_Invoer")
        _koswat_fom.scenarioInvoer = self.section.get("Scenario_Invoer")
        _koswat_fom.eenheidsprijzen = self.section.get("Eenheidsprijzen")
        _koswat_fom.uitvoerfolder = self.section.get("Uitvoerfolder")
        bool_string = self.section.get("BTW")
        if bool_string == "True":
            _koswat_fom.BTW = True
        if bool_string == "False":
            _koswat_fom.BTW = False

        return _koswat_fom
