#!/usr/bin/env python3
"""Create a deterministic size and SHA-256 manifest for a staged data release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, output: Path) -> dict[str, object]:
    root = root.resolve()
    output = output.resolve()
    files: list[dict[str, object]] = []

    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        if path.resolve() == output:
            continue
        size = path.stat().st_size
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": size,
                "sha256": sha256(path),
            }
        )

    return {
        "schema": "asymptotic-gadget-release-manifest-v1",
        "root": root.name,
        "file_count": len(files),
        "total_bytes": sum(int(item["bytes"]) for item in files),
        "files": files,
    }


def verify_manifest(root: Path, manifest_path: Path) -> list[str]:
    """Return human-readable differences between a manifest and its files."""

    expected: dict[str, Any] = json.loads(manifest_path.read_text())
    actual = build_manifest(root, manifest_path)
    errors: list[str] = []

    for key in ("schema", "root", "file_count", "total_bytes"):
        if expected.get(key) != actual.get(key):
            errors.append(
                f"{key}: expected {expected.get(key)!r}, found {actual.get(key)!r}"
            )

    def by_path(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
        entries = manifest.get("files", [])
        if not isinstance(entries, list):
            raise ValueError("manifest 'files' value must be a list")
        return {str(entry["path"]): entry for entry in entries}

    expected_files = by_path(expected)
    actual_files = by_path(actual)

    for path in sorted(expected_files.keys() - actual_files.keys()):
        errors.append(f"missing file: {path}")
    for path in sorted(actual_files.keys() - expected_files.keys()):
        errors.append(f"unexpected file: {path}")
    for path in sorted(expected_files.keys() & actual_files.keys()):
        for key in ("bytes", "sha256"):
            if expected_files[path].get(key) != actual_files[path].get(key):
                errors.append(
                    f"{path} {key}: expected {expected_files[path].get(key)!r}, "
                    f"found {actual_files[path].get(key)!r}"
                )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="staged release directory")
    parser.add_argument("--output", type=Path, default=Path("MANIFEST.json"))
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify root against an existing --output manifest",
    )
    args = parser.parse_args()

    if args.verify:
        errors = verify_manifest(args.root, args.output)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            raise SystemExit(1)
        print(f"verified {args.output}: all files match")
        return

    manifest = build_manifest(args.root, args.output)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}: {manifest['file_count']} files, {manifest['total_bytes']} bytes")


if __name__ == "__main__":
    main()
