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
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
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
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
        pleistoceen=-5,
        aquifer=-2,
    )

    infra = KoswatInputProfileBase(
        dike_section="test_data",
        buiten_maaiveld=0,
        buiten_talud=3,
        buiten_berm_hoogte=0,
        buiten_berm_breedte=0,
        kruin_hoogte=6,
        kruin_breedte=8,
        binnen_talud=3,
        binnen_berm_hoogte=0,
        binnen_berm_breedte=0,
        binnen_maaiveld=0,
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
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
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
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
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
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
        grondprijs_bebouwd=150,
        grondprijs_onbebouwd=10,
        factor_zetting=1.2,
        pleistoceen=-5,
        aquifer=-2,
    )
    
    profile_dijk4 = KoswatInputProfileBase(
        dike_section="dijk4",
        buiten_maaiveld=6.38,
        buiten_talud=2.56,
        buiten_berm_hoogte=6.38,
        buiten_berm_breedte=0,
        kruin_hoogte=11.38,
        kruin_breedte=10.36,
        binnen_talud=3.57,
        binnen_berm_hoogte=9.06,
        binnen_berm_breedte=19.23,
        binnen_maaiveld=6.45,
        grondprijs_bebouwd=322.63,
        grondprijs_onbebouwd=13.87,
        factor_zetting=1.2,
        pleistoceen=3.17,
        aquifer=6.06,
    )

    profile_dijk5 = KoswatInputProfileBase(
        dike_section="dijk5",
        buiten_maaiveld=7.64,
        buiten_talud=2.99,
        buiten_berm_hoogte=7.64,
        buiten_berm_breedte=0,
        kruin_hoogte=11.28,
        kruin_breedte=2.36,
        binnen_talud=2.03,
        binnen_berm_hoogte=10.69,
        binnen_berm_breedte=13.27,
        binnen_maaiveld=6.81,
        grondprijs_bebouwd=322.63,
        grondprijs_onbebouwd=13.87,
        factor_zetting=1.2,
        pleistoceen=3.53,
        aquifer=6.42,
    )
