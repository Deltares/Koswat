from __future__ import annotations

import logging
from pathlib import Path

from koswat.configuration.io.ini.koswat_costs_ini_fom import KoswatCostsIniFom
from koswat.configuration.settings.costs.koswat_costs import (
    DikeProfileCostsSettings,
    InfrastructureCostsSettings,
    KoswatCostsSettings,
    StorageCostsSettings,
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
        logging.info("Importing costs from {}.".format(from_path))
        _costs_fom = self._get_costs_fom(from_path)

        _costs_settings = KoswatCostsSettings()
        _costs_settings.price_year = int(_costs_fom.unit_prices_section.prijspeil)
        _costs_settings.dike_profile_costs = self._get_dike_profile_costs_settings(
            _costs_fom
        )
        _costs_settings.infrastructure_costs = self._get_infrastructure_costs_settings(
            _costs_fom
        )
        _costs_settings.storage_costs = self._get_storage_costs(
            _costs_fom,
        )
        return _costs_settings

    def _get_storage_costs(self, fom_costs: KoswatCostsIniFom) -> StorageCostsSettings:
        _settings = StorageCostsSettings()
        _fom_settings = (
            fom_costs.storing_costs_incl_tax_section
            if self.include_taxes
            else fom_costs.storing_costs_excl_tax_section
        )
        _settings.ground_easy = _fom_settings.grond_makkelijk
        _settings.ground_normal = _fom_settings.grond_normaal
        _settings.ground_hard = _fom_settings.grond_moeilijk
        _settings.construction_easy = _fom_settings.constructief_makkelijk
        _settings.construction_normal = _fom_settings.constructief_normaal
        _settings.construction_hard = _fom_settings.constructief_moeilijk
        _settings.roads_easy = _fom_settings.wegen_makkelijk
        _settings.roads_normal = _fom_settings.wegen_normaal
        _settings.roads_hard = _fom_settings.wegen_moeilijk
        _settings.ground_purchase_easy = _fom_settings.grond_makkelijk
        _settings.ground_purchase_normal = _fom_settings.grondaankoop_normaal
        _settings.ground_purchase_hard = _fom_settings.grondaankoop_moeilijk
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
