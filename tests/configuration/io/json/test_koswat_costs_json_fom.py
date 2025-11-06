from koswat.configuration.io.json.koswat_costs_json_fom import (
    ConstructionCostsSectionFom,
    DikeProfileCostsSectionFom,
    InfrastructureCostsSectionFom,
    KoswatCostsJsonFom,
    SurtaxCostsSectionFom,
    UnitPricesSectionFom,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from tests import test_data


class TestKoswatCostsJsonFom:
    def test_from_config(self):
        # 1. Define test data.
        _test_file_path = test_data.joinpath("json_reader", "koswat_costs.json")
        _config_reader = KoswatJsonReader()

        # 2. Run test
        _json_fom = _config_reader.read(_test_file_path)
        _config_fom = KoswatCostsJsonFom.from_config(_json_fom.content)

        # 3. Validate expectations.
        assert isinstance(_config_fom, KoswatCostsJsonFom)

        # Eenheidsprijzen
        assert isinstance(_config_fom.unit_prices_section, UnitPricesSectionFom)
        assert _config_fom.unit_prices_section.price_level == 2017

        # KostenDijkProfiel
        assert isinstance(
            _config_fom.dike_profile_costs_section, DikeProfileCostsSectionFom
        )
        assert (
            _config_fom.dike_profile_costs_section.construction_grass_layer_m3 == 12.44
        )
        assert (
            _config_fom.dike_profile_costs_section.construction_clay_layer_m3 == 18.05
        )
        assert _config_fom.dike_profile_costs_section.construction_core_m3 == 10.98
        assert _config_fom.dike_profile_costs_section.reuse_grass_layer_m3 == 6.04
        assert _config_fom.dike_profile_costs_section.reuse_core_m3 == 4.67
        assert _config_fom.dike_profile_costs_section.dispose_material_m3 == 7.07
        assert _config_fom.dike_profile_costs_section.profile_grass_layer_m2 == 0.88
        assert _config_fom.dike_profile_costs_section.profile_clay_layer_m2 == 0.65
        assert _config_fom.dike_profile_costs_section.profile_core_m2 == 0.60
        assert (
            _config_fom.dike_profile_costs_section.process_ground_level_surface_m2
            == 0.25
        )

        # KostenInfrastructuur
        assert isinstance(
            _config_fom.infrastructure_costs_section, InfrastructureCostsSectionFom
        )
        assert _config_fom.infrastructure_costs_section.roads_class2_removal == 7.40
        assert _config_fom.infrastructure_costs_section.roads_class24_removal == 9.64
        assert _config_fom.infrastructure_costs_section.roads_class47_removal == 23.99
        assert _config_fom.infrastructure_costs_section.roads_class7_removal == 38.77
        assert _config_fom.infrastructure_costs_section.roads_unknown_removal == 9.64
        assert (
            _config_fom.infrastructure_costs_section.roads_class2_construction == 24.31
        )
        assert (
            _config_fom.infrastructure_costs_section.roads_class24_construction == 32.30
        )
        assert (
            _config_fom.infrastructure_costs_section.roads_class47_construction == 31.85
        )
        assert (
            _config_fom.infrastructure_costs_section.roads_class7_construction == 36.64
        )
        assert (
            _config_fom.infrastructure_costs_section.roads_unknown_construction == 32.30
        )

        # KostenOpslagFactorenInclBTW
        assert isinstance(
            _config_fom.surtax_costs_incl_tax_section,
            SurtaxCostsSectionFom,
        )
        assert _config_fom.surtax_costs_incl_tax_section.soil_easy == 1.714
        assert _config_fom.surtax_costs_incl_tax_section.soil_normal == 1.953
        assert _config_fom.surtax_costs_incl_tax_section.soil_hard == 2.177
        assert _config_fom.surtax_costs_incl_tax_section.constructive_easy == 2.097
        assert _config_fom.surtax_costs_incl_tax_section.constructive_normal == 2.413
        assert _config_fom.surtax_costs_incl_tax_section.constructive_hard == 2.690
        assert _config_fom.surtax_costs_incl_tax_section.road_easy == 2.097
        assert _config_fom.surtax_costs_incl_tax_section.roads_normal == 2.413
        assert _config_fom.surtax_costs_incl_tax_section.roads_hard == 2.690
        assert _config_fom.surtax_costs_incl_tax_section.land_purchase_easy == 1.292
        assert _config_fom.surtax_costs_incl_tax_section.land_purchase_normal == 1.412
        assert _config_fom.surtax_costs_incl_tax_section.land_purchase_hard == 1.645

        # KostenOpslagFactorenExclBTW
        assert isinstance(
            _config_fom.surtax_costs_excl_tax_section,
            SurtaxCostsSectionFom,
        )
        assert _config_fom.surtax_costs_excl_tax_section.soil_easy == 1.421
        assert _config_fom.surtax_costs_excl_tax_section.soil_normal == 1.621
        assert _config_fom.surtax_costs_excl_tax_section.soil_hard == 1.810
        assert _config_fom.surtax_costs_excl_tax_section.constructive_easy == 1.741
        assert _config_fom.surtax_costs_excl_tax_section.constructive_normal == 2.003
        assert _config_fom.surtax_costs_excl_tax_section.constructive_hard == 2.233
        assert _config_fom.surtax_costs_excl_tax_section.road_easy == 1.741
        assert _config_fom.surtax_costs_excl_tax_section.roads_normal == 2.003
        assert _config_fom.surtax_costs_excl_tax_section.roads_hard == 2.233
        assert _config_fom.surtax_costs_excl_tax_section.land_purchase_easy == 1.292
        assert _config_fom.surtax_costs_excl_tax_section.land_purchase_normal == 1.412
        assert _config_fom.surtax_costs_excl_tax_section.land_purchase_hard == 1.645

        # KostenCBwand
        assert isinstance(
            _config_fom.construction_cost_cb_wall,
            ConstructionCostsSectionFom,
        )
        assert _config_fom.construction_cost_cb_wall.c_factor == 0
        assert _config_fom.construction_cost_cb_wall.d_factor == 159.326
        assert _config_fom.construction_cost_cb_wall.z_factor == -34.794
        assert _config_fom.construction_cost_cb_wall.f_factor == 0
        assert _config_fom.construction_cost_cb_wall.g_factor == 0

        # KostenDamwandOnverankerd
        assert isinstance(
            _config_fom.construction_cost_sheetpile_unanchored,
            ConstructionCostsSectionFom,
        )
        assert _config_fom.construction_cost_sheetpile_unanchored.c_factor == 9.298
        assert _config_fom.construction_cost_sheetpile_unanchored.d_factor == 132.239
        assert _config_fom.construction_cost_sheetpile_unanchored.z_factor == 103.628
        assert _config_fom.construction_cost_sheetpile_unanchored.f_factor == 0
        assert _config_fom.construction_cost_sheetpile_unanchored.g_factor == 0

        # KostenDamwandVerankerd
        assert isinstance(
            _config_fom.construction_cost_sheetpile_anchored,
            ConstructionCostsSectionFom,
        )
        assert _config_fom.construction_cost_sheetpile_anchored.c_factor == 9.298
        assert _config_fom.construction_cost_sheetpile_anchored.d_factor == 150.449
        assert _config_fom.construction_cost_sheetpile_anchored.z_factor == 1304.455
        assert _config_fom.construction_cost_sheetpile_anchored.f_factor == 0
        assert _config_fom.construction_cost_sheetpile_anchored.g_factor == 0

        # KostenDiepwand
        assert isinstance(
            _config_fom.construction_cost_diaphragm_wall,
            ConstructionCostsSectionFom,
        )
        assert _config_fom.construction_cost_diaphragm_wall.c_factor == 0
        assert _config_fom.construction_cost_diaphragm_wall.d_factor == 0
        assert _config_fom.construction_cost_diaphragm_wall.z_factor == 0
        assert _config_fom.construction_cost_diaphragm_wall.f_factor == 281.176
        assert _config_fom.construction_cost_diaphragm_wall.g_factor == 1.205

        # KostenKistdam
        assert isinstance(
            _config_fom.construction_cost_cofferdam,
            ConstructionCostsSectionFom,
        )
        assert _config_fom.construction_cost_cofferdam.c_factor == 0
        assert _config_fom.construction_cost_cofferdam.d_factor == 680.782
        assert _config_fom.construction_cost_cofferdam.z_factor == -74.602
        assert _config_fom.construction_cost_cofferdam.f_factor == 0
        assert _config_fom.construction_cost_cofferdam.g_factor == 0
