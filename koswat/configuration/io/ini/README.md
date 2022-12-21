# Koswat Configuration IO ini.

__Important!__ As explained in the `koswat.core.io.ini` module, we do not required concrete ini readers. Therefore the parsing logic is implemented within the instances of `KoswatIniFomProtocol`.
An exception to the above rule is with `KoswatScenarioListIniDirReader` as the setting pointing to its value leads to a directory containing more ini files.