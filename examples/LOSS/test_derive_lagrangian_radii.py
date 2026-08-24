#!/usr/bin/env python3

import importlib.util
import math
import tempfile
import unittest
from pathlib import Path

import h5py
import numpy as np


MODULE_PATH = Path(__file__).with_name("derive_lagrangian_radii.py")
SPEC = importlib.util.spec_from_file_location("derive_lagrangian_radii", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LagrangianRadiusTest(unittest.TestCase):
    def test_catalogue_parameters_are_sufficient(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalogue.hdf5"
            with h5py.File(path, "w") as catalogue:
                parameters = catalogue.create_group("Parameters")
                parameters.attrs["Omega0"] = 0.3
                parameters.attrs["Hubble"] = 100.0
                parameters.attrs["GravityConstantInternal"] = 1.0
                groups = catalogue.create_group("Group")
                groups["GroupMass"] = np.array([0.0, 4.0, 32.0])

            density, radii = MODULE.derive_catalogue(path)
            expected_density = 3.0 * 0.3 * 100.0**2 / (8.0 * math.pi)
            np.testing.assert_allclose(density, expected_density)
            np.testing.assert_allclose(
                radii["R_Lag_GroupMass"],
                MODULE.lagrangian_radius(np.array([0.0, 4.0, 32.0]), expected_density),
            )

    def test_missing_cosmology_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalogue.hdf5"
            with h5py.File(path, "w") as catalogue:
                catalogue.create_group("Parameters")
                catalogue.create_group("Group")

            with self.assertRaisesRegex(KeyError, "Omega0"):
                MODULE.derive_catalogue(path)


if __name__ == "__main__":
    unittest.main()
