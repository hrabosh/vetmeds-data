# Schéma a původ dat

## Zdroje

- [Data VLP ke stažení](https://www.uskvbl.cz/cs/databaze-a-seznamy/seznam-vlp/data-vlp-ke-stazeni) jsou zdrojem přípravků, balení a klasifikace. VetMeds ukládá rozdíly mezi ověřenými snímky registru od prvního pozorování uvedeného v `metadata.json`.
- [Věstník 2/2026, str. 54](https://www.uskvbl.cz/attachments/article/35/v%C4%9Bstn%C3%ADk_2.Q_2026.pdf#page=54) je zdrojem prvního oddílu o zrušených registracích. Historické události mohou odkazovat na přípravky, které už v aktuálním snímku chybějí.

Podmínky dalšího užití dat ověř u ÚSKVBL. Repozitář zatím neuvádí samostatnou licenci k datům.

## Verze 1

| Soubor | Klíče | Čas a vazby |
| --- | --- | --- |
| `metadata.json` | `snapshot_id`, `observed_at`, `history_started_at`, `counts`, `source_url` | Čas posledního věcně odlišného snímku a začátek sběru v UTC |
| `preparations.json` | `preparations[]`, `preparation_id`, `registration_number` | ID přípravku je klíč. Registrační číslo se může opakovat. |
| `packages.json` | `packages[]`, `package_code`, `preparation_id` | Interní kód označuje balení. Vazbu určuje ID přípravku. |
| `classification.json` | `preparations[]`, `terms.species`, `terms.substances`, `terms.atc` | `preparations[].id` odkazuje na ID přípravku. Hodnoty v `classification` odkazují na `id` v příslušném číselníku. Počet v číselníku počítá unikátní přípravky. |
| `changes.json` | `events[]`, `entity_id`, `observed_at` | Čas, kdy VetMeds změnu zachytil. U přesunu balení zůstávají ID přípravků před i po změně. |
| `registration-events.json` | `source.issue`, `source.url`, `source.sha256`, `events[]` | Historie z vydání Věstníku. Událost uvádí typ, název, registrační číslo, `occurred_in` jako měsíc ve formátu `YYYY-MM` a `source_page`. |

Každý soubor uvádí `schema_version`. Soubory snímku spojuje `snapshot_id`. Události z Věstníku mají vlastní zdroj a SHA-256 PDF. Při práci s více soubory použij odkazy z jednoho commitu. Identifikátory jsou řetězce a mohou začínat nulou. `null` znamená, že zdroj údaj neuvádí. Klasifikace se může měnit i mezi kontrolami stejného snímku.

Typ `missing_from_export` vyjadřuje rozdíl mezi dvěma snímky registru. Zrušení registrace dokládá samostatná událost `registration_cancelled` s odkazem na Věstník.

## Historie přípravku

Ve složce `v1/by-preparation` je po jednom souboru na přípravek. Soubor obsahuje `preparation`, `packages` a dostupnou `classification`. Cesta vychází z `preparation_id` a zůstává stejná i po přejmenování přípravku.

```bash
git clone https://github.com/hrabosh/vetmeds-data.git
cd vetmeds-data
id=0910f7c78008d143
soubor="$(python3 tools/preparations.py path "$id")"
git show "HEAD:$soubor"
git log -p -- "$soubor"
jq --arg id "$id" '.events[] | select(.preparation_id_before == $id or .preparation_id_after == $id)' v1/changes.json
```

Starší stav zobrazíš příkazem `git show <commit>:<soubor>`. Pokud přípravek zmizí z exportu, jeho soubor se odebere z aktuálního snímku a starší revize zůstanou v Gitu.

## Ověření a sestavení

Synchronizace ověřuje společná ID snímku, počty, vazby balení a formát událostí z Věstníku. Datové commity uvádějí `Snapshot-ID` a `Observed-At` pro registr. Čas poslední kontroly zdroje zobrazuje [dashboard](https://hrabosh.github.io/vetmeds/).

Každý soubor přípravku lze znovu sestavit ze souhrnných JSON stejného commitu.

```bash
pracovni="$(mktemp -d)"
python3 tools/preparations.py build v1 "$pracovni/by-preparation"
diff -r v1/by-preparation "$pracovni/by-preparation"
```

Po 60 dnech bez aktivity může GitHub plánovanou synchronizaci vypnout. Znovu ji zapneš v záložce [Actions](https://github.com/hrabosh/vetmeds-data/actions/workflows/sync.yml).
