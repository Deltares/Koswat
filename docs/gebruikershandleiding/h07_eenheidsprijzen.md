# Eenheidsprijzen

De instelling [_[eenheidsprijzen]_](h04_projectdefinitie.md#analyse) in de project-json geeft een verwijzing naar het bestand met eenheidsprijzen die in KOSWAT gehanteerd worden. Dit bestand wordt meegeleverd met KOSWAT, en heeft een structuur zoals weergegeven in onderstaand kader. De KOSWAT-kostendatabases (eenheidsprijzen en opslagfactoren) worden onderhouden en regelmatig van een update voorzien door Rijkswaterstaat Grote Projecten en Onderhoud (RWS GPO). Hierbij worden door GPO inzichten en gegevens uit een groot aantal referentieprojecten gebruikt.

De eenheidsprijzen sluiten aan bij de berekende hoeveelheden. Eenheidsprijzen van constructieve elementen worden beschreven aan de hand van een formule als functie van de wandlengte met een aantal constanten. De functie is gefit door een aantal onderliggende discrete kostenramingen. 

Een nadere beschrijving van de gehanteerde SSK raminssystematiek inclusief alle gehanteerde eenheidsprijzen en opslagfactoren die onder de verschillende kopjes worden gedefinieerd wordt gegeven in [Kostenberekening volgens SSK](h10_sskmethodiek.md).

```json
{
    "eenheidsprijzen": { "prijspeil": 2023 },
    "kostendijkprofiel": { … },
    "kostenverticaalzanddichtgeotextiel": { … },
    "kostencbwand": { … },
    "kostendamwandonverankerd": { … },
    "kostendamwandverankerd": { … },
    "kostendiepwand": { … },
    "kostenkistdam": { … },
    "kosteninfrastructuur": { … },
    "kostenopslagfactoreninclbtw": { … },
    "kostenopslagfactorenexclbtw": { … }
}
```
