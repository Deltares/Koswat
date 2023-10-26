# Strategies

This modules contains the logic to choose which measure will be applied for a given dike traject. This happens through a series of iterations:
1. For each point (meter) in the traject, determine which measures can be applied to it.
2. Choose one of the available measures based on the chosen [strategy](#order-based-default). When no measure is available the most restrictive will be chosen (`CofferDam`).
3. Apply a buffer (`constructie_overgang`) for each one of the measures.
4. Check if the minimal distance between constructions is met (`constructie_afstand`), otherwise change it into one of the measures next to it.
5. Repeat 4 until all measures have enough distance between themselves.

## Available strategies.

### Order based (default). 
A strategy is chosen based on a fix priority order:
1. `SoilReinforcement`
2. `PipingWallReinforcement`
3. `StabilityWallReinforcement`
4. `CofferDamReinforcement`

