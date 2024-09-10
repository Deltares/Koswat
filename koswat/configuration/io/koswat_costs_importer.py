from __future__ import annotations

import logging
from pathlib import Path

from koswat.configuration.io.ini.koswat_costs_ini_fom import (
    ConstructionCostsSectionFom,
    KoswatCostsIniFom,
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
from koswat.core.io.ini.koswat_ini_reader import KoswatIniReader
from koswat.core.io.koswat_importer_protocol import KoswatImporterProtocol


class KoswatCostsImporter(KoswatImporterProtocol):
    include_taxes: bool

    def __init__(self) -> None:
        self.include_taxes = None

    def _get_costs_fom(self, ini_file: Path) -> KoswatCostsIniFom:
        reader = KoswatIniReader()
        reader.koswat_ini_fom_type = KoswatCostsIniFom
        return reader.read(ini_file)

    def import_from(self, from_path: Path) -> KoswatCostsSettings:
        if not from_path.is_file():
            _error = "Costs ini file not found at {}.".format(from_path)
            raise FileNotFoundError(_error)
        if self.include_taxes is None:
            raise ValueError("A boolean value is expected for `include_taxes`.")
        logging.info("Importing costs settings from {}.".format(from_path))
        _costs_fom = self._get_costs_fom(from_path)

        _costs_settings = KoswatCostsSettings()
        _costs_settings.price_year = int(_costs_fom.unit_prices_section.prijspeil)
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
        self, fom_costs: KoswatCostsIniFom
    ) -> DikeProfileCostsSettings:
        _settings = DikeProfileCostsSettings()
        _settings.added_layer_grass_m3 = (
            fom_costs.dike_profile_costs_section.aanleg_graslaag_m3
        )
        _settings.added_layer_clay_m3 = (
            fom_costs.dike_profile_costs_section.aanleg_kleilaag_m3
        )
        _settings.added_layer_sand_m3 = (
            fom_costs.dike_profile_costs_section.aanleg_kern_m3
        )
        _settings.reused_layer_grass_m3 = (
            fom_costs.dike_profile_costs_section.hergebruik_graslaag_m3
        )
        _settings.reused_layer_core_m3 = (
            fom_costs.dike_profile_costs_section.hergebruik_kern_m3
        )
        _settings.disposed_material_m3 = (
            fom_costs.dike_profile_costs_section.afvoeren_materiaal_m3
        )
        _settings.profiling_layer_grass_m2 = (
            fom_costs.dike_profile_costs_section.profileren_graslaag_m2
        )
        _settings.profiling_layer_clay_m2 = (
            fom_costs.dike_profile_costs_section.profileren_kleilaag_m2
        )
        _settings.profiling_layer_sand_m2 = (
            fom_costs.dike_profile_costs_section.profileren_kern_m2
        )
        _settings.bewerken_maaiveld_m2 = (
            fom_costs.dike_profile_costs_section.bewerken_maaiveld_m2
        )
        return _settings

    def _get_infrastructure_costs_settings(
        self, fom_costs: KoswatCostsIniFom
    ) -> InfrastructureCostsSettings:
        _settings = InfrastructureCostsSettings()
        _settings.removing_roads_klasse2 = (
            fom_costs.infrastructure_costs_section.wegen_klasse2_verwijderen
        )
        _settings.removing_roads_klasse24 = (
            fom_costs.infrastructure_costs_section.wegen_klasse24_verwijderen
        )
        _settings.removing_roads_klasse47 = (
            fom_costs.infrastructure_costs_section.wegen_klasse47_verwijderen
        )
        _settings.removing_roads_klasse7 = (
            fom_costs.infrastructure_costs_section.wegen_klasse7_verwijderen
        )
        _settings.removing_roads_unknown = (
            fom_costs.infrastructure_costs_section.wegen_onbekend_verwijderen
        )
        _settings.adding_roads_klasse2 = (
            fom_costs.infrastructure_costs_section.wegen_klasse2_aanleg
        )
        _settings.adding_roads_klasse24 = (
            fom_costs.infrastructure_costs_section.wegen_klasse24_aanleg
        )
        _settings.adding_roads_klasse47 = (
            fom_costs.infrastructure_costs_section.wegen_klasse47_aanleg
        )
        _settings.adding_roads_klasse7 = (
            fom_costs.infrastructure_costs_section.wegen_klasse7_aanleg
        )
        _settings.adding_roads_unknown = (
            fom_costs.infrastructure_costs_section.wegen_onbekend_aanleg
        )
        return _settings

    def _get_surtax_costs(self, fom_costs: KoswatCostsIniFom) -> SurtaxCostsSettings:
        _settings = SurtaxCostsSettings()
        _fom_settings = (
            fom_costs.surtax_costs_incl_tax_section
            if self.include_taxes
            else fom_costs.surtax_costs_excl_tax_section
        )
        _settings.soil_easy = _fom_settings.grond_makkelijk
        _settings.soil_normal = _fom_settings.grond_normaal
        _settings.soil_hard = _fom_settings.grond_moeilijk
        _settings.construction_easy = _fom_settings.constructief_makkelijk
        _settings.construction_normal = _fom_settings.constructief_normaal
        _settings.construction_hard = _fom_settings.constructief_moeilijk
        _settings.roads_easy = _fom_settings.wegen_makkelijk
        _settings.roads_normal = _fom_settings.wegen_normaal
        _settings.roads_hard = _fom_settings.wegen_moeilijk
        _settings.land_purchase_easy = _fom_settings.grond_makkelijk
        _settings.land_purchase_normal = _fom_settings.grondaankoop_normaal
        _settings.land_purchase_hard = _fom_settings.grondaankoop_moeilijk
        return _settings

    def _get_construction_costs(
        self, fom_costs: KoswatCostsIniFom
    ) -> ConstructionCostsSettings:
        def _construction_fom_to_construction_factor(
            ini_fom: ConstructionCostsSectionFom,
        ) -> ConstructionFactors:
            _construction_factors = ConstructionFactors()
            _construction_factors.c_factor = ini_fom.c_factor
            _construction_factors.d_factor = ini_fom.d_factor
            _construction_factors.z_factor = ini_fom.z_factor
            _construction_factors.f_factor = ini_fom.f_factor
            _construction_factors.g_factor = ini_fom.g_factor
            return _construction_factors

        _settings = ConstructionCostsSettings()
        _settings.cb_damwand = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_cb_wall
        )
        _settings.vzg = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_vzg
        )
        _settings.damwand_onverankerd = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_damwall_unanchored
        )
        _settings.damwand_verankerd = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_damwall_anchored
        )
        _settings.diepwand = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_deep_wall
        )
        _settings.kistdam = _construction_fom_to_construction_factor(
            fom_costs.construction_cost_cofferdam
        )

        return _settings
