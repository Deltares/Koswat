from koswat.configuration.koswat_scenario import KoswatScenario

default_case = KoswatScenario.from_dict(
    dict(
        d_h=1,
        d_s=10,
        d_p=30,
        kruin_breedte=5,
        buiten_talud=3,
    )
)
