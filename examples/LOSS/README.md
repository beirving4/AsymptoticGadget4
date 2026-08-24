# LOSS reference experiment

This directory contains a portable reference configuration and the historical
text inputs for the `L=256 Mpc/h`, `256^3`-particle LOSS setup.

`loss_param_sandbox.txt` and the input power spectrum are byte-for-byte copies
from the preserved historical branch. The snapshot-epoch values are unchanged,
with a final newline normalized for the source release. `Config.sh` preserves
the active scientific options while omitting historical host diagnostics and
MPI-listener tuning. From the repository root, verify the release copies with:

```sh
shasum -a 256 -c examples/LOSS/INPUTS.sha256
```

## Build

From the repository root, choose an appropriate `SYSTYPE` for the local MPI,
HDF5, FFTW, and GSL installation, then run:

```sh
make -j 8 CONFIG=examples/LOSS/Config.sh BUILD_DIR=build-loss EXEC=AsymptoticGadget4-LOSS
```

For Homebrew on Apple Silicon or Intel macOS, add
`SYSTYPE=Darwin-Homebrew`. For Unix installations with dependencies on the
compiler's standard search path, add `SYSTYPE=Generic-system-gcc`. See the
[build portability guide](../../documentation/15_build_portability.md) for
prerequisites, verification status, and cross-platform comparison rules.

The reference configuration uses `FOF_LINKLENGTH=0.28`. A user may edit this
to 0.2, but the resulting group membership, SO centres, and merger histories
will not reproduce the LOSS catalogue.

## Primary path: archived initial conditions

The publication data release will contain the exact LOSS initial-condition
files used for the thesis simulations. The release must also provide their
SHA-256 checksums and a parameter-file variant whose `InitCondFile` and
`ICFormat` point to those files. Starting from that archived state, rather than
regenerating it, is the authoritative reproduction path:

```sh
sha256sum -c loss-initial-conditions.sha256
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_archived_ic.txt
```

On macOS, use `shasum -a 256 -c loss-initial-conditions.sha256` for the first
command. The exact filenames will be supplied by the data release. A release
rehearsal must show that the tagged code reads the complete IC set, reports the
expected cosmology, units, starting time, particle counts, and particle types,
and then advances to a readable short validation checkpoint. The validation
parameter file may stop early to make this acceptance test affordable; the
preserved production parameter file remains authoritative for a full forward
evolution.

Group catalogues and merger-tree products are reference outputs, not inputs to
ordinary forward integration. They are included so users can analyze the
thesis products directly and compare a rerun without downloading every full
particle snapshot.

For the Linux/HPC acceptance rehearsal, use the pinned
[cluster validation handoff](../../documentation/17_cluster_validation_handoff.md).
It records the IC inventory, platform, executable provenance, short checkpoint,
catalogue schema, resource use, and Zenodo staging manifest while keeping the
preserved inputs unchanged.

## Optional path: regenerate initial conditions

The historical parameter file uses the built-in N-GenIC path and expects to be
run from this directory so that `snapshot_epochs.txt` and the power-spectrum
table resolve correctly. Restartflag 6 generates initial conditions; a regular
start runs the simulation:

```sh
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_sandbox.txt 6
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_sandbox.txt
```

This path is useful for new experiments and implementation checks, but it is
not the exact data-release reproduction path because IC regeneration can
depend on the MPI layout and numerical-library versions.

## Trees

With on-the-fly `MERGERTREE`, descendant files are produced as snapshots are
written. Final tree assembly through the last catalogue uses restartflag 8:

```sh
mpirun -np NUMBER_OF_RANKS ../../AsymptoticGadget4-LOSS loss_param_sandbox.txt 8 LAST_SNAPSHOT_NUMBER
```

The Zenodo data release should include group catalogues, final trees, and
descendant/tree-link files so tree analysis and final assembly do not require
the full particle snapshot series.

## Lagrangian radii

Use `derive_lagrangian_radii.py`; these algebraically redundant fields are not
stored by the updated code.
