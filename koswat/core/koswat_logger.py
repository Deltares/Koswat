from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


class KoswatLogger:
    log_file: Optional[Path] = None

    @classmethod
    def init_logger(cls, log_file: Path) -> KoswatLogger:
        _logger = cls()
        if log_file.suffix != ".log":
            log_file = log_file.with_suffix(".log")

        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.unlink(missing_ok=True)
        log_file.touch()

        _logger.log_file = log_file
        _logger._set_console_handler()
        _logger._set_file_handler()
        _logger._set_formatter()
        return _logger

    def _get_logger(self) -> logging.Logger:
        """
        Gets the koswat logger which by default is the root logging.Logger.

        Returns:

            logging.Logger: Logger instance.
        """
        return logging.getLogger("")

    def _set_file_handler(self) -> None:
        # Create a root logger and set the minimum logging level.
        self._get_logger().setLevel(logging.INFO)
        self._file_handler = logging.FileHandler(filename=self.log_file, mode="a")
        self._file_handler.setLevel(logging.INFO)
        self._get_logger().addHandler(self._file_handler)

    def _set_console_handler(self) -> None:
        # Create a console handler and set the required logging level.
        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(logging.INFO)  # Can be also set to WARNING
        self._get_logger().addHandler(self._console_handler)

    def _set_formatter(self) -> None:
        # Create a formatter and add to the file and console handlers.
        _formatter = logging.Formatter(
            fmt="%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p",
        )
        self._file_handler.setFormatter(_formatter)
        self._console_handler.setFormatter(_formatter)
