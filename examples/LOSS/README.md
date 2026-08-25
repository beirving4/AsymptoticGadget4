# LOSS reference configuration

This directory contains a portable reference configuration and text inputs for
the LOSS setup. `Config.sh` preserves the scientific options while omitting
host-specific diagnostics and communication tuning.

Verify the tracked reference inputs from the repository root with:

```sh
shasum -a 256 -c examples/LOSS/INPUTS.sha256
```

## Build

Choose a `SYSTYPE` appropriate for the local MPI, HDF5, FFTW, and GSL
installation:

```sh
make -j 8 \
  SYSTYPE=YOUR_SYSTEM_TYPE \
  CONFIG=examples/LOSS/Config.sh \
  BUILD_DIR=build-loss \
  EXEC=AsymptoticGadget4-LOSS
```

Use `Darwin-Homebrew` on a Homebrew-equipped Mac or `Generic-system-gcc` when
Unix dependencies are visible on the compiler's standard search path. See the
[build guide](../../documentation/15_build_portability.md) for details.

The reference configuration uses `FOF_LINKLENGTH=0.28`. Changing it produces a
different FOF population, spherical-overdensity catalogue, and merger history.

## Run

The supplied parameter file uses GADGET-4's N-GenIC path. Run from this
directory so its relative input paths resolve correctly:

```sh
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_sandbox.txt 6
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_sandbox.txt
```

Users may instead provide compatible external initial conditions and adjust
`InitCondFile`, `ICFormat`, and the run parameters accordingly.

## Trees

With `MERGERTREE` enabled, descendant files are produced as snapshots are
written. Assemble native tree products through the desired final catalogue
with restart flag 8:

```sh
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS \
  loss_param_sandbox.txt 8 LAST_SNAPSHOT_NUMBER
```

The standard catalogue/link inputs and their indexing rules are described in
the [catalogue data dictionary](../../documentation/18_loss_catalogue_data_dictionary.md).

## Lagrangian radii

Use `derive_lagrangian_radii.py` when needed. These algebraically redundant
fields are not stored by AsymptoticGadget4.
