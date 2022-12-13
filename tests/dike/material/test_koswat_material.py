import math
from typing import Callable

import pytest

from koswat.dike.material.koswat_material import (
    KoswatMaterialFactory,
    KoswatMaterialType,
)


class TestKoswatMaterialFactory:
    def test_given_invalid_material_name_raises(self):
        _invalid_material = "water"
        with pytest.raises(ValueError) as exc_info:
            KoswatMaterialFactory.get_material(_invalid_material)

        assert (
            str(exc_info.value)
            == f"No information available for material {_invalid_material}"
        )

    @pytest.mark.parametrize("material_name", ["zand", "KLEI", " gRaS "])
    @pytest.mark.parametrize(
        "modify_name",
        [
            pytest.param(lambda x: x, id="As given"),
            pytest.param(lambda x: x.upper(), id="Uppercase"),
            pytest.param(lambda x: x.lower(), id="Lowercase"),
            pytest.param(lambda x: x.capitalize(), id="Capitalize"),
            pytest.param(lambda x: x.capitalize().swapcase(), id="Swapcase"),
        ],
    )
    def test_given_valid_material_name_returns_material(
        self, material_name: str, modify_name: Callable
    ):
        # 1. Define test data.
        _m_name = modify_name(material_name)

        # 2. Run test.
        _material = KoswatMaterialFactory.get_material(_m_name)

        # 3. Verify expectations.
        assert isinstance(_material, KoswatMaterialType)
        assert _material.name.lower() == material_name.lower().strip()
        assert not math.isnan(_material.cost)
