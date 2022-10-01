class ScenarioCases:
    default = dict(
        d_h=1,
        d_s=10,
        d_p=30,
        kruin_breedte=5,
        buiten_talud=3,
    )


class LayersCases:
    without_layers = dict(
        base_layer=dict(material="zand"),
        coating_layers=[],
    )
    with_clay = dict(
        base_layer=dict(material="zand"),
        coating_layers=[
            dict(material="klei", depth=4.2),
        ],
    )


class InputProfileCases:
    default = dict(
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
    )
