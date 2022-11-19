from pathlib import Path
from typing import Generator

import pytest
from matplotlib import pyplot
from matplotlib.figure import Figure

from koswat.plots.koswat_figure_context_handler import KoswatFigureContextHandler
from tests import test_results


class TestKoswatFigureContextHandler:
    def test_initialize(self):
        _test_file = Path(__file__)
        _context_handler = KoswatFigureContextHandler(_test_file, 42)
        assert isinstance(_context_handler, KoswatFigureContextHandler)
        assert _context_handler._output_path == _test_file
        assert _context_handler._dpi == 42

    @pytest.fixture(autouse=False)
    def valid_context(self) -> Generator:
        _test_dir = test_results / "koswat_figure_context_handler"
        _test_file = _test_dir / "test_plot.png"
        _test_dir.mkdir(parents=True, exist_ok=True)
        _test_file.unlink(missing_ok=True)

        _context_handler = KoswatFigureContextHandler(_test_file, 42)
        yield _context_handler

        pyplot.close()
        _test_file.unlink(missing_ok=True)

    def test_enter_context(self, valid_context: KoswatFigureContextHandler):
        _return_figure = valid_context.__enter__()
        assert isinstance(_return_figure, Figure)
        assert _return_figure.dpi == 42

    def test_exit_context(self, valid_context: KoswatFigureContextHandler):
        assert not valid_context._output_path.is_file()
        valid_context.__enter__()
        valid_context.__exit__()
        assert valid_context._output_path.is_file()
