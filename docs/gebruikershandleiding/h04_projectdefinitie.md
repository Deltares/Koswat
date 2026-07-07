# Definitie van een KOSWAT project
Een KOSWAT-project wordt gedefinieerd in verschillende *.json bestanden. Overkoepelend wordt een project-json opgesteld die wordt gebruikt in het [aanroepen van de berekening](h03_installatie.md#berekening). Deze project-json is verdeeld in een aantal blokken met invoer die in de volgende paragrafen beschreven worden. Als basis kunnen de invoerbestanden gebruikt worden in het voorbeeldproject dat beschikbaar is gesteld met KOSWAT. Paden naar bestanden en folders kunnen door de gebruiker worden aangepast en kunnen zowel absoluut als relatief ten opzichte van de project-json opgegeven worden.

In het bestand worden de globale rekeninstellingen gedefinieerd die in principe voor het gehele project geldig zijn. Voor een aantal instellingen is het mogelijk om hier per dijksectie van af te wijken, zie daarvoor de beschrijving van de [dijksectie invoer](h05_dijksectie-invoer.md).

Onderstaand is de structuur van de project-json weergegeven. De verschillende blokken worden in het vervolg van deze pagina uitgewerkt.

```json
{
    "analyse": { … },
    "dijkprofiel": { … },
    "grondmaatregel": { … },
    "verticalepipingoplossing": { … },
    "kwelscherm": { … },
    "stabiliteitswand": { … },
    "kistdam": { … },
    "omgeving": { … },
    "infrastructuur": { … }
}
```

## Analyse
<a id="analyse"></a>
In het blok _analyse_ worden allereerst de algemene instellingen gegeven voor het KOSWAT project, als volgt:

```json
"analyse": {
    "dijksectie_ligging": "dijksectie_ligging/dijksecties.shp",
    "dijksecties_selectie": "dijksecties_selectie.txt",
    "dijksectie_invoer": "dijksectie_invoer",
    "scenario_invoer": "scenarios",
    "eenheidsprijzen": "eenheidsprijzen_2022.json",
    "omgevingsdatabases": "omgeving",
    "uitvoerfolder": "KOSWAT_WV21_DR10_15_48_uitvoer",
    "btw": true
},
```

#### Dijksectie ligging en selectie
<a id="dijksectie-ligging"></a>
Met de instelling _[dijksectie_ligging]_ wordt verwezen naar de shapefile waarin de ligging van de dijksecties gedefinieerd is die in het KOSWAT-project beschouwd kunnen worden. Bij het opstellen van de shapefile met dijksecties wordt uitgegaan van een template van de ligging van normtrajecten. Deze template wordt met KOSWAT meegeleverd. De [omgevingsdatabases](h08_omgevingsdatabases.md) die in KOSWAT gebruikt worden zijn eveneens exact op deze ligging gebaseerd. Het is in de analyses noodzakelijk dat de dijksecties en omgevingsdatabases met elkaar overeen komen qua ligging.

De dijksectie-indeling wordt gemaakt door de meegeleverde template verder op te knippen in een GIS pakket (ArcGIS, QGIS, oid), en de dijksecties daarbij een unieke naam[^6] te geven in het veld “Dijksectie”. De attribute table bij de shapefile bevat naast het veld “Dijksectie” ook de velden “Traject”, “Subtraject” en “Lengte”. De lengte (in meter) dient na het opknippen opnieuw berekend te worden. De velden Traject en Subtraject verwijzen naar de betreffende delen van de omgevingsdatabases en mogen <u>niet</u> gewijzigd worden.

Het bijbehorende invoerbestand _[dijksecties_selectie]_ verwijst naar een eenvoudig tekstbestandje (*.txt) waarin de dijksecties gedefinieerd zijn waarmee we in het project gaan rekenen volgens onderstaande structuur. Dit hoeven niet alle dijksecties te zijn die in de shapefile gedefinieerd zijn, we kunnen hiermee een specifieke selectie maken.

```text
dijksectie_1
dijksectie_2
etc.
```

#### Dijksectie invoer
<a id="dijksectie-invoer"></a>
De instelling _[dijksectie_invoer]_ verwijst naar een map waarin de invoerbestanden met rekeninstellingen per dijksectie zijn opgeslagen in afzonderlijke json-files. De json-files in deze map hebben een naam die exact overeenkomt met de unieke dijksectienaam die is vastgelegd in de shapefile. De inhoud van de invoerbestanden wordt beschreven in [Dijksectie invoer](h05_dijksectie-invoer.md).

#### Scenario invoer
<a id="scenario-invoer"></a>
Om de versterkingen van de dijksecties te definiëren wordt gewerkt met scenario’s. De versterkingsopgave wordt niet door KOSWAT zelf bepaald, maar dient te worden opgegeven door de gebruiker of deze volgt uit andere tools (bijvoorbeeld OKADER). De instelling _[scenario_invoer]_ verwijst naar een map waarin de scenariobestanden per dijksectie zijn opgeslagen in afzonderlijke json-files, wederom met een naam die exact overeenkomt met de unieke dijksectienaam. In een bestand kunnen per dijksectie één of meerdere scenario’s worden gedefinieerd. De inhoud van de scenario-files wordt beschreven in [Scenario invoer](h06_scenario-invoer.md).

#### Eenheidsprijzen
<a id="eenheidsprijzen"></a>
De rekeninstelling _[eenheidsprijzen]_ geeft een verwijzing naar het bestand met de eenheidsprijzen die in KOSWAT gehanteerd worden. Dit bestand wordt standaard meegeleverd met KOSWAT. Zie [Eenheidsprijzen](h07_eenheidsprijzen.md) voor het gehanteerde format.

Met de rekeninstelling _[btw]_ wordt aangegeven of inclusief (waarde _true_) of exclusief btw (waarde _false_) wordt gerekend.

#### Omgevingsdatabases
<a id="omgevingsdatabases"></a>
KOSWAT werkt met omgevingsdatabases. Met deze rekeninstelling wordt aangegeven waar deze databases opgeslagen zijn. Meer configuratie wordt gedefinieerd in het blok [Omgeving](#omgeving) in de project-json, meer informatie over de omgevingsanalyses in het algemeen is te vinden in [Omgevingsdatabases](h08_omgevingsdatabases.md).

#### Uitvoerfolder
<a id="uitvoerfolder"></a>
Deze rekeninstelling spreekt voor zich, in deze folder wordt de uitvoer van de KOSWAT analyses opgeslagen per dijksectie en per doorgerekend scenario. Zie [KOSWAT uitvoer](h09_uitvoer.md) voor een nadere beschrijving van de uitvoerfiles die worden weggeschreven.

## Dijkprofiel
<a id="dijkprofiel"></a>
In de project-json worden in het blok _dijkprofiel_ de globale instellingen rondom het dijkprofiel gedefinieerd, die in principe gelden voor het hele project. Van deze globale instellingen kan per dijksectie worden afgeweken, zie hiervoor de invoerbestanden per sectie in [Dijksectie invoer](h05_dijksectie-invoer.md). In deze sectie-specifieke bestanden dient sowieso het dijkprofiel in de uitgangssituatie te worden gedefinieerd, al kunnen we er ook voor kiezen om een default profiel te specificeren voor alle dijksecties in onderstaand blok.

Algemene instellingen die in dit blok opgenomen kunnen worden:

```json
"dijkprofiel": {
    "dikte_graslaag": 0.3,
    "dikte_kleilaag": 0.5,
    "factorzetting": 1.2,
    "grondaankoop_bebouwd": 200,
    "grondaankoop_onbebouwd": 10
}
```

De factoren _[dikte_graslaag]_ en _[dikte_kleilaag]_ beschrijven de opbouw van het dijklichaam in verschillende lagen. Zie [Grondwerk](h10_sskmethodiek.md#grondwerk) voor een beschrijving hoe deze lagen worden behandeld in de berekening van volumes en kosten.

De instelling _[factorzetting]_ geeft aan hoeveel extra hoogte aangebracht dient te worden om zetting van de ondergrond ten gevolge van het gewicht van het extra aangebrachte grondlichaam te compenseren, een factor van 1,2 betekent hier 20% extra kruinverhoging. Let op: deze factor dient nog volledig doorgevoerd te worden in de berekening (2026).

Met de factoren _[grondaankoop_bebouwd]_ en _[grondaankoop_onbebouwd]_ worden de vierkantemeter-prijzen (in €/m2 excl. opslagen en btw) gegeven van de aankoop van grond in bebouwd en onbebouwd (agrarisch) gebied. In geval van een grondmaatregel wordt ervan uit gegaan dat dit veelal in onbebouwd gebied is. Voor de zwaardere constructieve maatregelen (stabiliteitswand, kistdam) wordt uitgegaan van bebouwd gebied (immers, je treft deze maatregelen niet voor niets). Bij een kwelscherm (lichtste constructieve maatregel) wordt met een gemiddelde gerekend.

## Grondmaatregel
<a id="grondmaatregel"></a>
In het blok grondmaatregel worden de instellingen gegeven die gelden specifiek voor de versterkingsmaatregel in grond.

```json
"grondmaatregel": {
    "actief": true,
    "opslagfactor_grond": "normaal",
    "opslagfactor_grondaankoop": "normaal",
    "max_bermlengte": 50,
    "min_bermhoogte": 0.5,
    "max_bermhoogte_factor": 0.4,
    "factor_toename_bermhoogte": 0.05
}
```

Met de instelling _[actief]_ wordt aangegeven of de grondmaatregel überhaupt wordt meegenomen in de berekening, _true_ of _false_. Op deze manier kan een gebruiker de keuze van een bepaalde maatregel op een dijksectie sturen. De instellingen op deze plek zijn globaal voor alle doorgerekende dijksecties, over het algemeen zal deze instelling daarom op true staan. Maar nogmaals, hier kan per dijksectie via de [dijksectie-specifieke invoerbestanden](h05_dijksectie-invoer.md) vanaf geweken worden.

Met de instellingen _[opslagfactor_grond]_ en _[opslagfactor_grondaankoop]_ wordt de moeilijkheidsfactor aangegeven op basis waarvan de opslagfactoren worden gekozen voor het grondwerk en de aankoop van grond (vastgoedkosten). Zie voor meer informatie de [kostenberekening volgens SSK](h10_sskmethodiek.md).

Met de laatste 3 instellingen wordt de hoogte van de pipingberm gestuurd. _[min_bermhoogte]_ is de minimale pipingbermhoogte in meter, de _[factor_toename_bermhoogte]_ beschrijft hoeveel de pipingbermhoogte toeneemt met iedere meter berm. De _[max_bermhoogte_factor]_ tenslotte is de maximale hoogte van de pipingberm relatief aan de totale dijkhoogte.

## Constructieve maatregelen

In verschillende opeenvolgende blokken worden de specifieke rekeninstellingen opgegeven voor de verschillende constructieve maatregelen. Net als bij de grondmaatregel wordt bij iedere constructieve maatregel aangegeven of deze _[actief]_ (_true_ of _false_) is in de berekening en welke opslagfactoren er moeten worden toegepast op het grondwerk _[opslagfactor_grond]_, op het constructieve element _[opslagfactor_constructief]_ en (indien relevant) de aankoop van grond _[opslagfactor_grondaankoop]_. Daarnaast zijn er instellingen die specifiek voor iedere maatregel. Deze worden in de volgende subparagrafen beschreven.

#### Verticale Piping Oplossing
<a id="verticalepipingoplossing"></a>
Let op: naamgeving van deze constructieve maatregel wordt gewijzigd in 2026.

De verticale piping oplossing is de aanduiding van een (innovatieve) gronddichte maar waterdoorlatende filterconstructie zoals een Verticaal Zanddicht Geotextiel (VZG) of een Grof Zand Barrière (GZB). Deze wordt als volgt geconfigureerd:

```json
"verticalepipingoplossing": {
    "actief": false,
    "opslagfactor_grond": "normaal",
    "opslagfactor_constructief": "normaal",
    "opslagfactor_grondaankoop": "normaal",
    "binnen_berm_breedte_vps": 10
}
```

In KOSWAT wordt deze oplossing altijd geraamd in combinatie met een korte berm aan de binnendijkse zijde. De lengte van deze berm wordt opgegeven met de instelling _[binnen_berm_breedte_vps]_.

#### Kwelscherm
<a id="kwelscherm"></a>
De vervolgens lichtste constructieve maatregel is een kwelscherm in de teen van de dijk. Hiermee kan in het ontwerp voorkomen worden dat een (lange) pipingberm aangelegd dient te worden. Het kwelscherm heeft in KOSWAT geen constructieve sterkte, en draagt daarmee niet bij aan de maatregelen ten aanzien van macrostabiliteit. Voor macrostabiliteit (opgave ds) dient als voorheen bij de grondmaatregel een taludverflauwing binnendijks plaats te vinden, zie [Figuur 1](h02_methode.md#figuur-1).

De lengte van het kwelscherm wordt bepaald door de benodigde extra dijkbasis ten aanzien van piping, waarbij rekening gehouden wordt met het feit dat verticale kwelweglengte effectiever is tegen piping dan horizontale kwelweglengte[^7]. De instellingen in de json zijn als volgt:

```json
"kwelscherm": {
    "actief": true,
    "opslagfactor_grond": "normaal",
    "opslagfactor_constructief": "normaal",
    "opslagfactor_grondaankoop": "normaal",
    "min_lengte_kwelscherm": 4,
    "overgang_cbwand_damwand": 0,
    "max_lengte_kwelscherm": 25
}
```

De minimale en maximale lengte van de toe te passen wand worden gegeven met _[min_lengte_kwelscherm]_ en _[max_lengte_kwelscherm]_.

Kosten voor een kwelscherm kunnen in KOSWAT berekend worden aan de hand van een cement-bentonietscherm voor de kortere schermen of een stalen damwand voor de grotere lengtes. De lengte waarop overgegaan wordt van de een op de andere maatregel in de berekening wordt aangegeven met de instelling _[overgang_cbwand_damwand]_. Voorheen stond deze instelling op 99 m, ofwel er werd altijd gekozen voor een cb-wand, de validatie van KOSWAT aan de hand van HWBP-projecten leert echter dat deze cb-wand in praktijk niet of nauwelijks toegepast wordt, maar dat meestal traditioneel gekozen wordt voor een stalen damwand (heavescherm). De instelling kan daarmee beter per default op 0 gezet worden, zodat de cb-wand hier niet meer gekozen wordt.

Tegenwoordig wordt ook meer en meer geëxperimenteerd met kunststof kwelschermen, deze zijn in KOSWAT nog niet als standaard maatregel opgenomen.

#### Stabiliteitswand
<a id="stabiliteitswand"></a>
Een stabiliteitswand in KOSWAT bestaat uit een enkelvoudige wand tot bovenin in het dijklichaam[^8]. De stabiliteitswand wordt ingebracht tot een meter in de draagkrachtige zandlaag. Instellingen voor deze maatregel zijn als volgt:

```json
"stabiliteitswand": {
    "actief": true,
    "opslagfactor_grond": "moeilijk",
    "opslagfactor_constructief": "normaal",
    "opslagfactor_grondaankoop": "moeilijk",
    "versteiling_binnentalud": 2,
    "min_lengte_stabiliteitswand": 5,
    "overgang_damwand_diepwand": 20,
    "max_lengte_stabiliteitswand": 25
}
```

De minimale en maximale lengte van de toe te passen wand worden gegeven met _[min_lengte_stabiliteitswand]_ en _[max_lengte_stabiliteitswand]_. De constructie kan uitgevoerd worden als een (verankerde) damwand of een diepwand, afhankelijk van de vereiste lengte. De overgang tussen de twee wordt ingesteld door de gebruiker met de rekeninstelling _[overgang_damwand_diepwand]_.

De noodzaak tot een taludverflauwing vervalt met deze oplossing. Het binnentalud mag zelfs versteild worden, waardoor meer ruimte bespaard wordt. Versteiling kan plaatsvinden tot een bepaald maximum (cotan) aangegeven met de instelling _[versteiling_binnentalud]_. Een steiler binnentalud dan 1:2 kan leiden tot extra uitdagingen in het beheer van de dijk (omkiepende grasmaaiers e.d.).

#### Kistdam
<a id="kistdam"></a>
Op plaatsen met bebouwing direct naast of in het bestaande dijklichaam kan een tweezijdige damwand in het dijklichaam worden gekozen, ofwel een kistdam. Hierbij wordt ervan uitgegaan dat de versterking volledig plaats vindt binnen het bestaande ruimtebeslag van de huidige dijk. Dit wordt bereikt door het versteilen van zowel de binnen- als de buitentaludhelling. Aan deze versteiling worden in de berekening geen grenzen gesteld. De inheidiepte van de kistdam is gelijk aan die van de stabiliteitswand.

```json
"kistdam": {
    "actief": true,
    "opslagfactor_grond": "moeilijk",
    "opslagfactor_constructief": "moeilijk",
    "min_lengte_kistdam": 7,
    "max_lengte_kistdam": 25
}
```

De minimale en maximale lengte van de toe te passen wand worden gegeven met _[min_lengte_kistdam]_ en _[max_lengte_kistdam]_.

## Omgeving
<a id="omgeving"></a>
Met de rekeninstelling _[omgevingstypes]_ wordt opgegeven welke lagen een harde grens stellen aan de beschikbare ruimte voor een versterking. Ofwel, als in de versterkingszone dergelijke obstructies geconstateerd worden, zal KOSWAT kiezen voor een alternatieve (constructieve) oplossing op die plek.

```json
"omgeving": {
    "omgevingtypes": ["bebouwing", "water", "spoorwegen"],
    "constructieafstand": 50,
    "constructieovergang": 10
}
```

Zie [Omgevingsdatabases](h08_omgevingsdatabases.md) voor meer informatie over de bestanden en de exacte folderstructuur waarin de bestanden moeten staan.

Met de rekeninstelling _[constructieovergang]_ wordt aangegeven over welke lengte aan weerszijden van een constructieve oplossing een overgangsconstructie moeten worden toegepast. Wanneer wordt gekozen voor een stabiliteitswand ter plaatse van een woning o.i.d., zal deze in praktijk aan weerszijden immers een stukje doorlopen, voordat er weer volledig in grond versterkt wordt. Een andere instelling is de minimale ruimte tussen constructies die wordt vereist, aangegeven met _[constructieafstand]_. In de analyse zullen twee constructieve strekkingen samengevoegd worden tot één doorlopende constructie, wanneer de ruimte tussen de constructies kleiner wordt dan deze opgegeven afstand.

## Infrastructuur
<a id="infrastructuur"></a>
Weginfrastructuur in de versterkingszone stelt geen grens aan de beschikbare ruimte zoals de obstructies beschreven in de vorige paragraaf, maar het leidt wel tot extra kosten om wegen tijdelijk te verwijderen en nadien opnieuw aan te leggen. De aanwezigheid van wegen is vastgelegd in de omgevingsdatabases beschreven in [Omgevingsdatabases](h08_omgevingsdatabases.md). Hierbij worden verschillende breedteklasses gehanteerd die aansluiten bij het Nationaal Wegen Bestand (NWB). De volgende instellingen zijn van kracht:

```json
"infrastructuur": {
    "actief": true,
    "opslagfactor_wegen": "normaal",
    "infrakosten_0dh": "vervang",
    "wegen_klasse2_breedte": 3.5,
    "wegen_klasse24_breedte": 8,
    "wegen_klasse47_breedte": 10,
    "wegen_klasse7_breedte": 12,
    "wegen_onbekend_breedte": 6
}
```

In de verschillende wegendatabases[^9] zijn as-lengtes van de verschillende wegtypes vastgelegd. Met de instellingen _[wegen_klasse2_breedte]_, _[wegen_klasse24_breedte]_, _[wegen_klasse47_breedte]_, _[wegen_klasse7_breedte]_ en _[wegen_onbekend_breedte]_ wordt aangegeven welke wegbreedte hierbij hoort om daarmee het aantal vierkante meters te bepalen ten behoeve van de kostenraming.

De rekeninstelling _[infrakosten_0dh]_ geeft aan op welke manier kosten worden geraamd voor infrastructuur die <u>op</u> de dijkkruin ligt op secties waar de dijk <u>niet</u> wordt opgehoogd (maar de dijk wel versterkt wordt ten aanzien van macrostabiliteit en/of piping). Mogelijke opties zijn hier “vervang” wanneer infrastructuur compleet vervangen wordt, “herstel” wanneer enkel kosten voor herstel van de bestaande infrastructuur wordt gerekend (bijvoorbeeld omdat het tijdens de versterking kapot wordt gereden door zwaar materieel) of “geen” wanneer hiervoor helemaal geen kosten gerekend hoeven te worden.

[^6]: Gebruik hierbij enkel letters _[a tot z]_, cijfers _[0 tot 9]_, koppeltekens _[- of _]_ en voor de zekerheid geen spaties of andere vreemde tekens.
[^7]: Rekenregels voor het bepalen van de wandlengte worden in 2026 bijgesteld.
[^8]: In 2026 wordt ook een damwand in de binnenteen aan het assortiment van KOSWAT toegevoegd. Rekenregels om de wandlengtes te bepalen worden dan ook tegen het licht gehouden.
[^9]: Klasse-indeling in de wegendatabases is gewijzigd, naamgeving van bestanden en rekeninstellingen dient hierop aangepast te worden in 2026.
