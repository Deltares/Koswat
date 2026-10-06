# Infrastructure priority

**DEFAULT STRATEGY**
This strategy checks whether the clusters resulting from the [order based strategy](#order-based) can change their selected reinforcement to one with cheaper costs. These costs are extracted from the [cost report](koswat_cost_report.md#cost-report) and relate to the reinforcement profile costs (dike's materials for the required space) and the possible [infrastructure costs](koswat_cost_report.md#infrastructure-report). In steps, this strategy can be broke down as:

__Steps breakdown__:

1. Assignment of [order based clusters](#order-based),
2. [Cluster options](#cluster-options) evaluation,
    1. [Common available measures](#cluster-common-available-measures-cost) cost calculation,
    2. Cheapest option selection,
3. Update reinforcement selection with selected option.

## Cluster options

For an optimal assignment of a new reinforcement profile, we make use of "subclusters". These subclusters are contiguous subsets from an order based cluster and have the minimal required length (`StrategyInput.reinforcement_min_cluster`). The logic for this section can be found in `InfraPriorityStrategy.generate_subcluster_options`.

For each of original the clusters, multiple combinations of subclusters are possible. We refer to them as "**cluster option**" (`InfraClusterOption`) . We can already discard creating subclusters when the size of the original cluster is less than twice the required minimal length. So for a minimal length of 2 locations, you require a cluster of at least 4 locations to generate subclusters.

__Conditions__:

- We only create subclusters when the cluster's original size is, at least, twice the required minimal cluster's length.
- We estimate the cluster's minimal length to be at least twice the size of the buffer so: `min_cluster_length = (2 * reinforcement_min_buffer) + 1`.
- We create subclusters based on the immediate results of the [order based strategy](#order-based).  We do not try to combine or create new clusters based on a "greedier" strategy.


### Cluster option example

For example, given the results of the [clustering example](#clustering-example) we can calculate the options for the clusters for a required minimal length of `2`:

1. List of clusters:
    ```json
    {
        (0, ["Location_000","Location_001",]),
        (4, ["Location_002","Location_003",
                "Location_004","Location_005",
                "Location_006",]),
        (5, ["Location_007","Location_008","Location_009",]),
    }
    ```
2. Options for cluster `{(0, ["Location_000","Location_001",])}`
    ```json
    - Valid options:
        (0, ["Location_000","Location_001",])
    ```

3. Options for cluster `{(4, ["Location_002","Location_003", "Location_004","Location_005", "Location_006",])}`
    ```json
    - Valid:
        - {["Location_002", "Location_003"],
            ["Location_004", "Location_005", "Location_006"]},
        - {["Location_002", "Location_003", "Location_004"],
            ["Location_005", "Location_006"]}
    - Invalid:
        - first subcluster's size is less than required:
            {["Location_002"],
            ["Location_003", "Location_004"],
            ["Location_005", "Location_006"]}

        - last subcluster's size is less than required:
            {["Location_002", "Location_003"],
            ["Location_004", "Location_005"],
            ["Location_006"]}, 
        - second subcluster's size is less than required:
            {["Location_002", "Location_003"],
            ["Location_004"],
            ["Location_005", "Location_006"]}, 
        - and so on...
    ```

4. Options for cluster `{(5, ["Location_007","Location_008","Location_009",]),}`
    ```json
    - Valid:
        - {["Location_007","Location_008","Location_009",]}
    - Invalid:
        - first subcluster's size is less than required:
            {["Location_007"], ["Location_008", "Location_009"]}
        - last subcluster's size is less than required:
            {["Location_007", "Location_008"], ["Location_009"]}
        - and so on...
    ```

## Cluster common available measures' cost

Once we have calculated a [cluster's option](#cluster-options) we can determine whether this cluster should be consider as a valid one. This estimation is based on the __cheapest reinforcement's cost__ (including surtax), and to get this value we first need to know which reinforcements are available at all the locations of this option. 

We will store this value in the `InfraClusterOption.cluster_costs`. In the current implementation, these costs are added to the `InfraClusterOption` together with the cluster's data (`list[InfraCluster]`).

__Conditions__:

- A "viable" cluster option must be cheaper than the order's cluster and has the cluster's minimal length.
- We consider "minimal costs" or "lower costs" as the lowest cost of applying a certain reinforcement type to a given subcluster.


### Common available measures' cost example

Following the [options example](#cluster-option-example) we can estimate some fictional costs based on the following tables (if a type / location is not mentioned, then assume its cost is zero (`0`)):

| Index | Reinforcement type | base cost incl. surtax |
| ---- | ---- |---- |
| 0 | Soil reinforcement | 42 |
| 1 | Vertical Piping Solution | 133 |
| 2 | Piping Wall | 420 |
| 3 | Stability Wall Toe| 1.328 |
| 4 | Stability Wall Crest| 4.2000 |
| 5 | Cofferdam | 42.000 |

| Location | Reinforcement indices | Infrastructure cost incl. surtax |
| ---- | ---- | ---- |
| Location_000 | 0, 1, 2 | 420.000 |
| Location_005 | 0, 1, 2, 3, 4, 5 | 420.000 |

We already know that only the second cluster can generate subclusters, therefore different valid options, so we will use said subcluster's options for the example.

```json

1. Determine current cost:
    - {4, ["Location_002", "Location_003",
        "Location_004", "Location_005", "Location_006"]}
    - Base costs = 5 * 4.200 = 21.000
    - Infra costs = (1) * 420.000 = 420.000
    - Total costs = 441.000

2. Calculate costs for first option:
    - {(4, ["Location_002", "Location_003"],
        ["Location_004", "Location_005", "Location_006"])},
    1. First subcluster's common measures:
        - Stability Wall Crest (current):
            - Base costs = 2 * 4.200 = 8.4000
            - Infra costs = 0
            - Total costs = 8.4000
        - Cofferdam:
            - Base costs = 2 * 42.000 = 84.000
            - Infra costs = 0
            - Total costs = 84.000
        - The current reinforcement is cheaper
    2. Second subcluster's common measures:
        - Stability Wall Crest (current):
            - Base costs = 3 * 4.2000 = 12.600
            - Infra costs = (1) * 420.000 = 420.000
            - Total costs = 432.600
        - Cofferdam:
            - Base costs = 3 * 42.000 = 126.000
            - Infra costs = 0
            - Total costs = 126.000
        - Cofferdam will be cheaper.
    3. Subcluster's best option is cheaper than current:
        - {(4, ["Location_002", "Location_003"]),
            (5, ["Location_004", "Location_005", "Location_006"])}
        - Total cost = 8.400 + 126.000 = 134.400
        - Selected as option.

3. Calculate costs for second option:
    - {4, (["Location_002", "Location_003", "Location_004"],
        ["Location_005", "Location_006"])}
    1. First subluster's common measures
        - Stability Wall Crest (current):
            - Base costs = 3 * 4.200 = 12.600
            - Infra costs = 0
            - Total costs = 12.600
        - Cofferdam:
            - Base costs = 3 * 42.000 = 126.000
            - Infra costs = 0
            - Total costs = 126.000
        - The current reinforcement is cheaper
    2. Second subluster's common measures
        - Stability Wall Crest (current):
            - Base costs = 2 * 4.200 = 8.400
            - Infra costs = 0
            - Total costs = 8.400
        - Cofferdam:
            - Base costs = 2 * 42.000 = 84.000
            - Infra costs = 0
            - Total costs = 84.000
        - Cofferdam is cheaper
    3. Subcluster's best option is cheaper than selection:
        - {(4, ["Location_002", "Location_003", "Location_004"]),
            (5, ["Location_005", "Location_006"])}
        - Total cost = 12.600 + 84.000 = 96.600
        - Selected as option.

4. Update locations' selected reinforcement:
{
    (2, ["Location_000","Location_001",]),
    (4, ["Location_002","Location_003", "Location_004",]),
    (5, ["Location_005","Location_006", "Location_007",
          "Location_008","Location_009",]),
}
```

In this example we can therefore demonstrate the cost reduction. The last column represents the difference:

- O.S. = Order strategy
- I.S. = Infrastructure priority strategy

| Location | (O.S.) reinforcement | (O.S.) cost | (I.S.) reinforcement | (I.S.) cost | Difference |
| ---- | ---- | ---- | ---- | ---- | ---- |
|Total | ---- | 8.547.084 | ----  | 2.223.440 | __-419.622__ |
|Location_000 | Soil reinforcement | 420.042 | Piping Wall | 420 | -419.622 |
|Location_001 | Soil reinforcement | 42 | Piping Wall | 420 | 378 |
|Location_002 | Stability Wall Crest | 4.200 | Stability Wall Crest | 4.2000 | 0 |
|Location_003 | Stability Wall Crest | 4.2000 | Stability Wall Crest | 4.2000 | 0 |
|Location_004 | Stability Wall Crest | 4.2000 | Stability Wall Crest | 42.000 | 0 |
|Location_005 | Stability Wall Crest | 424.200 | Cofferdam | 42.000 | -382.200 |
|Location_006 | Stability Wall Crest | 4.2000 | Cofferdam | 42.000 |37.800 |
|Location_007 | Cofferdam | 42.000 | Cofferdam | 42.000 | 0 |
|Location_008 | Cofferdam | 42.000 | Cofferdam | 42.000 | 0 |
|Location_009 | Cofferdam | 42.000 | Cofferdam | 42.000 | 0 |
