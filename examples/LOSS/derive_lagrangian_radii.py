#!/usr/bin/env python3
"""Derive comoving Lagrangian radii from an AsymptoticGadget HDF5 catalogue.

The catalogue already stores the cosmology and unit inputs in /Parameters, so
Lagrangian radii do not need to be persisted as per-halo datasets.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import h5py
import numpy as np


GRAVITY_CGS = 6.67430e-8
MASS_DATASETS = (
    "GroupMass",
    "Group_M_Mean200",
    "Group_M_TopHat200",
    "Group_M_Crit200",
    "Group_M_Crit500",
    "Group_M_Turnaround",
    "Group_M_TurnLambda",
)


def _required_attribute(attributes: h5py.AttributeManager, name: str) -> float:
    if name not in attributes:
        raise KeyError(f"catalogue is missing /Parameters attribute {name!r}")
    return float(attributes[name])


def mean_matter_density(parameters: h5py.AttributeManager) -> float:
    """Return rho_m,0 in the catalogue's internal mass/length^3 units."""

    omega0 = _required_attribute(parameters, "Omega0")
    hubble = _required_attribute(parameters, "Hubble")
    gravity_internal = _required_attribute(parameters, "GravityConstantInternal")

    if gravity_internal == 0.0:
        unit_length = _required_attribute(parameters, "UnitLength_in_cm")
        unit_mass = _required_attribute(parameters, "UnitMass_in_g")
        unit_velocity = _required_attribute(parameters, "UnitVelocity_in_cm_per_s")
        unit_time = unit_length / unit_velocity
        gravity_internal = (
            GRAVITY_CGS
            / unit_length**3
            * unit_mass
            * unit_time**2
        )

    if omega0 <= 0.0 or hubble <= 0.0 or gravity_internal <= 0.0:
        raise ValueError("Omega0, Hubble, and the internal gravitational constant must be positive")

    return 3.0 * omega0 * hubble**2 / (8.0 * math.pi * gravity_internal)


def lagrangian_radius(mass: np.ndarray, density: float) -> np.ndarray:
    """Return comoving R_Lag in internal length units; nonpositive masses map to zero."""

    mass = np.asarray(mass, dtype=np.float64)
    radius = np.zeros_like(mass)
    positive = mass > 0.0
    radius[positive] = np.cbrt(3.0 * mass[positive] / (4.0 * math.pi * density))
    return radius


def derive_catalogue(path: Path) -> tuple[float, dict[str, np.ndarray]]:
    with h5py.File(path, "r") as catalogue:
        if "Parameters" not in catalogue or "Group" not in catalogue:
            raise KeyError("expected /Parameters and /Group in the HDF5 catalogue")

        density = mean_matter_density(catalogue["Parameters"].attrs)
        groups = catalogue["Group"]
        radii: dict[str, np.ndarray] = {}
        for name in MASS_DATASETS:
            if name in groups:
                radii[f"R_Lag_{name}"] = lagrangian_radius(groups[name][...], density)

    return density, radii


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path, help="one fof_subhalo_tab_XXX HDF5 file")
    parser.add_argument("--output", type=Path, help="optional NumPy .npz output")
    args = parser.parse_args()

    density, radii = derive_catalogue(args.catalogue)
    summary = {
        "catalogue": str(args.catalogue),
        "mean_matter_density_internal": density,
        "derived_datasets": {name: int(values.size) for name, values in radii.items()},
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.output:
        np.savez_compressed(args.output, mean_matter_density=density, **radii)


if __name__ == "__main__":
    main()
