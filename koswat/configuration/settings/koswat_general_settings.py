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
    VZG = 1
    CB_DAMWAND = 2
    DAMWAND_ONVERANKERD = 3
    DAMWAND_VERANKERD = 4
    DIEPWAND = 5
    KISTDAM = 6
