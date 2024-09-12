# Koswat strategies

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

1. `SoilReinforcementProfile`
2. `VPSReinforcementProfile`
3. `PipingWallReinforcementProfile`
4. `StabilityWallReinforcementProfile`
5. `CofferDamReinforcementProfile`

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
    ],
    "VSPReinforcementProfile": [
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

__Note__: Masks' values are the position of a reinforcement type in the [reinforcement's order list](#reinforcment-order). So a location with `CofferDamReinforcementProfile` will have a 4 at the mask's position, whilst a `SoilReinforcementProfile` will have a 0 instead (remember in Python indexing starts with 0).

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
        [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
    "PipingWallReinforcementProfile": 
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    "StabilityWallReinforcementProfile": 
        [-1, -1,  3,  3,  3,  3 ,-1, -1, -1, -1],
    "CofferDamReinforcementProfile": 
        [-1, -1, -1, -1, -1, -1 ,-1,  4,  4,  4],
}

3. Merge all masks and select their maximum value:
[0, 0, 3, 3, 3, 3, 0, 4, 4, 4]

4. Update the cluster's locations:
{
    "SoilReinforcementProfile": [
        "Location_000",
    ],
    "VPSReinforcementProfile": [
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
[
    (0, ["Location_000","Location_001",]),
    (3, ["Location_002","Location_003","Location_004","Location_005",]),
    (0, ["Location_006",]),
    (4, ["Location_007","Location_008","Location_009",]),
]

2. Iterate over each reinforcement type:
2.1. Target is "SoilReinforcementProfile" (idx=0), non-compliant clusters:
    [
        (0, ["Location_006",]),
    ]
    2.1.1. Length = 1.
    2.1.2. Get a stronger neighbor,
        - Left-neighbor reinforcement type = 3,
        - Right-neighbor reinforcement type = 4,
        - Left-neighbor is selected.
    2.1.3. Move locations to stronger neighbor.
    [
        (2, ["Location_002", ... ,"Location_006",]),
        (0, ["Location_006",]),
    ]
    2.1.4. Remove the current cluster from the available list.

2.2. Target is "PipingWallReinforcementProfile" (idx=3), 
    - All clusters are compliant at this point.
2.3. Target is "StabilityWallReinforcementProfile" (idx=4),
    - All clusters are compliant at this point.
2.5. "CofferDamReinforcementProfile" won't be checked as it's the last
reinforcement profile type, therefore the strongest.

Resulting cluster:
    [
        (0, ["Location_000","Location_001",]),
        (3, ["Location_002","Location_003","Location_004","Location_005","Location_006",]),
        (4, ["Location_007","Location_008","Location_009",]),
    ]
```