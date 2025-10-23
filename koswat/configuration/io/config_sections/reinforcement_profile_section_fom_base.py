import abc
import math
from configparser import SectionProxy
from typing import Optional

from koswat.configuration.io.config_sections.config_section_fom_base import (
    ConfigSectionFomBase,
)
from koswat.configuration.settings.koswat_general_settings import SurtaxFactorEnum
from koswat.core.io.file_object_model_protocol import FileObjectModelProtocol


class ReinforcementProfileSectionFomBase(ConfigSectionFomBase, abc.ABC):
    soil_surtax_factor: SurtaxFactorEnum
