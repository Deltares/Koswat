from koswat.strategies.infra_priority_strategy.infra_cluster_option import (
    InfraClusterOption,
)


class TestInfraClusterOption:
    def test_initialize(self):
        # 1. Define test data
        _min_length = 2

        # 2. Run test.
        _option = InfraClusterOption(_min_length)

        # 3. Verify expectations.
        assert isinstance(_option, InfraClusterOption)
        assert not _option.cluster_collection
        assert not _option.cluster_costs
        assert not _option.valid_option()
