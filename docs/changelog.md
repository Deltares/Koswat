## Unreleased

### Feat

- **VolumeCalculationParameters**: Included all operations required to for volume calculation
- **ReinforcementProfileProtocol**: Added new property to retrieve the new ground level surface
- **OutsideSlopeReinforcementLayersWrapperBuilder**: Added builder for for the outside slope reinforcement layers wrapper
- **StandardReinforcemetnLayersWrapperBuilder**: Added logic to generate the geometries of a standard reinforcement dike
- **ReinforcementLayersWrapper**: We now have dedicated builders for the LayersWrapper associated with a Reinforcement
- **ReinforcementProfileBuilderProtocol**: Created protocol for better hierarchy
- **CoatingLayerCostReport**: Extended usage of previous StandardLayerCostReport so that other reinforcements can also use it
- Added logic to extract the surface of a layer
- **LayerCostReportProtocol;StandardLayerCostReportBuilder**: Extracted standard layer cost report builder logic into separate class. Added protocol to represent the layer cost reports
- **koswat/geometries; standard_layer_cost_report**: Implemented logic for StandardLayer cost calculation
- **OutsideSlopeReinforcementProfileProtocol;StandardReinforcementProfileProtocol**: Added protocols to represent the different types of reinforcement - per volume; Added tests for factory
- **LayerCostReportbuilderFactory**: Added logic to retrieve the corresponding LayerCostReportBuilderProtocol; Adapted tests and related imports
- **LayerCostReportBuilderFactory**: Introduced layer cost report builder factory for the different types of volume calculators available

### Fix

- **PipingWallReinforcementProfileCalculation**: Solved wrong calculation of the Length Piping Wall
- **StabilityWallReinforcementProfileCalculation**: Corrected calculation of the length stability wall property
- StabilityWall calculation was not properly mapped
- **OutsideSlopeProfileCostReportBuilder**: Now we properly calculate the added core layer
- **OutsideSlopeProfileCostReportBuilder**: Calculation of the 'kistdam' layers is now done properly

### Refactor

- **koswat/calculations**: Moved calculations into their respecitve reinforcement types
- Starting to move logic of added / removed layers to the calculation module
- **cost_report**: Moved layer factory to profile factory as the logic should be in a higher level

## v0.5.1 (2022-10-11)

### Fix

- **SummaryMatrixCsvExporter**: We now export the locations in order of import

## v0.5.0 (2022-10-11)

### Feat

- **SummaryMatrixCsvExporter**: We now also export the CsvFom into a file
- **SummaryMatrixCsvFom;SummaryMatrixCsvExporter**: Added Summary Matrix Csv Fom and Exporter initial logic
- **CofferDamInputProfile**: Added concrete input profile for CofferDamReinforcementProfile
- **calculations/cofferdam;CofferdamReinforcementProfileCalculation;CofferdamReinforcementProfile**: Added Cofferdam Reinforcement Profile and Calculation to the calculations module. Added information to the summary to also build their report.
- **StabilityWallInputProfile;StabilityWallReinforcementProfileCalculation**: Created both concrete input profile and profile calculation for StabilityWallReinforcementProfile
- **StabilityWallReinforcemetnProfile**: Added StabilityWallReinforcementProfile type
- **PipingWallInputProfile**: Created dedicated input profile for PipingWall
- **KoswatInputProfileProtocol**: Made a Koswat Input Profile protocol to manage better concrete input profiles. Adapted existing code and tests
- **PipingWallReinforcementProfileCalculation**: Added calculation for PipingWall Reinforcement Profile
- **PipingWall**: Added PipingWallReinforcementProfile class
- **ReinforcementProfileProtocol**: Introduced ReinforcementProfileProtocol as a sub protocol of KoswatProfileProtocol. Adapted existent classes and tests. Moved existing calculations into calculations\soil

### Fix

- **CofferdamReinforcementProfileCalculation**: P4 x coordinate set to 0 for all builds from this calculation
- **KoswatProfileBuilder**: Removed paramater from build method to make it complier to the BuilderProtocol

## v0.4.0 (2022-10-07)

### Feat

- **MultiLocationMultiProfileCostBuilder**: Added new report to summarize reports of profile per location.
- **ListMultiLocationProfileCostBuilder**: It is now possible to make a report for multiple locations and multiple possible profiles
- **KoswatBuildingsPolderside.get_classify_surroundings**: We can now retrieve all points classified by their distance to the closest building
- **KoswatSurroundings**: Added wrapper class for surroundings and a builder for it. Extended other `koswat/surrounding` builder classes to be initialized from files.
- **KoswatCsvFomBuilder;Koswat\surroundings**: We can now map the csv data to surrounding points and their distances to buildings. Adapted related code
- **KoswatCsvReader**: It is possible to read a CSV file into a `FileObjectModelProtocol` instance of `KoswatCsvFom`. Added new methods to fom and reader protocols, adapted related classes
- **KoswatShpReader**: Added KoswatShpReader to read from a shapefile. Added reader protocol and io module

### Refactor

- **koswat/surroundings**: Moved files into separate module
- **dike**: Renamed profiles module to dike for a more coherent approach
- **cost_report**: Moved directories into a better  tree structure
- **koswat/cost_report**: Seggregated module into builders and reports.
- **koswat/cost_report**: Extracted reports into their own modules
- **ProfileCostBuilder**: Profile cost builder is independent of the profile type. All types of new profiles are calculated and then a report is done for each of them"

## v0.3.0 (2022-10-03)

### Feat

- **CharacteristicPoints**: Created characteristic points to replace the previous 'ProtocolSide' related classes. Introduced builder to allow initial or reinforced profile creation
- **KoswatLayersBuilder**: We now can create layers based on the provided depth
- **ProfileReinforcementCostBuilder**: Generates a cost report for the new profile based on the extra required volume
- **KoswatReport**: Added KoswatReport to generate costs overviews
- It is now possible to create layers from a dictionary
- **koswat_layers;koswat_profile_builder**: Added new class to represent the layers of a profile, their material and so on.
- **koswat/calculations**: Added profile reinforcement calculation
- **koswat/profiles**: Added koswat profiles and related properties. They can now be built from an input profile

## v0.2.0 (2022-09-27)

### Feat

- **koswat**: Initial commit. Created Initial architecture and basic tests for the structure given. Added version control through commitizen
