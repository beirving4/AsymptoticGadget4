#!/usr/bin/env python3
"""Validate LOSS group fields and provenance in GADGET-4 merger trees."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np


TREE_GROUP_FIELDS = (
    "GroupMass",
    "Group_M_Crit200",
    "Group_R_Crit200",
    "Group_M_Mean200",
    "Group_R_Mean200",
    "Group_M_Crit500",
    "Group_R_Crit500",
    "Group_M_TopHat200",
    "Group_R_TopHat200",
    "Group_M_Turnaround",
    "Group_R_Turnaround",
    "Group_M_TurnLambda",
    "Group_R_TurnLambda",
)

STANDARD_TRANSFER_FIELDS = TREE_GROUP_FIELDS[:9]


def _decode(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


def _piece_number(path: Path) -> int:
    try:
        return int(path.name.rsplit(".", 2)[-2])
    except (IndexError, ValueError):
        return 0


def resolve_tree_files(path: Path) -> list[Path]:
    """Resolve a tree file, an output directory, or a tree-file basename."""
    if path.is_file():
        return [path]

    candidates: list[Path] = []
    if path.is_dir():
        for directory in (path, path / "treedata"):
            single = directory / "trees.hdf5"
            if single.is_file():
                candidates.append(single)
            candidates.extend(directory.glob("trees.*.hdf5"))
    else:
        single = Path(f"{path}.hdf5")
        if single.is_file():
            candidates.append(single)
        candidates.extend(path.parent.glob(f"{path.name}.*.hdf5"))

    resolved = sorted(set(candidates), key=_piece_number)
    if not resolved:
        raise FileNotFoundError(f"no merger-tree HDF5 files found for {path}")
    return resolved


def resolve_catalogue_files(directory: Path, snapshot: int) -> list[Path]:
    """Resolve single- or multi-file FOF/SUBFIND catalogues for a snapshot."""
    suffix = f"{snapshot:03d}"
    single = directory / f"fof_subhalo_tab_{suffix}.hdf5"
    if single.is_file():
        return [single]

    group_dir = directory / f"groups_{suffix}"
    pieces = sorted(group_dir.glob(f"fof_subhalo_tab_{suffix}.*.hdf5"), key=_piece_number)
    if not pieces:
        raise FileNotFoundError(
            f"no FOF/SUBFIND catalogue found for snapshot {suffix} under {directory}"
        )
    return pieces


def _read_catalogue(directory: Path, snapshot: int) -> dict[str, np.ndarray]:
    pieces = resolve_catalogue_files(directory, snapshot)
    values: dict[str, list[np.ndarray]] = {
        "GroupNsubs": [],
        **{field: [] for field in TREE_GROUP_FIELDS},
    }
    optional_presence: dict[str, bool] = {}

    for path in pieces:
        with h5py.File(path, "r") as catalogue:
            group = catalogue["Group"]
            for field in ("GroupNsubs", *STANDARD_TRANSFER_FIELDS):
                if field not in group:
                    raise AssertionError(f"{path} is missing /Group/{field}")
                values[field].append(group[field][...])

            for field in TREE_GROUP_FIELDS[len(STANDARD_TRANSFER_FIELDS) :]:
                present = field in group
                if field in optional_presence and optional_presence[field] != present:
                    raise AssertionError(
                        f"catalogue pieces disagree about the presence of /Group/{field}"
                    )
                optional_presence[field] = present
                if present:
                    values[field].append(group[field][...])

    result: dict[str, np.ndarray] = {}
    for field, arrays in values.items():
        if arrays:
            result[field] = np.concatenate(arrays)
    return result


def validate(
    tree_path: Path,
    *,
    catalogue_dir: Path | None = None,
    expected_commit: str | None = None,
    expected_fof_link_length: float | None = None,
) -> dict[str, Any]:
    tree_files = resolve_tree_files(tree_path)
    catalogue_cache: dict[int, dict[str, np.ndarray]] = {}
    central_groups: dict[int, list[np.ndarray]] = {}
    compared_fields: set[str] = set()
    commits: set[str] = set()
    dates: set[str] = set()
    link_lengths: set[float] = set()
    total_halos = 0
    total_trees = 0
    central_count = 0
    satellite_count = 0
    declared_total_halos: set[int] = set()
    declared_total_trees: set[int] = set()

    for path in tree_files:
        with h5py.File(path, "r") as trees:
            for group_name in ("Config", "Header", "Parameters", "TreeHalos"):
                if group_name not in trees:
                    raise AssertionError(f"{path} is missing /{group_name}")

            header = trees["Header"].attrs
            for attribute in ("Git_commit", "Git_date"):
                if attribute not in header:
                    raise AssertionError(f"{path} is missing /Header/{attribute}")
            commits.add(_decode(header["Git_commit"]))
            dates.add(_decode(header["Git_date"]))

            link_length = float(trees["Config"].attrs["FOF_LINKLENGTH"])
            link_lengths.add(link_length)

            halos = trees["TreeHalos"]
            for field in TREE_GROUP_FIELDS:
                if field not in halos:
                    raise AssertionError(f"{path} is missing /TreeHalos/{field}")

            forbidden: list[str] = []
            trees.visititems(
                lambda name, obj: forbidden.append(name)
                if isinstance(obj, h5py.Dataset) and "R_Lag" in name
                else None
            )
            if forbidden:
                raise AssertionError(f"stored Lagrangian-radius datasets found: {forbidden}")

            first_in_group = halos["TreeFirstHaloInFOFgroup"][...]
            tree_index = halos["TreeIndex"][...]
            snapshot = halos["SnapNum"][...]
            group_number = halos["GroupNr"][...]
            satellite = first_in_group != tree_index
            central = ~satellite

            for field in TREE_GROUP_FIELDS:
                values = halos[field][...]
                bad = int(np.count_nonzero(values[satellite]))
                if bad:
                    raise AssertionError(f"{path} has {bad} nonzero satellite rows in {field}")

            file_halos = int(first_in_group.size)
            header_halos = int(header["Nhalos_ThisFile"])
            if file_halos != header_halos:
                raise AssertionError(
                    f"{path} contains {file_halos} halo rows but declares {header_halos}"
                )

            total_halos += file_halos
            total_trees += int(header["Ntrees_ThisFile"])
            declared_total_halos.add(int(header["Nhalos_Total"]))
            declared_total_trees.add(int(header["Ntrees_Total"]))
            central_count += int(np.count_nonzero(central))
            satellite_count += int(np.count_nonzero(satellite))

            if catalogue_dir is not None:
                for snap in np.unique(snapshot):
                    snap_number = int(snap)
                    if snap_number not in catalogue_cache:
                        catalogue_cache[snap_number] = _read_catalogue(
                            catalogue_dir, snap_number
                        )
                    catalogue = catalogue_cache[snap_number]
                    rows = np.flatnonzero(central & (snapshot == snap))
                    groups = group_number[rows].astype(np.int64, copy=False)
                    central_groups.setdefault(snap_number, []).append(groups)

                    for field in TREE_GROUP_FIELDS:
                        if field not in catalogue:
                            continue
                        actual = halos[field][...][rows]
                        expected = catalogue[field][groups]
                        if not np.array_equal(actual, expected):
                            raise AssertionError(
                                f"{path}: snapshot {snap_number} differs exactly in {field}"
                            )
                        compared_fields.add(field)

    if len(commits) != 1 or len(dates) != 1:
        raise AssertionError("tree pieces do not have consistent Git provenance")
    if len(link_lengths) != 1:
        raise AssertionError("tree pieces do not have a consistent FOF linking length")
    if declared_total_halos != {total_halos}:
        raise AssertionError(
            f"tree pieces sum to {total_halos} halos but declare {declared_total_halos}"
        )
    if declared_total_trees != {total_trees}:
        raise AssertionError(
            f"tree pieces sum to {total_trees} trees but declare {declared_total_trees}"
        )
    if satellite_count == 0:
        raise AssertionError("tree fixture contains no satellite rows")

    commit = next(iter(commits))
    link_length = next(iter(link_lengths))
    if expected_commit is not None and commit != expected_commit:
        raise AssertionError(f"tree commit is {commit}, expected {expected_commit}")
    if expected_fof_link_length is not None and not np.isclose(
        link_length, expected_fof_link_length, rtol=0.0, atol=1.0e-12
    ):
        raise AssertionError(
            f"tree FOF linking length is {link_length}, expected {expected_fof_link_length}"
        )

    if catalogue_dir is not None:
        for snapshot, group_arrays in central_groups.items():
            actual_groups = np.sort(np.concatenate(group_arrays))
            expected_groups = np.flatnonzero(catalogue_cache[snapshot]["GroupNsubs"] > 0)
            if not np.array_equal(actual_groups, expected_groups):
                raise AssertionError(
                    f"snapshot {snapshot} central rows do not cover every group with subhalos"
                )

    return {
        "catalogue_fields_exactly_matched": sorted(compared_fields),
        "catalogue_snapshots_checked": len(central_groups),
        "central_rows": central_count,
        "fof_link_length": link_length,
        "git_commit": commit,
        "git_date": next(iter(dates)),
        "satellite_rows_checked": satellite_count,
        "tree_files": len(tree_files),
        "tree_halos": total_halos,
        "trees": total_trees,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tree_path", type=Path)
    parser.add_argument(
        "--catalogue-dir",
        type=Path,
        help="optionally require exact group-field transfer from these catalogues",
    )
    parser.add_argument("--expected-commit")
    parser.add_argument("--expected-fof-link-length", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = validate(
        args.tree_path,
        catalogue_dir=args.catalogue_dir,
        expected_commit=args.expected_commit,
        expected_fof_link_length=args.expected_fof_link_length,
    )
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
