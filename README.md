# VetMeds Data

Veřejný export českého registru veterinárních léčiv v JSON. Obsahuje přípravky, jejich balení a změny zachycené porovnáním ověřených exportů. Přehled pro prohlížeč nabízí [dashboard VetMeds](https://hrabosh.github.io/vetmeds/).

| Soubor | Obsah |
| --- | --- |
| [`v1/metadata.json`](v1/metadata.json) | Zdroj, ID snímku, čas pozorování, začátek historie a počty. |
| [`v1/preparations.json`](v1/preparations.json) | Přípravky v aktuálním exportu včetně registračního čísla, držitele a metadat SPC. |
| [`v1/packages.json`](v1/packages.json) | Balení v aktuálním exportu včetně vazby na přípravek, způsobu výdeje a data zneplatnění kódu, pokud je ve zdroji. |
| [`v1/changes.json`](v1/changes.json) | Věcné změny od prvního snímku včetně hodnot před a po změně. Nejnovější události jsou první. |

Všechny čtyři soubory mají `schema_version` a `snapshot_id`. Při stahování více souborů ověř shodné ID nebo použij adresy ze stejného commitu na GitHubu. Pro jednotlivé přípravky používej `preparation_id`. Balení na něj odkazují a mají vlastní `package_code`. Kódy a identifikátory jsou řetězce a mohou začínat nulou. Hodnota `null` znamená, že zdroj údaj neuvádí.

```bash
curl -fsS https://hrabosh.github.io/vetmeds/data/v1/metadata.json | jq .
```

Historie začíná prvním snímkem. `observed_at` označuje čas záchytu, nikoliv datum právní účinnosti změny. Událost `missing_from_export` znamená, že záznam chyběl v následujícím exportu. Platnost registrace ověř v [oficiálním seznamu ÚSKVBL](https://www.uskvbl.cz/cs/databaze-a-seznamy/seznam-vlp).

Workflow **Sync VetMeds dataset** kontroluje veřejný export denně v 08:17 UTC. Věcně shodný export nevytváří commit. Čas poslední úspěšné kontroly zdroje je na dashboardu. Po 60 dnech bez aktivity může GitHub plánované běhy veřejného repozitáře vypnout. V takovém případě je lze zapnout v záložce **Actions**.

Zdrojem jsou [exporty ÚSKVBL](https://www.uskvbl.cz/cs/databaze-a-seznamy/seznam-vlp/data-vlp-ke-stazeni). Licence pro další užití dat v tomto repozitáři zatím uvedená není.
