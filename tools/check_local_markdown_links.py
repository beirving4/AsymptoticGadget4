#!/usr/bin/env python3
"""Check that repository-local Markdown link targets exist."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("#", "http://", "https://", "mailto:")


def markdown_files() -> list[Path]:
    roots = [
        ROOT / "README.md",
        ROOT / "MODIFICATIONS.md",
        ROOT / "AUTHORS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CONTRIBUTING.md",
    ]
    roots.extend(
        ROOT / "documentation" / name
        for name in (
            "01_index.md",
            "12_asymptotic_extensions.md",
            "13_loss_data_release.md",
            "14_graphify_audit.md",
            "15_build_portability.md",
            "16_release_checklist.md",
            "17_cluster_validation_handoff.md",
        )
    )
    roots.extend(sorted((ROOT / "examples").glob("LOSS*/README.md")))
    return [path for path in roots if path.is_file()]


def missing_links(path: Path) -> list[str]:
    missing: list[str] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        for match in LINK.finditer(line):
            raw_target = match.group(1).strip().strip("<>")
            target_text = raw_target.split(maxsplit=1)[0]
            if not target_text or target_text.startswith(SKIP_PREFIXES):
                continue
            target_text = unquote(target_text.split("#", maxsplit=1)[0])
            target = (path.parent / target_text).resolve()
            if not target.exists():
                relative_source = path.relative_to(ROOT)
                missing.append(f"{relative_source}:{line_number}: {raw_target}")
    return missing


def main() -> None:
    missing = [item for path in markdown_files() for item in missing_links(path)]
    if missing:
        for item in missing:
            print(f"ERROR: missing local Markdown target: {item}")
        raise SystemExit(1)
    print(f"checked local links in {len(markdown_files())} Markdown files")


if __name__ == "__main__":
    main()
