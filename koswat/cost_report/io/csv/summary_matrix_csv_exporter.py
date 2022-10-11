import itertools
from typing import List

from koswat.cost_report.io.csv.summary_matrix_csv_fom import SummaryMatrixCsvFom
from koswat.cost_report.summary.koswat_summary import KoswatSummary
from koswat.io.koswat_exporter_protocol import KoswatExporterProtocol


class SummaryMatrixCsvExporter(KoswatExporterProtocol):
    data_object_model: KoswatSummary

    def __init__(self) -> None:
        self.data_object_model = None

    def build(self) -> SummaryMatrixCsvFom:
        _fom = SummaryMatrixCsvFom()
        _list_of_report_values = list(
            zip(
                *(
                    list(report.as_dict().values())
                    for report in self.data_object_model.locations_profile_report_list
                )
            )
        )
        _fom.headers = [" "]
        _fom.headers.extend(_list_of_report_values[0])
        _total_cost_row = ["Total cost (€)"]
        _total_cost_row.extend(_list_of_report_values[1])
        _total_volume_row = ["Total volume (m3)"]
        _total_volume_row.extend(_list_of_report_values[2])
        _fom.cost_rows = [_total_cost_row, _total_volume_row]

        return _fom

    def export(self, file_object_model: SummaryMatrixCsvFom) -> None:
        return super().export(file_object_model)
