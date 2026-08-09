"""Verify that built distribution versions match a release tag."""

import argparse
import email
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Callable, Iterable, List, Tuple


PROJECT_NAME = "sandborg-petersen-decoder"
EXPECTED_LICENSE = "MIT"


def metadata_version(contents: bytes) -> str:
    message = email.message_from_bytes(contents)
    name = message.get("Name")
    version = message.get("Version")
    license_expression = message.get("License-Expression")
    if name != PROJECT_NAME or not version:
        raise ValueError(
            f"Unexpected package metadata: Name={name!r}, Version={version!r}"
        )
    if license_expression != EXPECTED_LICENSE:
        raise ValueError(
            "Unexpected package license metadata: "
            f"License-Expression={license_expression!r}, expected {EXPECTED_LICENSE!r}"
        )
    return version


def wheel_version(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        metadata_files = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_files) != 1:
            raise ValueError(f"Expected one METADATA file in {path.name}")
        return metadata_version(archive.read(metadata_files[0]))


def sdist_version(path: Path) -> str:
    with tarfile.open(path, "r:gz") as archive:
        metadata_files = [
            member
            for member in archive.getmembers()
            if member.name.endswith("/PKG-INFO") and member.isfile()
        ]
        if len(metadata_files) != 1:
            raise ValueError(f"Expected one PKG-INFO file in {path.name}")
        extracted = archive.extractfile(metadata_files[0])
        if extracted is None:
            raise ValueError(f"Could not read PKG-INFO from {path.name}")
        return metadata_version(extracted.read())


def validate(tag: str, directory: Path) -> List[str]:
    expected = tag.removeprefix("v")
    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    errors: List[str] = []

    if len(wheels) != 1:
        errors.append(f"Expected one wheel in {directory}, found {len(wheels)}")
    if len(sdists) != 1:
        errors.append(f"Expected one source distribution in {directory}, found {len(sdists)}")

    readers: Iterable[Tuple[Path, Callable[[Path], str]]] = [
        *((path, wheel_version) for path in wheels),
        *((path, sdist_version) for path in sdists),
    ]
    for path, reader in readers:
        try:
            actual = reader(path)
        except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as error:
            errors.append(str(error))
            continue
        if actual != expected:
            errors.append(
                f"{path.name} contains version {actual!r}, expected {expected!r} from {tag!r}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    args = parser.parse_args()

    errors = validate(args.tag, args.directory)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Distribution metadata matches {args.tag}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
