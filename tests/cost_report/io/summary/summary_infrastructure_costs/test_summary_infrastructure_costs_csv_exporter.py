import shutil

import pytest

from koswat.core.io.koswat_exporter_protocol import KoswatExporterProtocol
from koswat.cost_report.io.summary.summary_infrastructure_costs.summary_infrastructure_costs_csv_exporter import (
    SummaryInfrastructureCostsCsvExporter,
)
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from tests import test_results


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
;;;*) Kosten incl. opslagfactoren;;;;TestInfra1;;;;TestInfra2;;;;TestInfra1;;;;TestInfra2;;;;TestInfra1;;;;TestInfra2;;;;TestInfra1;;;;TestInfra2;;;\n\
Section;X coord;Y coord;Totale kosten* (Euro);Totale kosten* (Euro);Totale kosten* (Euro);Totale kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro);Zone A Lengte (m);Zone A Kosten* (Euro);Zone B Lengte (m);Zone B Kosten* (Euro)\n\
A;0.24;0.42;0.0;0.0;0.0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0;0;0.0\n\
A;2.4;0.42;19.8;19.8;19.8;19.8;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6;1;3.3;2;6.6\n\
A;0.24;2.4;79.2;79.2;79.2;79.2;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4;2;13.2;4;26.4\n\
A;2.4;2.4;178.2;178.2;178.2;178.2;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4;3;29.7;6;59.4"
        assert _expected_text == _read_text
