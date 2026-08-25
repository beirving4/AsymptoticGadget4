# AsymptoticGadget4

[![Release validation](https://github.com/beirving4/AsymptoticGadget4/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/beirving4/AsymptoticGadget4/actions/workflows/ci.yml)

AsymptoticGadget4 is an unofficial scientific fork of GADGET-4. It extends the
FOF/SUBFIND and merger-tree outputs with spherical-overdensity definitions for
turnaround and the cosmological-constant force-balance scale.

The main additions are:

- `Group_M_Turnaround` and `Group_R_Turnaround`;
- `Group_M_TurnLambda` and `Group_R_TurnLambda`;
- transfer of standard and added FOF properties to main-subhalo merger-tree
  rows;
- portable build profiles and automated validation tools.

Lagrangian radii are not stored because they can be derived from halo mass and
the cosmology metadata already present in GADGET HDF5 outputs. The reference
configuration uses `FOF_LINKLENGTH=0.28`; users may select another value, but
that defines a different halo population.

## Build

The code requires a C++11 compiler, MPI-3, HDF5, GSL, FFTW, zlib, GNU Make, and
Python for generated build configuration.

For a reduced validation build on macOS with Homebrew:

```sh
brew install open-mpi hdf5 gsl fftw python
make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke
```

For Linux and other Unix systems, use `SYSTYPE=Generic-system-gcc` when the
required libraries are available on the compiler's standard search path. See
the [build guide](documentation/15_build_portability.md) for additional
options and validation commands.

## Graphify

The repository includes a deterministic Graphify recipe for navigating and
auditing the code structure:

```sh
tools/run_graphify.sh
```

The generated graph is a navigation aid; source review, compilation, and
runtime tests remain authoritative. See the
[Graphify audit](documentation/14_graphify_audit.md) for scope and limitations.

## GADGET-4 and licensing

This project is a modified version of GADGET-4 and is not an official GADGET-4
release. For the original code, manual, and numerical-method description, see
the [official GADGET-4 website](https://wwwmpa.mpa-garching.mpg.de/gadget4/)
and the [GADGET-4 code paper](https://doi.org/10.1093/mnras/stab1855).

AsymptoticGadget4 retains the GNU GPL version 3 and upstream copyright notices.
See [`LICENSE`](LICENSE), [`AUTHORS.md`](AUTHORS.md), and
[`CITATION.cff`](CITATION.cff).
