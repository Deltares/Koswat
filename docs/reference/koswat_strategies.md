# Koswat strategies

Koswat can determine which is the "best" reinforcement type for a dike traject based on different selection criteria that we name "strategies" (`StrategyProtocol`).

A strategy requires a strategy input (`StrategyInput`), this input contains information over which measures are available at each location as well as what's the __minimal buffer__ (`structure_min_buffer`) and __minimal length__ (`structure_min_length`)  for each measure type.

By default a strategy is applied as follows:

1. For each point (meter) in the traject, determine which measures can be applied to it.
2. Choose one of the available measures based on the chosen [strategy](#order-based-default). When no measure is available the most restrictive will be chosen (`CofferDam`).
3. Apply a buffer (`structure_min_buffer`) for each one of the measures.
4. Check if the minimal distance between constructions is met (`structure_min_length`), otherwise change it into one of the measures next to it.
5. Repeat 4 until all measures have enough distance between themselves.
6. Return list of mapped locations (`list[StrategyLocationReinforcement]`).

## Available strategies

### Order based (default)

This strategy is the first an default of all defined strategies. Its criteria is based on a pre-defined ['order'](#measure-order) of each reinforcement. In steps, it can be seen as:

1. Pre-selection of a location's available reinforcement based on said order, when a location does not have any "available" reinforcement, then the last measure's order will be pre-selected.
2. [Clustering](#measure-clustering) of all locations by their pre-selected measure.
3. [Measure buffering](#measure-buffering) to each of the clusters.
4. [Measure minimal distance](#measure-minimal-distance) to the resulting clusters from the previous step.

#### Measure order
The predefined (hardcoded) reinforcement's order is as follows:

1. `SoilReinforcementProfile`
2. `PipingWallReinforcementProfile`
3. `StabilityWallReinforcementProfile`
4. `CofferDamReinforcementProfile`

#### Measure clustering

We create measure-location clusters for the whole traject.

A cluster represents a measure that its "selected" for a series of continuous locations. This means locations that are next to each other sharing the same measure type (`Type[ReinforcementProfileProtocol]`).

##### Clustering example
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

#### Measure buffering

Given a [measure cluster](#measure-clustering), we will create a dictionary of masks of size `NM` where `N` (the keys) is the number of available measure types (`Type[ReinforcementProfileProtocol]`) and `M` the number of available locations. 

__Note__: Masks' values are the position of a reinforcement type in the [measure's order list](#measure-order). So a location with`CofferDamReinforcementProfile` will have a 3 at the mask's position, whilst a `SoilReinforcementProfile` will have a 0 instead (remember in Python indexing starts with 0).

Steps that are followed:

1. Initialize the dictionary masks with all values to -1.

2. Iterate over the clusters list, and for each entry:

    1. Select the mask to update using the cluster's measure type (cluster's key).

    2. Update the indices representing the cluster's locations (cluster's values) with the matching value for this cluster's key (see previous __note__).

    3. Add a buffer (`StrategyInput.structure_min_buffer`) by updating the adjacent's positions of this cluster with the same values as in step 1. 

3. Merge all masks into a 1-dimensional array where the cell's value is the maximum between the available masks.
    - This is done to prevent that a buffer of a "higher" demanding measure such as `CofferDamReinforcementProfile` is replaced by a "weaker" one.
 
4. Update the locations with their new associated reinforcement. The resulting mask contains the index of the measure to be applied in the [measure's order](#measure-order).


##### Buffering example

One simplified example, based on the [clustering example](#clustering-example), and using a buffer value of "1". This example is also tested in the `tests.strategies.order_strategy.py` test file.

```json
1. Initialize the masks based on the provided clusters:
{
    "SoilReinforcementProfile": 
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
        [0, 0, 0, 0, 0, 0 ,0, 0, 0, -1],
    "PipingWallReinforcementProfile": 
        [-1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1],
    "StabilityWallReinforcementProfile": 
        [-1, -1, 2, 2, 2, 2 ,-1, -1, -1, -1],
    "CofferDamReinforcementProfile": 
        [-1, -1, -1, -1, -1, -1 ,-1, 3, 3, 3],
}

3. Merge all masks and select their maximum value:
[0, 0, 2, 2, 2, 2, 0, 3, 3, 3]

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

#### Measure minimal distance

Given a [measure cluster](#measure-clustering), ideally done after applying [buffering](#measure-buffering), we will now proceed to change the pre-selected measure of all those clusters who contain less locations than required by the describing property. We do this by updating their type with a "stronger" one.

__Note__: 
- We define a _non-compliant_ cluster as a cluster that does not contain as many locations as defined by the minimal length requirement (`structure_min_length`).
- We also define a _non-compliant exception_ when a cluster does not meet said requirement but the adjacent clusters are of a lower reinforcement type.

1. Do `N` iterations where `N` is the initial number of _non compliant_ clusters.
2. For each cluster:
    0. If it's _non-compliant_ move to step 2.1, otherwise check the next cluster (2.0).
    1. Determine its current value as done for the masks of [buffering](#measure-buffering).
    2. Select the strongest measure type between the current cluster's value and the previous cluster's value (-1 if there is no previous cluster).
    3. Select the strongest measure type between the current cluster's value and the next cluster's value (-1 if there is no next cluster).
    4. Select the weakest measure type between the results of step 2.2 and 2.3.
        - If the new value is the same, mark as "exception".
    5. If the current value has changed, then update the location's selected measure. 
        - In addition, if the new value is of the next's cluster then move the locations already to said luster to prevent it from being _non compliant_.
3. Determine if clusters have been corrected:
    * if the number of non-compliant clusters is 0, or
    * if there are as many non-compliant as exception-clusters identified, or
    * if there are still `N` iterations already happened, then we are done.
    * otherwise, go back to step 2.
4. All clusters should now meet the requirements (unless not possible)

##### Minimal distance example

One simplified example, based on the [buffering example](#buffering-example), and using a minimal distance of "5", can be as follows:

```json
1. Determine initial non-compliant clusters, in our case (strcture_min_length=5), no clusters fulfill this rule, so we require a maximum of 4 iterations as we have 4 clusters.

2. During iteration 1:

    1. Check first cluster ("SoilReinforcementProfile"):
        0. Non-compliant (length=2)
        1. Current value = 0,
        2. Previous value = 1,
        3. Next value = 2,
        4. Determine new value = 2,
        5. Update value and next cluster:
            "StabilityWallReinforcementProfile": [
                "Location_000",
                "Location_001",
                "Location_002",
                "Location_003",
                "Location_004",
                "Location_005",
            ],
    2. Check second cluster ("StabilityWallReinforcementProfile"):
        0. It is now compliant (length=6), move to next cluster.
    3. Check third cluster:
        0. Non-compliant (length=1)
        1. Current value = 0,
        2. Previous value = 2,
        3. Next value = 3,
        4. Determine new value = 2,
        5. Update value (but not moved to previous cluster):
            "StabilityWallReinforcementProfile": [
                "Location_000",
                "Location_001",
                "Location_002",
                "Location_003",
                "Location_004",
                "Location_005",
            ],
            "StabilityWallReinforcementProfile": [
                "Location_006", 
            ],
    4. Check fourth cluster:
        0. Non-compliant (length=3)
        1. Current value = 3,
        2. Previous value = 2,
        3. Next value = -1,
        4. Determine new value = 3, mark as exception.
        5. Do not update value:
            "CofferDamReinforcementProfile": [
                "Location_007",
                "Location_008",
                "Location_009",
            ],
    5. Return number of non-compliant exceptions (1)
3. Get new clustering and number of non-compliants:
    {
        "StabilityWallReinforcementProfile": [
            "Location_000",
            "Location_001",
            "Location_002",
            "Location_003",
            "Location_004",
            "Location_005",
            "Location_006", 
        ],
        "CofferDamReinforcementProfile": [
            "Location_007",
            "Location_008",
            "Location_009",
        ],
    }
4. All non-compliant clusters are exception. Finish.
```