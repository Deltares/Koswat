from configparser import SectionProxy

from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol
from koswat.core.io.ini.koswat_ini_fom_protocol import KoswatIniFomProtocol
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


class DikeProfileSectionFom(KoswatIniFomProtocol, KoswatJsonFomProtocol):
    thickness_grass_layer: float
    thickness_clay_layer: float

    @classmethod
    def from_ini(cls, ini_config: SectionProxy) -> FileObjectModelProtocol:
        _section = cls()
        _section.thickness_grass_layer = ini_config.getfloat("dikte_graslaag")
        _section.thickness_clay_layer = ini_config.getfloat("dikte_kleilaag")
        return _section
