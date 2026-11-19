"""Create one stable JSON file per veterinary medicine preparation."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

RECORDS = Path("v1/by-preparation")


def identifier(row, field):
    value = row[field]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def record_path(preparation_id):
    bucket = hashlib.sha256(preparation_id.encode("utf-8")).hexdigest()[:2]
    filename = quote(preparation_id, safe="") + ".json"
    return RECORDS / bucket / filename


def load_rows(source, filename, key):
    document = json.loads((source / filename).read_text(encoding="utf-8"))
    return document[key]



def add_classification(source, records):
    path = source / "classification.json"
    if not path.is_file():
        return

    document = json.loads(path.read_text(encoding="utf-8"))
    terms = {
        group: {term["id"]: term["name"] for term in document["terms"][group]}
        for group in ("species", "substances", "atc")
    }
    for item in document["preparations"]:
        preparation_id = identifier(item, "id")
        record = records[preparation_id]
        if "classification" in record:
            raise ValueError(f"Duplicate classification for preparation {preparation_id!r}")
        record["classification"] = {
            group: [
                {"id": term, "name": labels[term]}
                for term in item["classification"][group]
            ]
            for group, labels in terms.items()
        }


def project(source, output):
    records = {}
    for preparation in load_rows(source, "preparations.json", "preparations"):
        preparation_id = identifier(preparation, "preparation_id")
        if preparation_id in records:
            raise ValueError(f"Duplicate preparation {preparation_id!r}")
        records[preparation_id] = {
            "schema_version": 1,
            "preparation": preparation,
            "packages": [],
        }

    package_codes = set()
    for package in load_rows(source, "packages.json", "packages"):
        code = identifier(package, "package_code")
        preparation_id = identifier(package, "preparation_id")
        if preparation_id not in records:
            raise ValueError(f"Package {code!r} references missing preparation {preparation_id!r}")
        if code in package_codes:
            raise ValueError(f"Duplicate package {code!r}")
        package_codes.add(code)
        records[preparation_id]["packages"].append(package)

    add_classification(source, records)
    output.mkdir()
    for preparation_id, record in records.items():
        record["packages"].sort(key=lambda package: package["package_code"])
        destination = output / record_path(preparation_id).relative_to(RECORDS)
        destination.parent.mkdir(exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
    print(f"Built {len(records)} preparation files from {len(package_codes)} packages.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    lookup = commands.add_parser("path", help="Print the Git path for a preparation ID")
    lookup.add_argument("preparation_id")
    build = commands.add_parser("build", help="Generate the files from a validated v1 export")
    build.add_argument("source", type=Path)
    build.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.command == "path":
        print(record_path(args.preparation_id).as_posix())
        return
    try:
        project(args.source, args.output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
