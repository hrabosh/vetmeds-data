# VetMeds Data · Český registr veterinárních léčiv

Aktuální přípravky, balení a historie změn českého registru veterinárních léčiv ÚSKVBL ve formátu JSON. Každý přípravek má vlastní soubor se svými baleními a Git uchovává jeho dřívější verze.

Czech veterinary medicines registry dataset. It contains current products, package records and observed changes.

[Dashboard VetMeds](https://hrabosh.github.io/vetmeds/) · [Katalog přípravků a balení](https://hrabosh.github.io/vetmeds/registr.html)

## Datové soubory

| Soubor | Obsah | Stažení |
| --- | --- | --- |
| [`v1/metadata.json`](v1/metadata.json) | Zdroj, ID snímku, čas pozorování, začátek historie a počty. | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/metadata.json) |
| [`v1/preparations.json`](v1/preparations.json) | Aktuální přípravky včetně registračního čísla, držitele a metadat SPC. | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/preparations.json) |
| [`v1/packages.json`](v1/packages.json) | Balení, vazba na přípravek, způsob výdeje a případné datum zneplatnění kódu. | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/packages.json) |
| [`v1/changes.json`](v1/changes.json) | Změny od prvního snímku včetně hodnot před a po změně. Nejnovější události jsou první. | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/changes.json) |
| [`v1/classification.json`](v1/classification.json) | Léčivé látky, cílové druhy zvířat, kódy ATCvet a vazby na přípravky. | [JSON](https://raw.githubusercontent.com/hrabosh/vetmeds-data/main/v1/classification.json) |

Všechny souhrnné soubory mají `schema_version` a `snapshot_id`. Při stahování více souborů ověř shodné ID nebo použij adresy ze stejného commitu na GitHubu. Pro jednotlivé přípravky používej `preparation_id`. Balení na něj odkazují a mají vlastní `package_code`. Kódy a identifikátory jsou řetězce a mohou začínat nulou. Hodnota `null` znamená, že zdroj údaj neuvádí.

```bash
curl -fsS https://hrabosh.github.io/vetmeds/data/v1/metadata.json | jq .
```

## Historie přípravku v Gitu

[Aagent](v1/by-preparation/a5/0910f7c78008d143.json) ukazuje strukturu jednoho záznamu. Objekt `preparation` obsahuje údaje o přípravku, pole `packages` jeho balení v daném snímku. Objekt `classification` uvádí léčivé látky, cílové druhy a kódy ATCvet s popisky. Cestu určuje `preparation_id` a je stejná i po přejmenování přípravku.

Po úplném klonování repozitáře můžeš zobrazit aktuální stav i změny přípravku. `jq` slouží k filtrování souhrnných souborů.

```bash
git clone https://github.com/hrabosh/vetmeds-data.git
cd vetmeds-data
id=0910f7c78008d143
soubor="$(python3 tools/preparations.py path "$id")"

# Aktuální záznam a jeho historie v Gitu
git show "HEAD:$soubor"
git log -p -- "$soubor"

# Události přípravku i jeho balení od začátku sběru
jq --arg id "$id" '.events[] | select(.preparation_id_before == $id or .preparation_id_after == $id)' v1/changes.json
```

Pro dřívější stav vyber commit z výpisu a použij `git show <commit>:<soubor>`. Když přípravek zmizí z exportu, jeho soubor se odebere z aktuálního snímku a starší revize zůstanou v Gitu. Historie jednotlivých souborů začíná jejich prvním zveřejněním. Dřívější zachycené události najdeš v `v1/changes.json`.

## Čas a původ dat

Historie začíná prvním snímkem. `observed_at` označuje čas záchytu, nikoliv datum právní účinnosti změny. Událost `missing_from_export` znamená, že záznam chyběl v následujícím exportu. Platnost registrace ověř v [oficiálním seznamu ÚSKVBL](https://www.uskvbl.cz/cs/databaze-a-seznamy/seznam-vlp).

Workflow **Sync VetMeds dataset** kontroluje veřejný export denně v 08:17 UTC. Kontroluje shodné ID snímku, počty záznamů a vazby balení k přípravkům. Nový datový commit nese `Snapshot-ID` a `Observed-At` v závěru zprávy. Historii snímků registru vypíše `git log -- v1/metadata.json` a vývoj číselníků `git log -- v1/classification.json`. ID snímku a `Observed-At` se vztahují k údajům registru. Klasifikace se může změnit mezi dvěma kontrolami téhož snímku. Věcně shodný export nevytváří commit. Čas poslední úspěšné kontroly zdroje je na dashboardu. Po 60 dnech bez aktivity může GitHub plánované běhy veřejného repozitáře vypnout. V takovém případě je lze zapnout v záložce **Actions**.

Zdrojem jsou [exporty ÚSKVBL](https://www.uskvbl.cz/cs/databaze-a-seznamy/seznam-vlp/data-vlp-ke-stazeni). Licence pro další užití dat v tomto repozitáři zatím uvedená není.

## Místní sestavení souborů

Příkaz znovu sestaví soubory přípravků ze souhrnných JSON stejného commitu. Výstup můžeš porovnat s obsahem repozitáře.

```bash
pracovni="$(mktemp -d)"
python3 tools/preparations.py build v1 "$pracovni/by-preparation"
diff -r v1/by-preparation "$pracovni/by-preparation"
```
