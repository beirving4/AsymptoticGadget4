# Build portability and validation

AsymptoticGadget4 uses the GADGET-4 build system and adds portable profiles for
common macOS and Unix installations. Build profiles select compilers and
library paths; they do not change the scientific configuration.

## Dependencies

Required components are:

- a C++11 compiler;
- MPI-3;
- HDF5;
- GSL;
- FFTW;
- zlib;
- GNU Make;
- Python for generated build configuration.

Optional features may require additional libraries documented in the upstream
manual.

## macOS with Homebrew

Install the common dependencies:

```sh
brew install open-mpi hdf5 gsl fftw python
```

Build the reduced validation configuration:

```sh
make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke
```

`Darwin-Homebrew` uses the Homebrew MPI compiler wrapper and discovers formula
prefixes without embedding a user-specific installation path.

## Linux and other Unix systems

When MPI, HDF5, GSL, and FFTW are visible on the compiler's normal search path,
use:

```sh
make -j 4 SYSTYPE=Generic-system-gcc DIR=examples/LOSS-smoke
```

Installations using environment modules or nonstandard prefixes can provide
the standard Make variables or add a site-specific build profile. Keep those
machine-local paths outside the repository.

On older Unix systems where the default `memfd_create` shared-memory backend is
unavailable, enable GADGET-4's existing compile-time option:

```text
OLDSTYLE_SHARED_MEMORY_ALLOCATION
```

This backend reserves shared memory according to `MaxMemSize` for each MPI
task. Choose rank counts and memory settings appropriate to the target system.

## Reduced validation workflow

From `examples/LOSS-smoke`, run the generated test problem and tree assembly:

```sh
mpirun -np 2 ./Gadget4 param.txt
mpirun -np 2 ./Gadget4 param.txt 8 0
python3 validate_outputs.py output
```

The validator checks HDF5 metadata, standard and added catalogue fields,
merger-tree fields, satellite sentinels, and finite values. This reduced test
is intended to exercise interfaces and data flow; it is not a substitute for
scientific convergence testing of a production simulation.

## Automated validation

The GitHub Actions workflow builds and runs the reduced test on Linux and
checks the Python helpers, release tooling, checksums, local documentation
links, and citation metadata. The current status is shown on the repository
README badge.

The macOS profile is also available as a manual workflow job. Other Unix and
ARM systems should be treated as unverified until the same build and runtime
checks are completed in those environments.

## Numerical comparison policy

Cross-platform runs should use the same initial conditions, scientific
configuration, runtime parameters, output epochs, MPI layout where practical,
and dependency precision. Compare exact integer topology and identifiers
separately from floating-point fields, using tolerances chosen before the
comparison.

Successful compilation or a reduced smoke test does not establish bitwise
equivalence across compilers, libraries, processor architectures, or a full
production evolution.
