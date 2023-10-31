# Koswat

Koswat module is divided in submodules, each focusing on a specific set of tasks. On the root you will find the fundamental __init__.py and __main__.py as well as a the `KoswatHandler` class in the file koswat_handler.py.

Available modules as for the time of writing of this file:

- [configuration](./configuration/README.md) Module related to the settings and setup of a Koswat analysis.
- [core](./core/README.md) Module containing the core functionality (mostly protocols and generic functionality).
- [cost_report](./cost_report/README.md) Module containing the analysis of KOSWAT. Here we trigger the generation of reinforcement profiles that will be applied to the analysis when and if suitable for the given koswat environment.
- [dike](./dike/README.md) Module containing the representation of a Dike in Koswat and its related types and properties.
- [dike_reinforcements](./dike_reinforcements//README.md) Module related to the definition and calculation of reinforcement profiles.
- [strategies](./strategies/README.md) Module containing the different selection criteria of reinforcement profile for a location.
- [plots](./plots/README.md) Module containing plotting export functionality.