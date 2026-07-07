# Software, installatie en gebruik

De KOSWAT-software is geschreven in Python en beschikbaar via de Github omgeving van Deltares op [https://github.com/Deltares/Koswat](https://github.com/Deltares/Koswat). Voor de installatie van KOSWAT kan bijvoorbeeld de Python Package Index PyPi gebruikt worden. In onderstaande stappen wordt een zekere basiskennis van het werken met Python verondersteld. Andere manieren van installatie, bijvoorbeeld via een Docker container worden gegeven in de online documentatie via het menu aan de linkerzijde.

Start met het creëren van een Python omgeving waarin pip geïnstalleerd is.

```console
conda create -n koswat_env python==3.13 pip
```

Installeer nadat je deze omgeving hebt geactiveerd vervolgens KOSWAT. Gebruik hierbij een versie die gereleased en stabiel is, zie hiervoor het [overzicht met releases op Github](https://github.com/Deltares/Koswat/releases). Voor KOSWAT versie 2025.Q4 geldt:

```console
pip install git+https://github.com/Deltares/Koswat.git@v0.16.0
```

Check of de installatie geslaagd is met:

```console
pip show koswat
```

<a id="berekening"></a>
Wanneer de installatie geslaagd is kan een KOSWAT-project doorgerekend worden. Dit project wordt gedefinieerd in een *.json bestand (zie het onderdeel [Definitie van een KOSWAT project](h04_projectdefinitie.md)) en kan gedraaid worden via de command line met het volgende commando:

```console
python -m koswat --input_file path\to\your\koswat.json --log_output path\to\your\output\dir
```
