"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2025 Stichting Deltares

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Any

from koswat.configuration.io.config_sections.config_section_helper import (
    SectionConfigHelper,
)
from koswat.core.io.json.koswat_json_fom_protocol import KoswatJsonFomProtocol


class UnitPricesSectionFom(KoswatJsonFomProtocol):
    price_level: float

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "UnitPricesSectionFom":
        _section = cls()
        _section.price_level = int(input_config["prijspeil"])
        return _section


class DikeProfileCostsSectionFom(KoswatJsonFomProtocol):
    construction_grass_layer_m3: float
    construction_clay_layer_m3: float
    construction_core_m3: float
    reuse_grass_layer_m3: float
    reuse_core_m3: float
    dispose_material_m3: float
    profile_grass_layer_m2: float
    profile_clay_layer_m2: float
    profile_core_m2: float
    process_ground_level_surface_m2: float

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "DikeProfileCostsSectionFom":
        _section = cls()
        _section.construction_grass_layer_m3 = SectionConfigHelper.get_float(
            input_config["aanleg_graslaag_m3"]
        )
        _section.construction_clay_layer_m3 = SectionConfigHelper.get_float(
            input_config["aanleg_kleilaag_m3"]
        )
        _section.construction_core_m3 = SectionConfigHelper.get_float(
            input_config["aanleg_kern_m3"]
        )
        _section.reuse_grass_layer_m3 = SectionConfigHelper.get_float(
            input_config["hergebruik_graslaag_m3"]
        )
        _section.reuse_core_m3 = SectionConfigHelper.get_float(
            input_config["hergebruik_kern_m3"]
        )
        _section.dispose_material_m3 = SectionConfigHelper.get_float(
            input_config["afvoeren_materiaal_m3"]
        )
        _section.profile_grass_layer_m2 = SectionConfigHelper.get_float(
            input_config["profileren_graslaag_m2"]
        )
        _section.profile_clay_layer_m2 = SectionConfigHelper.get_float(
            input_config["profileren_kleilaag_m2"]
        )
        _section.profile_core_m2 = SectionConfigHelper.get_float(
            input_config["profileren_kern_m2"]
        )
        _section.process_ground_level_surface_m2 = SectionConfigHelper.get_float(
            input_config["bewerken_maaiveld_m2"]
        )
        return _section


class InfrastructureCostsSectionFom(KoswatJsonFomProtocol):
    roads_class2_removal: float
    roads_class24_removal: float
    roads_class47_removal: float
    roads_class7_removal: float
    roads_unknown_removal: float
    roads_class2_construction: float
    roads_class24_construction: float
    roads_class47_construction: float
    roads_class7_construction: float
    roads_unknown_construction: float

    @classmethod
    def from_config(
        cls, input_config: dict[str, Any]
    ) -> "InfrastructureCostsSectionFom":
        _section = cls()
        _section.roads_class2_removal = SectionConfigHelper.get_float(
            input_config["wegen_klasse2_verwijderen"]
        )
        _section.roads_class24_removal = SectionConfigHelper.get_float(
            input_config["wegen_klasse24_verwijderen"]
        )
        _section.roads_class47_removal = SectionConfigHelper.get_float(
            input_config["wegen_klasse47_verwijderen"]
        )
        _section.roads_class7_removal = SectionConfigHelper.get_float(
            input_config["wegen_klasse7_verwijderen"]
        )
        _section.roads_unknown_removal = SectionConfigHelper.get_float(
            input_config["wegen_onbekend_verwijderen"]
        )
        _section.roads_class2_construction = SectionConfigHelper.get_float(
            input_config["wegen_klasse2_aanleg"]
        )
        _section.roads_class24_construction = SectionConfigHelper.get_float(
            input_config["wegen_klasse24_aanleg"]
        )
        _section.roads_class47_construction = SectionConfigHelper.get_float(
            input_config["wegen_klasse47_aanleg"]
        )
        _section.roads_class7_construction = SectionConfigHelper.get_float(
            input_config["wegen_klasse7_aanleg"]
        )
        _section.roads_unknown_construction = SectionConfigHelper.get_float(
            input_config["wegen_onbekend_aanleg"]
        )
        return _section


