import pytest

from koswat.profiles.koswat_layers import KoswatLayer


class TestAcceptance:
    def test_koswat_package_can_be_imported(self):
        """
        Import test. Not really necessary given the current way we are testing (directly to the cli). But better safe than sorry.
        """

        try:
            import koswat
            import koswat.main
        except ImportError as exc_err:
            pytest.fail(f"It was not possible to import required packages {exc_err}")

    def test_given_default_case_returns_costs(self):
        # 1. Define test data.
        _base_layer = KoswatLayer()

        # 2. Run test.

        # 3. Verify eexpectations.
        pass
