import argparse
import re
from datetime import date
from pathlib import Path


TAG_PATTERN = re.compile(r"^v\d+\.\d+(?:\.\d+)?$")
REQUIRED_FIELDS = ("version", "date-released")


def read_citation_metadata(path):
    values = {}
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        if raw_line.startswith(" ") or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        if key in REQUIRED_FIELDS:
            values[key] = value.strip().strip('"').strip("'")

    return values


def validation_errors(metadata, tag=None, today=None):
    errors = []
    missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
    if missing:
        return [f"Missing CITATION.cff field(s): {', '.join(missing)}"]

    version = metadata["version"]
    release_date_text = metadata["date-released"]

    if not TAG_PATTERN.fullmatch(version):
        errors.append(
            "CITATION.cff version must use vMAJOR.MINOR or vMAJOR.MINOR.PATCH"
        )
    if tag and version != tag:
        errors.append(
            f"CITATION.cff version {version!r} does not match release tag {tag!r}"
        )

    try:
        release_date = date.fromisoformat(release_date_text)
    except ValueError:
        errors.append("CITATION.cff date-released must use YYYY-MM-DD")
    else:
        if release_date > (today or date.today()):
            errors.append("CITATION.cff date-released cannot be in the future")

    return errors


def validate_release(path, tag=None, today=None):
    metadata = read_citation_metadata(path)
    return validation_errors(metadata, tag=tag, today=today)


def main():
    parser = argparse.ArgumentParser(
        description="Validate CITATION.cff before publishing a tagged release."
    )
    parser.add_argument("--tag", help="Release tag expected in CITATION.cff")
    parser.add_argument(
        "--citation", default="CITATION.cff", help="Path to the citation file"
    )
    args = parser.parse_args()

    errors = validate_release(args.citation, tag=args.tag)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    metadata = read_citation_metadata(args.citation)
    print(
        "Release metadata is valid: "
        f"{metadata['version']} ({metadata['date-released']})"
    )


if __name__ == "__main__":
    main()
