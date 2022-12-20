## v0.11.0 (2022-12-20)

### Feat

- **koswat/koswat_handler.py**: We now accept a log_output argument to specify the directory where to save the koswat run log.

## v0.10.0 (2022-12-20)

### Feat

- **koswat/configuration/converters**: Created converters fom to dom
- **koswat/configuration/io/converters/**: Added configuration converters for the analysis section. We can now generate input profiles from the ini files
- **koswat/configuration/io/csv**: Added import of KoswatInputProfiles
- **KoswatHandler;KoswatLogger**: Added handler and logger for koswat runs from CLI

### Fix

- **koswat/geometries/calc_library.py**: We now order the points of the geometries so that calculations can be done correctly
- **koswat/calculations**: Corrected profile calculation for all types and their tests. These changes come directly from Peter de Grave
- **koswat/configuration/io/koswat_run_settings_importer.py**: corrected filtering of selected input profiles
- **koswat_dike_locations_shp_reader.py**: Fixed enumerating a filtered list instead of filtering after enumerating
- **KoswatSurroundingsConverter**: Fixed return as it was only giving the latest mapped FOM
- **configuration/io/converters**: Fixed return of data and adapted tests
- **koswat_analysis_converter.py**: Small fix to converter
- **koswat_General_settings.py**: Fix validation for surroundings
- **koswat/calculations**: Fixed calculations due to new profile input property
- **KoswatMaterialType**: Minor fix regarding usage of new KoswatMaterialType
- **KoswatMaterialType**: Adapted code to use the enum instead of strings

### Refactor

- **koswat/configuration/io**: Moved converters into io
- **koswat/dike/surroundings/io/shp**: Moved shp reader and fom to surroundings module
- **koswat/configuration**: Integrating mapping of files to fom's during settings import
- **koswat/dike/surroundings/io**: Moved previous CSV reader into a concrete module within dike/surroundings. Created protocols for csv reading so it can be repurposed
- **KoswatMaterialType**: Made koswat material into an enum. Adapted code overall in the source

## v0.9.0 (2022-12-12)

### Feat

- **KoswatGeneralSettings**: Created DOM for koswat general settings configuration
- **KoswatConfigurationIniImporter**: We can now map all different ini fom classes to the config class
- **koswat/configuration**: Created koswat configuration module and related class KoswatConfiguration to encapsulate all require information for a koswat analysis
- **KoswatScenarioIniFom**: It is now possible to read a KoswatScenarioIniFom from file
- **KoswatDikeSelectionIniFom**: It is now possible to read a Dike Selection INI file into its corresponding FOM
- **KoswatCostsIniFom**: Added logic to fully implement reading of a KoswatCostsIniFom file
- **KoswatCostsIniFom**: Added koswat costs ini file
- **KoswatIniReader**: Created koswat ini reader and initial approach to reading the general Koswat INI file

### Fix

- **KoswatCosts**: Added class conversion to dictionary

### Refactor

- **koswat/configuration/models**: Moved configuration data object models into their own module. Fixed / grouped imports
- **KoswatDikeSelection**: Koswat dike selection now implements a new type KoswatDikeSelectionTxtFom with related reader
- **koswat_scenario**: Moved koswat scenario into koswat/configuration
- **koswat/io**: Adapted export / import fom protocol

## v0.8.2 (2022-12-09)

### Fix

- **KoswatLayerProtocol**: we now have two different geometries for a layer, so that the profile with the layer and the stand alone representation of it are better reached

## v0.8.1 (2022-11-21)

### Fix

- **SummaryMatrixCsvExporter**: We now provide NANs when volume parameter is not defined
- **summary_matrix_csv_exporter**: We now correctly export all required information to the csv for the user

## v0.8.0 (2022-11-19)

### Feat

- **KoswatPlotContext**: Created plot context handler so it's easier to initialize and close plots

## v0.7.0 (2022-11-18)

### Feat

- **koswat/cost_report/io/plots/**: Added module for cost_report export plots logic
- **koswat_profile_plot.py**: We can now set a unique color for layers_wrapper and profile plots
- **koswat/plots/dike/**: Extracted dike plotting logic into separate classes
- **koswat/plots/geometries**: Created module with plotting for regular geometries from shapely

### Fix

- **koswat/plots/utils.py**: Replaced wrapper as it is not a good approach
- **characteristic_points_builder.py**: Resolved a circular dependency

### Refactor

- **koswat/calculations/io/**: Extracted plot exporters from calculations into their corresponding directory
- **koswat/plots**: Create concrete module for plotting
- **koswat/io**: Moved io files into their corresponding modules

## v0.6.0 (2022-11-11)

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
