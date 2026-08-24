#!/usr/bin/env python3
"""Focused tests for validate_loss_tree_fields.py."""

from __future__ import annotations

import tempfile
from pathlib import Path

import h5py
import numpy as np

from validate_loss_tree_fields import TREE_GROUP_FIELDS, validate


def _write_fixture(root: Path) -> tuple[Path, Path]:
    output = root / "output"
    output.mkdir()
    catalogue_path = output / "fof_subhalo_tab_000.hdf5"
    tree_path = output / "trees.hdf5"

    with h5py.File(catalogue_path, "w") as catalogue:
        group = catalogue.create_group("Group")
        group.create_dataset("GroupNsubs", data=np.array([2, 1], dtype=np.int32))
        for number, field in enumerate(TREE_GROUP_FIELDS, start=1):
            group.create_dataset(field, data=np.array([number, number + 1], dtype=np.float32))

    with h5py.File(tree_path, "w") as trees:
        trees.create_group("Parameters")
        config = trees.create_group("Config")
        config.attrs["FOF_LINKLENGTH"] = 0.28
        header = trees.create_group("Header")
        header.attrs["Git_commit"] = "fixture-commit"
        header.attrs["Git_date"] = "fixture-date"
        header.attrs["Nhalos_ThisFile"] = 3
        header.attrs["Nhalos_Total"] = 3
        header.attrs["Ntrees_ThisFile"] = 2
        header.attrs["Ntrees_Total"] = 2
        halos = trees.create_group("TreeHalos")
        halos.create_dataset("TreeFirstHaloInFOFgroup", data=np.array([0, 0, 2]))
        halos.create_dataset("TreeIndex", data=np.array([0, 1, 2]))
        halos.create_dataset("SnapNum", data=np.zeros(3, dtype=np.int32))
        halos.create_dataset("GroupNr", data=np.array([0, 0, 1], dtype=np.int64))
        for number, field in enumerate(TREE_GROUP_FIELDS, start=1):
            halos.create_dataset(
                field, data=np.array([number, 0, number + 1], dtype=np.float32)
            )

    return tree_path, output


def test_valid_fixture() -> None:
    with tempfile.TemporaryDirectory() as directory:
        tree_path, catalogue_dir = _write_fixture(Path(directory))
        summary = validate(
            tree_path,
            catalogue_dir=catalogue_dir,
            expected_commit="fixture-commit",
            expected_fof_link_length=0.28,
        )
        assert summary["satellite_rows_checked"] == 1
        assert summary["central_rows"] == 2
        assert summary["tree_halos"] == 3
        assert summary["trees"] == 2
        assert len(summary["catalogue_fields_exactly_matched"]) == len(TREE_GROUP_FIELDS)


def test_nonzero_satellite_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        tree_path, _ = _write_fixture(Path(directory))
        with h5py.File(tree_path, "r+") as trees:
            trees["TreeHalos/GroupMass"][1] = 1
        try:
            validate(tree_path)
        except AssertionError as error:
            assert "nonzero satellite rows" in str(error)
        else:
            raise AssertionError("nonzero satellite value was accepted")


if __name__ == "__main__":
    test_valid_fixture()
    test_nonzero_satellite_rejected()
    print("validate_loss_tree_fields tests: OK")
