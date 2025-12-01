"""
                    GNU GENERAL PUBLIC LICENSE
                      Version 3, 29 June 2007

    KOSWAT, from the dutch combination of words `Kosts-Wat` (what are the costs)
    Copyright (C) 2024 Stichting Deltares

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

from __future__ import annotations

import logging
from pathlib import Path

from koswat.configuration.io.json.koswat_costs_json_fom import (
    ConstructionCostsSectionFom,
    KoswatCostsJsonFom,
)
from koswat.configuration.settings.costs.construction_costs_settings import (
    ConstructionFactors,
)
from koswat.configuration.settings.costs.koswat_costs_settings import (
    ConstructionCostsSettings,
    DikeProfileCostsSettings,
    InfrastructureCostsSettings,
    KoswatCostsSettings,
    SurtaxCostsSettings,
)
from koswat.core.io.json.koswat_json_reader import KoswatJsonReader
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol


class KoswatCostsImporter(KoswatImporterProtocol):
    include_taxes: bool

    def __init__(self) -> None:
        self.include_taxes = None

    def _get_costs_fom(self, config_file: Path) -> KoswatCostsJsonFom:
        reader = KoswatJsonReader()
        _json_fom = reader.read(config_file)
        return KoswatCostsJsonFom.from_config(_json_fom.content)

    def import_from(self, from_path: Path) -> KoswatCostsSettings:
        if not from_path.is_file():
            _error = "Costs json file not found at {}.".format(from_path)
            raise FileNotFoundError(_error)
        if self.include_taxes is None:
            raise ValueError("A boolean value is expected for `include_taxes`.")
        logging.info("Importing costs settings from {}.".format(from_path))
        _costs_fom = self._get_costs_fom(from_path)

        _costs_settings = KoswatCostsSettings()
        _costs_settings.price_year = int(_costs_fom.unit_prices_section.price_level)
        _costs_settings.dike_profile_costs = self._get_dike_profile_costs_settings(
            _costs_fom
        )
        _costs_settings.infrastructure_costs = self._get_infrastructure_costs_settings(
            _costs_fom
        )
        _costs_settings.surtax_costs = self._get_surtax_costs(
            _costs_fom,
        )
        _costs_settings.construction_costs = self._get_construction_costs(_costs_fom)
        return _costs_settings

    def _get_dike_profile_costs_settings(
        self, fom_costs: KoswatCostsJsonFom
    ) -> DikeProfileCostsSettings:
        _settings = DikeProfileCostsSettings()
        _settings.added_layer_grass_m3 = (
            fom_costs.dike_profile_costs_section.construction_grass_layer_m3
        )
        _settings.added_layer_clay_m3 = (
            fom_costs.dike_profile_costs_section.construction_clay_layer_m3
        )
        _settings.added_layer_sand_m3 = (
            fom_costs.dike_profile_costs_section.construction_core_m3
        )
        _settings.reused_layer_grass_m3 = (
            fom_costs.dike_profile_costs_section.reuse_grass_layer_m3
        )
        _settings.reused_layer_core_m3 = (
            fom_costs.dike_profile_costs_section.reuse_core_m3
        )
        _settings.disposed_material_m3 = (
            fom_costs.dike_profile_costs_section.dispose_material_m3
        )
        _settings.profiling_layer_grass_m2 = (
            fom_costs.dike_profile_costs_section.profile_grass_layer_m2
        )
        _settings.profiling_layer_clay_m2 = (
            fom_costs.dike_profile_costs_section.profile_clay_layer_m2
        )
        _settings.profiling_layer_sand_m2 = (
            fom_costs.dike_profile_costs_section.profile_core_m2
        )
        _settings.processing_ground_level_surface_m2 = (
            fom_costs.dike_profile_costs_section.process_ground_level_surface_m2
        )
        return _settings

    def _get_infrastructure_costs_settings(
        self, fom_costs: KoswatCostsJsonFom
    ) -> InfrastructureCostsSettings:
        _settings = InfrastructureCostsSettings()
        _settings.removing_roads_klasse2 = (
            fom_costs.infrastructure_costs_section.roads_class2_removal
        )
        _settings.removing_roads_klasse24 = (
            fom_costs.infrastructure_costs_section.roads_class24_removal
        )
        _settings.removing_roads_klasse47 = (
            fom_costs.infrastructure_costs_section.roads_class47_removal
        )
        _settings.removing_roads_klasse7 = (
            fom_costs.infrastructure_costs_section.roads_class7_removal
        )
        _settings.removing_roads_unknown = (
            fom_costs.infrastructure_costs_section.roads_unknown_removal
        )
        _settings.adding_roads_klasse2 = (
            fom_costs.infrastructure_costs_section.roads_class2_construction
        )
        _settings.adding_roads_klasse24 = (
            fom_costs.infrastructure_costs_section.roads_class24_construction
        )
        _settings.adding_roads_klasse47 = (
            fom_costs.infrastructure_costs_section.roads_class47_construction
        )
        _settings.adding_roads_klasse7 = (
            fom_costs.infrastructure_costs_section.roads_class7_construction
        )
        _settings.adding_roads_unknown = (
            fom_costs.infrastructure_costs_section.roads_unknown_construction
        )
        return _settings

    def _get_surtax_costs(self, fom_costs: KoswatCostsJsonFom) -> SurtaxCostsSettings:
        _settings = SurtaxCostsSettings()
        _fom_settings = (
            fom_costs.surtax_costs_incl_tax_section
            if self.include_taxes
            else fom_costs.surtax_costs_excl_tax_section
        )
        _settings.soil_easy = _fom_settings.soil_easy
        _settings.soil_normal = _fom_settings.soil_normal
        _settings.soil_hard = _fom_settings.soil_hard
        _settings.construction_easy = _fom_settings.constructive_easy
        _settings.construction_normal = _fom_settings.constructive_normal
        _settings.construction_hard = _fom_settings.constructive_hard
        _settings.roads_easy = _fom_settings.road_easy
        _settings.roads_normal = _fom_settings.roads_normal
        _settings.roads_hard = _fom_settings.roads_hard
        _settings.land_purchase_easy = _fom_settings.soil_easy
        _settings.land_purchase_normal = _fom_settings.land_purchase_normal
        _settings.land_purchase_hard = _fom_settings.land_purchase_hard
        return _settings

    def _get_construction_costs(
        self, fom_costs: KoswatCostsJsonFom
    ) -> ConstructionCostsSettings:
        def _construction_fom_to_construction_factor(
            config_fom: ConstructionCostsSectionFom,
        ) -> ConstructionFactors:
            _construction_factors = ConstructionFactors()
            _construction_factors.c_factor = config_fom.c_factor
            _construction_factors.d_factor = config_fom.d_factor
            _construction_factors.z_factor = config_fom.z_factor
            _construction_factors.f_factor = config_fom.f_factor
            _construction_factors.g_factor = config_fom.g_factor
            return _construction_factors

        _settings = ConstructionCostsSettings()
        _settings.cb_sheetpile = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_cb_wall
        )
        _settings.vzg = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_vzg
        )
        _settings.sheetpile_unanchored = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_sheetpile_unanchored
        )
        _settings.sheetpile_anchored = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_sheetpile_anchored
        )
        _settings.diaphragm_wall = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_diaphragm_wall
        )
        _settings.cofferdam = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_cofferdam
        )

        return _settings
