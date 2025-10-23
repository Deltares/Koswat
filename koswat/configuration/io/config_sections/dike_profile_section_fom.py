from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)


class DikeProfileSectionFom(ConfigSectionFomBase):
    dike_section: str = ""
    thickness_grass_layer: float
    thickness_clay_layer: float

    _float_mappings = dict(
        dikte_graslaag="thickness_grass_layer",
        dikte_kleilaag="thickness_clay_layer",
    )
    _surtax_mappings = dict()