class SurtaxCostsSectionFom(KoswatJsonFomProtocol):
    soil_easy: float
    soil_normal: float
    soil_hard: float
    constructive_easy: float
    constructive_normal: float
    constructive_hard: float
    road_easy: float
    roads_normal: float
    roads_hard: float
    land_purchase_easy: float
    land_purchase_normal: float
    land_purchase_hard: float

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "SurtaxCostsSectionFom":
        _section = cls()
        _section.soil_easy = SectionConfigHelper.get_float(
            input_config["grond_makkelijk"]
        )
        _section.soil_normal = SectionConfigHelper.get_float(
            input_config["grond_normaal"]
        )
        _section.soil_hard = SectionConfigHelper.get_float(
            input_config["grond_moeilijk"]
        )
        _section.constructive_easy = SectionConfigHelper.get_float(
            input_config["constructief_makkelijk"]
        )
        _section.constructive_normal = SectionConfigHelper.get_float(
            input_config["constructief_normaal"]
        )
        _section.constructive_hard = SectionConfigHelper.get_float(
            input_config["constructief_moeilijk"]
        )
        _section.road_easy = SectionConfigHelper.get_float(
            input_config["wegen_makkelijk"]
        )
        _section.roads_normal = SectionConfigHelper.get_float(
            input_config["wegen_normaal"]
        )
        _section.roads_hard = SectionConfigHelper.get_float(
            input_config["wegen_moeilijk"]
        )
        _section.land_purchase_easy = SectionConfigHelper.get_float(
            input_config["grondaankoop_makkelijk"]
        )
        _section.land_purchase_normal = SectionConfigHelper.get_float(
            input_config["grondaankoop_normaal"]
        )
        _section.land_purchase_hard = SectionConfigHelper.get_float(
            input_config["grondaankoop_moeilijk"]
        )
        return _section


class ConstructionCostsSectionFom(KoswatJsonFomProtocol):
    c_factor: float
    d_factor: float
    z_factor: float
    f_factor: float
    g_factor: float

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "ConstructionCostsSectionFom":
        _section = cls()
        _section.c_factor = SectionConfigHelper.get_float(input_config["c"])
        _section.d_factor = SectionConfigHelper.get_float(input_config["d"])
        _section.z_factor = SectionConfigHelper.get_float(input_config["z"])
        _section.f_factor = SectionConfigHelper.get_float(input_config["f"])
        _section.g_factor = SectionConfigHelper.get_float(input_config["g"])
        return _section


class KoswatCostsJsonFom(KoswatJsonFomProtocol):
    unit_prices_section: UnitPricesSectionFom
    dike_profile_costs_section: DikeProfileCostsSectionFom
    infrastructure_costs_section: InfrastructureCostsSectionFom
    surtax_costs_incl_tax_section: SurtaxCostsSectionFom
    surtax_costs_excl_tax_section: SurtaxCostsSectionFom
    construction_cost_cb_wall: ConstructionCostsSectionFom
    construction_cost_vzg: ConstructionCostsSectionFom
    construction_cost_sheetpile_unanchored: ConstructionCostsSectionFom
    construction_cost_sheetpile_anchored: ConstructionCostsSectionFom
    construction_cost_diaphragm_wall: ConstructionCostsSectionFom
    construction_cost_cofferdam: ConstructionCostsSectionFom

    @classmethod
    def from_config(cls, input_config: dict[str, Any]) -> "KoswatCostsJsonFom":
        _costs_fom = cls()
        _costs_fom.unit_prices_section = UnitPricesSectionFom.from_config(
            input_config["eenheidsprijzen"]
        )
        _costs_fom.dike_profile_costs_section = DikeProfileCostsSectionFom.from_config(
            input_config["kostendijkprofiel"]
        )
        _costs_fom.infrastructure_costs_section = (
            InfrastructureCostsSectionFom.from_config(
                input_config["kosteninfrastructuur"]
            )
        )
        _costs_fom.surtax_costs_incl_tax_section = SurtaxCostsSectionFom.from_config(
            input_config["kostenopslagfactoreninclbtw"]
        )
        _costs_fom.surtax_costs_excl_tax_section = SurtaxCostsSectionFom.from_config(
            input_config["kostenopslagfactorenexclbtw"]
        )
        _costs_fom.construction_cost_vzg = ConstructionCostsSectionFom.from_config(
            input_config["kostenverticaalzanddichtgeotextiel"]
        )
        _costs_fom.construction_cost_cb_wall = ConstructionCostsSectionFom.from_config(
            input_config["kostencbwand"]
        )
        _costs_fom.construction_cost_sheetpile_unanchored = (
            ConstructionCostsSectionFom.from_config(
                input_config["kostendamwandonverankerd"]
            )
        )
        _costs_fom.construction_cost_sheetpile_anchored = (
            ConstructionCostsSectionFom.from_config(
                input_config["kostendamwandverankerd"]
            )
        )
        _costs_fom.construction_cost_diaphragm_wall = (
            ConstructionCostsSectionFom.from_config(input_config["kostendiepwand"])
        )
        _costs_fom.construction_cost_cofferdam = (
            ConstructionCostsSectionFom.from_config(input_config["kostenkistdam"])
        )
        return _costs_fom
