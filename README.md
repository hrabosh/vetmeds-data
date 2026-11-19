# VetMeds Data

Český registr veterinárních léčiv v JSON. Obsahuje aktuální přípravky a balení, klasifikaci podle látek, cílových druhů a ATCvet, změny zachycené při kontrolách exportu a ověřené události z Věstníku ÚSKVBL.

Czech veterinary medicines registry data and a source-linked history of regulatory events.

[Dashboard](https://hrabosh.github.io/vetmeds/) · [Katalog](https://hrabosh.github.io/vetmeds/registr.html) · [Historický katalog](https://hrabosh.github.io/vetmeds/registr.html?historie) · [Schéma a původ dat](DATA.md)

## Stažení

| Soubor | Obsah | Přímý odkaz |
| --- | --- | --- |
| [metadata.json](v1/metadata.json) | ID snímku, zdroj, čas pozorování a počty | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/metadata.json) |
| [preparations.json](v1/preparations.json) | Aktuální přípravky a registrační údaje | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/preparations.json) |
| [packages.json](v1/packages.json) | Balení, způsob výdeje a vazba na přípravek | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/packages.json) |
| [classification.json](v1/classification.json) | Léčivé látky, cílové druhy a ATCvet | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/classification.json) |
| [changes.json](v1/changes.json) | Změny mezi snímky registru | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/changes.json) |
| [registration-events.json](v1/registration-events.json) | Zrušení registrací z Věstníku 2/2026 | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/registration-events.json) |

Každý přípravek má také [samostatný soubor s baleními a klasifikací](v1/by-preparation/a5/0910f7c78008d143.json). Přehled jeho verzí zobrazuje Git. [Příklady příkazů](DATA.md#historie-přípravku)

Repozitář přebírá ověřená data z VetMeds denně v 08:17 UTC. Za změnu exportu zapíše jeden commit. [Běhy synchronizace](https://github.com/hrabosh/vetmeds-data/actions/workflows/sync.yml)
