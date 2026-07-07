# Scenario invoer

Om de versterkingen van de dijksecties te definiëren wordt gewerkt met scenario’s. De versterkingsopgave wordt niet door KOSWAT zelf bepaald, maar dient te worden opgegeven door de gebruiker of deze volgt uit andere tools (bijvoorbeeld OKADER). De instelling [_[scenario_invoer]_](h04_projectdefinitie.md#analyse) in de project-json verwijst naar een map waarin de scenariobestanden per dijksectie zijn opgeslagen in afzonderlijke json-files, wederom met een naam die overeenkomt met de unieke dijksectienaam, dus {dijksectie}.json. In een bestand kunnen per dijksectie één of meerdere scenario’s worden gedefinieerd als volgt:

```json
{
    "scenario_1": {
        "dh": 0.5,
        "ds": 6,
        "dp": 15
    },
    "scenario_2": {
        "dh": 1,
        "ds": 9,
        "dp": 25,
        "Buitentalud": 4,
        "Kruinbreedte": 10
    }
}
```

Per scenario geven we in ieder geval (verplicht) de opgave ten aanzien van hoogte _[dh]_, en de benodigde toename van de dijkbasis ten aanzien van macrostabiliteit _[ds]_ en piping _[dp]_ op, zie ook [Figuur 1](h02_methode.md#figuur-1). Optioneel kan hierbij ook een nieuwe helling van het buitentalud _[buitentalud]_ (in cotangens, dus 1:x) worden opgegeven (in het geval van een buitentaludverflauwing) en een aanpassing van de breedte van de dijkkruin _[kruinbreedte]_ (in m).
