
from configparser import ConfigParser

from koswat.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol


class EenheidsprijzenSection(KoswatIniFomProtocol):
    prijspeil: float

class KostenDijkprofielSection(KoswatIniFomProtocol):
    aanleg_graslaag_m3: float
    aanleg_kleilaag_m3: float
    aanleg_kern_m3: float
    hergebruik_graslaag_m3: float
    hergebruik_kern_m3: float
    afvoeren_materiaal_m3: float
    profileren_graslaag_m2: float
    profileren_kleilaag_m2: float
    profileren_kern_m2: float 
    bewerken_maaiveld_m2: float

class KostenInfrastructuurSection(KoswatIniFomProtocol):
    wegen_klasse2_verwijderen: float
    wegen_klasse24_verwijderen: float
    wegen_klasse47_verwijderen: float
    wegen_klasse7_verwijderen : float
    wegen_onbekend_verwijderen: float
    wegen_klasse2_aanleg: float
    wegen_klasse24_aanleg: float
    wegen_klasse47_aanleg: float
    wegen_klasse7_aanleg : float
    wegen_onbekend_aanleg: float
class KostenOpslagfactorenInclBTWSection(KoswatIniFomProtocol):
    grond_makkelijk :float
    grond_normaal :float
    grond_moeilijk :float
    constructief_makkelijk :float
    constructief_normaal :float
    constructief_moeilijk :float
    wegen_makkelijk :float
    wegen_normaal :float
    wegen_moeilijk :float
    grondaankoop_makkelijk :float
    grondaankoop_normaal :float
    grondaankoop_moeilijk :float
class KostenOpslagfactorenExclBTWSection(KoswatIniFomProtocol):
    grond_makkelijk: float
    grond_normaal: float
    grond_moeilijk: float
    constructief_makkelijk: float
    constructief_normaal: float
    constructief_moeilijk: float
    wegen_makkelijk: float
    wegen_normaal: float
    wegen_moeilijk: float
    grondaankoop_makkelijk: float
    grondaankoop_normaal: float
    grondaankoop_moeilijk: float
class KoswatCostsIniFom(KoswatIniFomProtocol):
    Eenheidsprijzen: EenheidsprijzenSection
    KostenDijkprofiel: KostenDijkprofielSection
    KostenInfrastructuur: KostenInfrastructuurSection
    KostenOpslagfactorenInclBTW: KostenOpslagfactorenInclBTWSection
    KostenOpslagfactorenExclBTW: KostenOpslagfactorenExclBTWSection 


    @classmethod
    def from_dict(cls, ini_dict: ConfigParser) -> KoswatIniFomProtocol:
        raise NotImplementedError()
    