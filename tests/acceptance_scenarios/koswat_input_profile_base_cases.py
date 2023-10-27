import pytest

from koswat.dike.profile.koswat_input_profile_base import KoswatInputProfileBase
from tests.acceptance_scenarios.cases_protocol import CasesProtocol


class InputProfileCases(CasesProtocol):
    default = KoswatInputProfileBase(
        dike_section="test_data",
        buiten_maaiveld=0,
        buiten_talud=3,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=5,
        binnen_talud=3,
        binnen_berm_hoogte=0,
        binnen_berm_breedte=0,
        binnen_maaiveld=0,
        pleistoceen=-5,
        aquifer=-2,
    )

    profile_case_2 = KoswatInputProfileBase(
        dike_section="test_data",
        buiten_maaiveld=0,
        buiten_talud=4,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6.5,
        kruin_breedte=5,
        binnen_talud=5.54,
        binnen_berm_hoogte=2.6,
        binnen_berm_breedte=54,
        binnen_maaiveld=0,
        pleistoceen=-5,
        aquifer=-2,
    )

    cases = [pytest.param(default, id="Default Input Profile")]


class AcceptanceTestInputProfileCases(CasesProtocol):
    profile_dijk1 = KoswatInputProfileBase(
        dike_section="dijk1",
        buiten_maaiveld=0,
        buiten_talud=3,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=5,
        binnen_talud=3,
        binnen_berm_hoogte=0,
        binnen_berm_breedte=0,
        binnen_maaiveld=0,
        pleistoceen=-5,
        aquifer=-2,
    )

    profile_dijk2 = KoswatInputProfileBase(
        dike_section="dijk2",
        buiten_maaiveld=-2,
        buiten_talud=3,
        buiten_berm_hoogte=-2,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=5,
        binnen_talud=3,
        binnen_berm_hoogte=0,
        binnen_berm_breedte=0,
        binnen_maaiveld=0,
        pleistoceen=-5,
        aquifer=-2,
    )

    profile_dijk3 = KoswatInputProfileBase(
        dike_section="dijk3",
        buiten_maaiveld=0,
        buiten_talud=3,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=5,
        binnen_talud=3,
        binnen_berm_hoogte=-2,
        binnen_berm_breedte=0,
        binnen_maaiveld=-2,
        pleistoceen=-5,
        aquifer=-2,
    )
