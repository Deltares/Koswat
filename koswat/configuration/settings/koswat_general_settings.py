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
    CB_DAMWAND = 0
    DAMWAND_ONVERANKERD = 1
    DAMWAND_VERANKERD = 2
    DIEPWAND = 3
    KISTDAM = 4
