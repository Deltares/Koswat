from typing import Protocol

import pytest


class CasesProtocol(Protocol):
    cases: list[pytest.param]
