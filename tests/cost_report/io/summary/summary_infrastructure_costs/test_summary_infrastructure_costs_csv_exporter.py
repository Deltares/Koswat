import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_infrastructure_costs.summary_infrastructure_costs_csv_exporter import (
    SummaryInfrastructureCostsCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results
from tests.cost_report.io.summary import valid_mocked_summary


class TestSummaryInfrastructureCostCsvExporter:
    def test_initialize(self):
        _exporter = SummaryInfrastructureCostsCsvExporter()
        assert isinstance(_exporter, SummaryInfrastructureCostsCsvExporter)
        assert isinstance(_exporter, KoswatExporterProtocol)

    def test_summary_infrastructure_costs_csv_exporter_export(
        self, valid_mocked_summary: KoswatSummary, request: pytest.FixtureRequest
    ):
        # 1. Define test data.
        _test_dir = test_results.joinpath(request.node.name)
        _export_path = _test_dir.joinpath("summary_infrastructure_costs.csv")
        if _test_dir.is_dir():
            shutil.rmtree(_test_dir)

        # 2. Run test
        SummaryInfrastructureCostsCsvExporter().export(
            valid_mocked_summary, _export_path
        )

        # 3. Validate results
        assert _export_path.exists()
        _read_text = _export_path.read_text(encoding="utf-8")
        _expected_text = ";;;Kistdam;Kwelscherm;Grondmaatregel profiel;Stabiliteitswand;Kistdam;;;;;;;;Kwelscherm;;;;;;;;Grondmaatregel profiel;;;;;;;;Stabiliteitswand;;;;;;;\n\
;;;;;;;Road Klasse2;;;;Road Klasse24;;;;Road Klasse2;;;;Road Klasse24;;;;Road Klasse2;;;;Road Klasse24;;;;Road Klasse2;;;;Road Klasse24;;;\n\
Section;X coord;Y coord;Totale kosten (€);Totale kosten (€);Totale kosten (€);Totale kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€);Zone A Lengte (m);Zone A Kosten (€);Zone B Lengte (m);Zone B Kosten (€)\n\
A;0.24;0.42;0.0;0.0;0.0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0\n\
A;2.4;0.42;6.6000000000000005;6.6000000000000005;6.6000000000000005;6.6000000000000005;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2;1;1.1;2;2.2\
A;0.24;2.4;13.200000000000001;13.200000000000001;13.200000000000001;13.200000000000001;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4;2;2.2;4;4.4\n\
A;2.4;2.4;19.8;19.8;19.8;19.8;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005;3;3.3000000000000003;6;6.6000000000000005"
        assert _expected_text == _read_text
