#!/usr/bin/env python3
"""Validate the AsymptoticGadget HDF5 smoke-test outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import h5py
import numpy as np


TURNAROUND_FIELDS = (
    "Group_M_Turnaround",
    "Group_R_Turnaround",
    "Group_M_TurnLambda",
    "Group_R_TurnLambda",
)

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
    *TURNAROUND_FIELDS,
)


def _dataset_names(handle: h5py.File) -> list[str]:
    names: list[str] = []
    handle.visititems(
        lambda name, obj: names.append(name) if isinstance(obj, h5py.Dataset) else None
    )
    return names


def validate(output_dir: Path, snapshot_number: int) -> dict[str, int]:
    suffix = f"{snapshot_number:03d}"
    catalogue_path = output_dir / f"fof_subhalo_tab_{suffix}.hdf5"
    snapshot_path = output_dir / f"snapshot_{suffix}.hdf5"
    trees_path = output_dir / "trees.hdf5"

    with h5py.File(catalogue_path, "r") as catalogue:
        for top_level in ("Config", "Header", "Parameters", "Group"):
            if top_level not in catalogue:
                raise AssertionError(f"{catalogue_path} is missing /{top_level}")
        for field in TURNAROUND_FIELDS:
            if field not in catalogue["Group"]:
                raise AssertionError(f"catalogue is missing /Group/{field}")
        catalogue_names = _dataset_names(catalogue)
        group_count = int(catalogue["Group"]["GroupMass"].shape[0])

    with h5py.File(snapshot_path, "r") as snapshot:
        if "Acceleration" not in snapshot["PartType1"]:
            raise AssertionError("snapshot is missing /PartType1/Acceleration")
        snapshot_names = _dataset_names(snapshot)

    with h5py.File(trees_path, "r") as trees:
        for top_level in ("Config", "Header", "Parameters", "TreeHalos"):
            if top_level not in trees:
                raise AssertionError(f"{trees_path} is missing /{top_level}")
        halos = trees["TreeHalos"]
        for attribute in ("Git_commit", "Git_date"):
            if attribute not in trees["Header"].attrs:
                raise AssertionError(f"tree header is missing {attribute}")
        for field in TREE_GROUP_FIELDS:
            if field not in halos:
                raise AssertionError(f"tree is missing /TreeHalos/{field}")

        first_in_group = halos["TreeFirstHaloInFOFgroup"][...]
        tree_index = halos["TreeIndex"][...]
        satellite = first_in_group != tree_index
        for field in TREE_GROUP_FIELDS:
            if np.any(halos[field][...][satellite] != 0):
                raise AssertionError(f"satellite rows contain nonzero {field}")
        tree_names = _dataset_names(trees)
        tree_halo_count = int(first_in_group.size)

    treelink_path = output_dir / f"subhalo_treelink_{suffix}.hdf5"
    with h5py.File(treelink_path, "r") as treelinks:
        for attribute in ("Git_commit", "Git_date"):
            if attribute not in treelinks["Header"].attrs:
                raise AssertionError(f"tree-link header is missing {attribute}")

    all_names = catalogue_names + snapshot_names + tree_names
    forbidden = [name for name in all_names if "R_Lag" in name]
    if forbidden:
        raise AssertionError(f"stored Lagrangian-radius datasets found: {forbidden}")

    return {
        "groups": group_count,
        "tree_halos": tree_halo_count,
        "satellite_rows_checked": int(np.count_nonzero(satellite)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--snapshot", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(validate(args.output_dir, args.snapshot), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
