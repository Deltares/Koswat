# Strategies

Koswat can determine which is the "best" reinforcement type for a dike traject based on different selection criteria that we name "strategies" (`StrategyProtocol`).

A strategy requires a strategy input (`StrategyInput`), this input contains information over which reinforcement types are available at each location as well as what's the __minimal buffer__ (`reinforcement_min_buffer`) and __minimal length__ (`reinforcement_min_length`)  for each reinforcement type.

By default a strategy is applied as follows:

1. For each point (meter) in the traject, determine which reinforcements can be applied to it.
2. Choose one of the available reinforcements based on the chosen [strategy](#order-based-default). When no reinforcement is available the most restrictive will be chosen (`CofferDam`).
3. Apply a buffer (`reinforcement_min_buffer`) for each one of the reinforcements.
4. Check if the minimal distance between constructions is met (`reinforcement_min_length`), otherwise change it into one of the reinforcements next to it.
5. Repeat 4 until all reinforcements have enough distance between themselves.
6. Return list of mapped locations (`list[StrategyLocationReinforcement]`).

## Available strategies

### Order based (default)

This strategy is the first and default of all defined strategies. Its criteria is based on a pre-defined ['order'](#reinforcement-order) of each reinforcement. In steps, it can be seen as:

1. Pre-selection of a location's available reinforcement based on said order, when a location does not have any "available" reinforcement, then the last reinforcement's order will be pre-selected.
2. [Grouping](#reinforcement-grouping) of all locations by their pre-selected reinforcement.
3. [Buffering](#reinforcement-buffering) to each of the groupings.
4. [Clustering](#reinforcement-clustering) to the resulting groupings from the previous step.

#### Reinforcement order
The predefined (hardcoded) reinforcement's order, from least to most restrictive, is as follows:

| Priority index | Reinforcement type |
| ---- | ---- |
| 0 | `SoilReinforcementProfile` |
| 1 | `VPSReinforcementProfile` |
| 2 | `PipingWallReinforcementProfile` |
| 3 | `StabilityWallReinforcementProfile` |
| 4 | `CofferDamReinforcementProfile` |

#### Reinforcement grouping

We create reinforcement-location "grouping" for the whole traject.

A grouping represents a reinforcement type that is "selected" for a series of continuous locations. This means locations that are next to each other sharing the same measure type (`Type[ReinforcementProfileProtocol]`).

##### Grouping example
Simplified representation for a traject with 10 locations. This example is also tested in the `tests.strategies.order_strategy.py` test file.
```json
{
    "SoilReinforcementProfile": [
        "Location_000",
        "Location_001",
        "Location_002",
    ],
    "StabilityWallReinforcementProfile": [
        "Location_003",
        "Location_004",
    ],
    "SoilReinforcementProfile": [
        "Location_005",
        "Location_006",
        "Location_007",
    ],
    "CofferDamReinforcementProfile": [
        "Location_008",
        "Location_009",
    ],
}
```

#### Reinforcement buffering

Given a [reinforcement grouping](#reinforcement-grouping), we will create a dictionary of masks of size `NM` where `N` (the keys) is the number of available reinforcement types (`Type[ReinforcementProfileProtocol]`) and `M` the number of available locations. 

__Note__: Masks' values are the position of a reinforcement type in the [reinforcement's order list](#reinforcment-order). So a location with`CofferDamReinforcementProfile` will have a 4 at the mask's position, whilst a `SoilReinforcementProfile` will have a 0 instead (remember in Python indexing starts with 0).

__Steps breakdown__:

1. Initialize the dictionary masks with all values to -1.

2. Iterate over the groupings list, and for each entry:

    1. Select the mask to update using the grouping's reinforcement type (cluster's key).

    2. Update the indices representing the grouping's locations (grouping's values) with the matching value for this grouping's key (see previous __note__).

    3. Add a buffer (`StrategyInput.reinforcement_min_buffer`) by updating the adjacent's positions of this grouping with the same values as in step 1. 

3. Merge all masks into a 1-dimensional array where the cell's value is the maximum between the available masks.
    - This is done to prevent that a buffer of a "stronger" demanding reinforcement such as `CofferDamReinforcementProfile` is replaced by a "weaker" one.
 
4. Update the locations with their new associated reinforcement. The resulting mask contains the index of the reinforcement to be applied in the [reinforcement's order](#reinforcement-order).


##### Buffering example

One simplified example, based on the [grouping example](#grouping-example), and using a buffer value of "1". This example is also tested in the `tests.strategies.order_strategy_buffering.py` test file.

```json
1. Initialize the masks based on the provided clusters:
    {
        "SoilReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
        "VPSReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
        "PipingWallReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
        "StabilityWallReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
        "CofferDamReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
    }

2. Iterate over the clusters and update the masks' values:
    {
        "SoilReinforcementProfile": 
            [ 0,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        "VPSReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        "PipingWallReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        "StabilityWallReinforcementProfile": 
            [-1, -1,  3,  3,  3,  3, -1, -1, -1, -1],
        "CofferDamReinforcementProfile": 
            [-1, -1, -1, -1, -1, -1, -1,  4,  4,  4],
    }

3. Merge all masks and select their maximum value:
    [0, 0, 3, 3, 3, 3, 0, 4, 4, 4]

4. Update the cluster's locations:
    {
        "SoilReinforcementProfile": [
            "Location_000",
            "Location_001",
        ],
        "StabilityWallReinforcementProfile": [
            "Location_002",
            "Location_003",
            "Location_004",
            "Location_005",
        ],
        "SoilReinforcementProfile": [
            "Location_006",
        ],
        "CofferDamReinforcementProfile": [
            "Location_007",
            "Location_008",
            "Location_009",
        ],
    }
```

#### Reinforcement clustering

Given a [reinforcement grouping](#reinforcement-grouping), ideally done after applying [buffering](#reinforcement-buffering), we will now proceed to change the pre-selected reinforcement of all those groupings that contain less locations than required by the describing property. We do this by updating their type with the one of a "stronger" adjacent grouping, on this section called "clusters". These clusters are internally represented by the class `OrderCluster`.

The strategy here is to detect _non-compliant_ reinforcement-location clusters and replace their selected reinforcement type with the "least strong" of its adjacent clusters. We do this iteratively, so we first target the lowest type of reinforcements (`SoilReinforcementProfile`) and we move up until the first to the last (the last one cannot be further strengthened).

__Conditions__: 

- We define a _non-compliant_ cluster as a cluster that does not contain as many locations as defined by the minimal length requirement (`reinforcement_min_length`).
- We also define a _non-compliant exception_ when a cluster does not meet said requirement but the adjacent clusters are of a lower reinforcement type. Therefore retaining their initial reinforcement type.
- The first and last clusters, are __always considered compliant__. Therefore they retain their initial reinforcement type.
- Clusters whose reinforcement type is placed the last in the strategy's [order](#reinforcement-order), are skipped and __always considered compliant__, as they cannot be further strengthened.

__Steps breakdown__:

1. Generate a list of all available _unmerged_ clusters.
2. For each reinforcement type _target-reinforcement_, in the strategy order:
    1. Get the current _non-compliant_ clusters
    2. For each _non-compliant_ _target-reinforcement_ cluster :
        1. Check if its indeed not compliant.
            - Otherwise move to the next cluster.
        2. Get a stronger cluster among the neighbors. Selects the neighbor with the
        "weakest", yet greater than the actual, reinforcement type value.
            - If both neighbors are "weaker" than the current reinforcement type,
            then it is considered an "exception" as it cannot be further strengthened.
            We therefore move to the next _non-compliant_ cluster.
        3. Move the current cluster's locations to the stronger reinforcement cluster.
        4. Remove the cluster from the "available clusters" list as it is integrated in
        step 2.2.3.


##### Clustering example

One simplified example, based on the [buffering example](#buffering-example), and using a minimal distance of "5". This example is also tested in the `tests.strategies.order_strategy_clustering.py` test file.

```json
1. List of unmerged clusters:
    {
        (0, ["Location_000","Location_001",]),
        (3, ["Location_002","Location_003","Location_004","Location_005",]),
        (0, ["Location_006",]),
        (4, ["Location_007","Location_008","Location_009",])
    }

2. Iterate over each reinforcement type:

2.1. Target is "SoilReinforcementProfile" (idx=0), non-compliant clusters
    {
        (0, ["Location_006",])
    }

2.1.1. Length = 1.

2.1.2. Get a stronger neighbor,
    - Left-neighbor reinforcement type = 3,
    - Right-neighbor reinforcement type = 4,
    - Left-neighbor is selected.

2.1.3. Move locations to stronger neighbor.
    {
        (2, ["Location_002", ... ,"Location_006",]),
        (0, ["Location_006",]),
    }

2.1.4. Remove the current cluster from the available list.

2.2. Target is "PipingWallReinforcementProfile" (idx=2), 
    - All clusters are compliant at this point.

2.3. Target is "StabilityWallReinforcementProfile" (idx=3),
    - All clusters are compliant at this point.

2.4. "CofferDamReinforcementProfile" (idx=4)
    - Last reinforcement profile type, therefore the strongest.

Resulting cluster:
    {
        (0, ["Location_000","Location_001",]),
        (3, ["Location_002","Location_003","Location_004","Location_005","Location_006",]),
        (4, ["Location_007","Location_008","Location_009",]),
    }
```

### Infrastructure priority

This (experimental) strategy checks whether the clusters resulting from the [order based strategy](#order-based-default) can change their selected reinforcement to one with cheaper costs. These costs are extracted from the [cost report](koswat_cost_report.md#cost-report) and relate to the reinforcement profile costs (dike's materials for the required space) and the possible [infrastructure costs](koswat_cost_report.md#infrastructure-report). In steps, this strategy can be broke down as:

__Steps breakdown__:

1. Assignment of [order based clusters](#order-based-default),
2. [Cluster options](#cluster-options) evaluation,
    1. [Common available measures](#cluster-common-available-measure-costs) cost calculation,
    2. Cheapest option selection,
3. Update reinforcement selection with selected option.

#### Cluster options

For an optimal assignment of a new reinforcement profile, we make use of "subclusters". These subclusters are contiguous subsets from an order based cluster and have the minimal required length (`StrategyInput.reinforcement_min_cluster`). The logic for this section can be found in `InfraPriorityStrategy.generate_subcluster_options`.

For each of original the clusters, multiple combinations of subclusters are possible. We refer to them as "**cluster option**" (`InfraClusterOption`) . We can already discard creating subclusters when the size of the original cluster is less than twice the required minimal length. So for a minimal length of 2 locations, you require a cluster of at least 4 locations to generate subclusters.

__Conditions__:

- We only create (sub)clusters when the cluster's original size is, at least, twice the required minimal cluster's length.
- We estimate the cluster's minimal length to be at least twice the size of the buffer so: `min_cluster_length = (2 * reinforcement_min_buffer) + 1`.
- We create (sub)clusters based on the immediate results of the [order based strategy](#order-based-default).  We do not try to combine or create new clusters based on a "greedier" strategy.


##### Cluster option example

For example, given the results of the [clustering example](#clustering-example) we can calculate the options for the clusters for a required minimal length of `2`:

1. List of clusters:
    ```json
    {
        (0, ["Location_000","Location_001",]),
        (3, ["Location_002","Location_003",
                "Location_004","Location_005",
                "Location_006",]),
        (4, ["Location_007","Location_008","Location_009",]),
    }
    ```
2. Options for cluster `{(0, ["Location_000","Location_001",])}`
    ```json
    - Valid options:
        (0, ["Location_000","Location_001",])
    ```

3. Options for cluster `{(3, ["Location_002","Location_003", "Location_004","Location_005", "Location_006",])}`
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

4. Options for cluster `{(4, ["Location_007","Location_008","Location_009",]),}`
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

#### Cluster common available measures' cost

Once we have calculated a [cluster's option](#cluster-options) we can determine whether this cluster should be consider as a valid one. This estimation is based on the __cheapest reinforcement's cost__, and to get this value we first need to know which reinforcements are available at all the locations of this option. 

We will store this value in the `InfraClusterOption.cluster_costs`. In the current implementation, these costs are added to the `InfraClusterOption` together with the cluster's data (`list[InfraCluster]`).

__Conditions__:

- A "viable" cluster option must be cheaper than the order's cluster and has the cluster's minimal length.
- We consider "minimal costs" or "lower costs" as the lowest cost of applying a certain reinforcement type to a given subcluster.


##### Common available measures' cost example

Following the [options example](#cluster-option-example) we can estimate some fictional costs based on the following tables (if a type / location is not mentioned, then assume its cost is zero (`0`)):

| Index | Reinforcement type | base cost |
| ---- | ---- |---- |
| 0 | Soil reinforcement | 42 |
| 1 | Vertical Piping Solution | 420 |
| 2 | Piping Wall | 4.200 |
| 3 | Stability Wall | 42.000 |
| 4 | Cofferdam | 420.000 |

| Location | Reinforcement indices | Infrastructure cost |
| ---- | ---- | ---- |
| Location_000 | 0, 1 | 4.200.000 |
| Location_005 | 0, 1, 2, 3 | 4.200.000 |

We already know that only the second cluster can generate subclusters, therefore different valid options, so we will use said subcluster's options for the example.

```json

1. Determine current cost:
    - {3, ["Location_002", "Location_003",
        "Location_004", "Location_005", "Location_006"]}
    - Base costs = 5 * 42.000 = 210.000
    - Infra costs = (1) * 4.200.000 = 4.200.000
    - Total costs = 4.410.000

2. Calculate costs for first option:
    - {(3, ["Location_002", "Location_003"],
        ["Location_004", "Location_005", "Location_006"])},
    1. First subcluster's common measures:
        - Stability Wall (current):
            - Base costs = 2 * 42.000 = 84.000
            - Infra costs = 0
            - Total costs = 42.000
        - Cofferdam:
            - Base costs = 2 * 420.000 = 840.000
            - Infra costs = 0
            - Total costs = 840.000
        - The current reinfocement is cheaper
    2. Second subcluster's common measures:
        - Stability Wall (current):
            - Base costs = 3 * 42.000 = 126.000
            - Infra costs = (1) * 4.200.000 = 4.200.000
            - Total costs = 4.326.000
        - Cofferdam:
            - Base costs = 3 * 420.000 = 1.260.000
            - Infra costs = 0
            - Total costs = 1.260.000
        - Cofferdam will be cheaper.
    3. Subcluster's best option is cheaper than current:
        - {(3, ["Location_002", "Location_003"]),
        (4, ["Location_004", "Location_005", "Location_006"])}
        - Total cost = 42.000 + 1.260.000 = 1.302.000
        - Selected as option.

3. Calculate costs for second option:
    - {3, (["Location_002", "Location_003", "Location_004"],
        ["Location_005", "Location_006"])}
    1. First subluster's common measures
        - Stability Wall (current):
            - Base costs = 3 * 42.000 = 126.000
            - Infra costs = 0
            - Total costs = 126.000
        - Cofferdam:
            - Base costs = 3 * 420.000 = 1.260.000
            - Infra costs = 0
            - Total costs = 1.260.000
        - The current reinfocement is cheaper
    2. Second subluster's common measures
        - Stability Wall (current):
            - Base costs = 2 * 42.000 = 84.000
            - Infra costs = 0
            - Total costs = 84.000
        - Cofferdam:
            - Base costs = 2 * 420.000 = 840.000
            - Infra costs = 0
            - Total costs = 840.000
        - Cofferdam is cheaper
    3. Subcluster's best option is cheaper than selection:
        - {(3, ["Location_002", "Location_003", "Location_004"]),
            (4, ["Location_005", "Location_006"])}
        - Total cost = 126.000 + 840.000 = 966.000
        - Selected as option.

4. Update locations' selected reinforcement:
{
    (2, ["Location_000","Location_001",]),
    (3, ["Location_002","Location_003", "Location_004",]),
    (4, ["Location_005","Location_006", "Location_007",
          "Location_008","Location_009",]),
}
```

In this example we can therefore demonstrate the cost reduction. The last column represents the difference (positive means saved money):

- O.S. = Order strategy
- I.S. = Infrastructure priority strategy

| Location | (O.S.) reinforcement | (O.S.) cost | (I.S.) reinforcement | (I.S.) cost | Difference |
| ---- | ---- | ---- | ---- | ---- | ---- |
|Total | ---- | 6.090.084 | ----  | 2.226.840 | __+3.863.244__ |
|Location_000 | Soil reinforcement | 4.200.042 | Piping Wall | 420 | +4.199.622 |
|Location_001 | Soil reinforcement | 42 | Piping Wall | 420 | -378 |
|Location_002 | Stability Wall | 42.000 | Stability Wall | 42.000 | 0 |
|Location_003 | Stability Wall | 42.000 | Stability Wall | 42.000 | 0 |
|Location_004 | Stability Wall | 42.000 | Stability Wall | 42.000 | 0 |
|Location_005 | Stability Wall | 462.000 | Cofferdam | 420.000 | +42000 |
|Location_006 | Stability Wall | 42.000 | Cofferdam | 420.000 | -378000 |
|Location_007 | Cofferdam | 420.000 | Cofferdam | 420.000 | 0 |
|Location_008 | Cofferdam | 420.000 | Cofferdam | 420.000 | 0 |
|Location_009 | Cofferdam | 420.000 | Cofferdam | 420.000 | 0 |

####  Infrastructure priority (old approach) example

---------------
> **_Important!_** 
> This example is based on the first approach of this strategy and its steps might differ from the current solution. We left this example as it can help understanding the basic concepts of the strategy.
---------------
We will start by defining some unrealistic costs per reinforcement type for all locations* such as. For a more realistic scenario check the [subclustering example](#infrastructure-priority-subclustering-example):

| Index | Reinforcement type | base cost | infra cost | total cost |
| ---- | ---- |---- | ---- | ---- |
| 0 | Soil reinforcement | 42 | 420.000 | 420.042 |
| 1 | Vertical Piping Solution | 420 | 420.000 | 420.420 |
| 2 | Piping Wall | 4200 | 0 | 4200 |
| 3 | Stability Wall | 42.000 | 420.000 | 462.000 |
| 4 | Cofferdam | 420.000 | 0 | 420.000 |

---------------
> **_Important!_** 
> For example purposes we are applying the same infrastructure costs to all the locations. |However, in a real case these costs would vary per location (and per reinforcement type). So we can determine the cluster's reinforcement costs as `(total cost) * N locations`
---------------

Based on this data `Piping Wall` will be chosen **unless** any of the points in the cluster cannot apply it due to obstacles or other constraints, in which case it would end up settling for a `Cofferdam` reinforcement.

Let's see now the strategy steps using the results from the [clustering example](#clustering-example): 

```json
1. List of clusters:
    {
        (0, ["Location_000","Location_001",]),
        (3, ["Location_002","Location_003",
                "Location_004","Location_005",
                "Location_006",]),
        (4, ["Location_007","Location_008","Location_009",]),
    }

2. Iterate over each cluster:

2.1. First cluster is:
    { (0, ["Location_000","Location_001",]) }
    
    2.1.1. Get the current cost of using this cluster.
        - Total costs * N locations = `(420042) * 2 = 840084`

    2.1.2. Get cheaper common available measures:
        - Soil Reinforcement, (idx=0),
            - [Discard] Current selection.
        - Vertical Piping Solution, (idx=1),
            - Costs = `(420.420) * 2 = 840.840`
            - [Discard] Costs are higher than initial state.
        - Piping Wall, (idx=2),
            - Costs = `(4.200 + 0) * 2 = 8.400`
            - [Keep] Costs are cheaper than the initial state.
        - Stability Wall, (idx=3),
            - Costs = `(462.000) * 2 = 924.000`
            - [Discard] Costs are higher than initial state.
        - Cofferdam, (idx=3),
            - Costs = `(420.000) * 2 = 840.000`
            - [Keep] Costs are cheaper than the initial state, keep.

    2.1.3. Set the cheapest common available measure per cluster:
        - Piping wall < Cofferdam < Soil reinforcement (current)
        - Piping wall is the new reinforcement for this cluster.
    
    - Result: {(2, ["Location_000","Location_001",])}

2.2. Second cluster is:
    {(3, ["Location_002","Location_003",
            "Location_004","Location_005",
            "Location_006",])}

    2.3.1. Get the current cost of using this cluster.
        - Total costs * N locations = `(462.000) * 5 = 2.310.000`
    
    2.3.2. Get cheaper common available measures.
        - Soil Reinforcement, (idx=0),
            - [Discard] Not present at "Location_003", "Location_004".
        - Vertical Piping Solution, (idx=1),
            - [Discard] Not present at "Location_003", "Location_004".
        - Piping Wall, (idx=2),
            - [Discard] Not present at "Location_003", "Location_004".
        - Stability Wall, (idx=3),
            - [Discard] Current selection.
        - Cofferdam, (idx=3),
            - Costs = `(420.000) * 5 = 2.100.000`
            - [Keep] Costs are cheaper than the initial state.
    
    2.3.3. Set the cheapest common available measure per cluster:
        - Cofferdam < Stability wall
        - Cofferdam is the new reinforcement for this cluster.
    
    - Result : {(4, ["Location_002","Location_003",
                    "Location_004","Location_005",
                    "Location_006",])}

2.3. Third cluster is:
    { (4, ["Location_007","Location_008",
            "Location_009",])}}

    2.3.1. Get the current cost of using this cluster.
        - Total costs * N locations = `(420.000) * 3 = 1.260.000`

    2.3.2. Get cheaper common available measures.
        - Cofferdam, (idx=4),
            - Current selection.

    2.3.3. Set the cheapest common available measure per cluster:
        - Only cofferdam available,
        - No further action.

    - Result: {(4, ["Location_007","Location_008",
                    "Location_009",])}

2.4. Resulting clusters:
    {
        (2, ["Location_000","Location_001",]),
        (4, ["Location_002","Location_003",
                "Location_004","Location_005",
                "Location_006","Location_007",
                "Location_008","Location_009",]),
    }
```

With this, we went from:

- Initial costs: `(420.042) * 2 + (462.000) * 5 + (420.000) * 3 = 4.410.084`, to
- Final costs: `(4.200) * 2 + (420.000) * 8 = 3.368.400`

Which would amount to a total save of **1.041.684€**

