from __future__ import annotations

import enum


class SurtaxFactorEnum(enum.Enum):
    MAKKELIJK = 0
    NORMAAL = 1
    MOEILIJK = 2


class InfraCostsEnum(enum.Enum):
    GEEN = 0
    HERSTEL = 1
    VERVANG = 2


class ConstructionTypeEnum(enum.Enum):
    VZG = 0
    CB_DAMWAND = 1
    DAMWAND_ONVERANKERD = 2
    DAMWAND_VERANKERD = 3
    DIEPWAND = 4
    KISTDAM = 5
