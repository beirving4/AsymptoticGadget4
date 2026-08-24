# Build portability and validation

## Scope

AsymptoticGadget4 is source-portable rather than binary-portable. Build a new
executable for every operating system, CPU architecture, compiler, MPI
implementation, and relevant library stack. Do not copy a Mach-O ARM binary
to an Intel Mac or Linux system and expect it to run.

The LOSS extensions use standard C++11, MPI, and the existing GADGET-4 HDF5
I/O abstractions. They add no operating-system branches, CPU intrinsics, or
architecture-specific data layouts. `EXPLICIT_VECTORIZATION` remains optional
and is disabled in both LOSS configurations. That option selects x86 AVX and
is rejected by the Apple Silicon build profile if enabled.

## Required software

- a C++11 compiler and an MPI-3 implementation providing `mpicxx` and
  `mpirun`;
- HDF5, including C headers and libraries;
- GSL;
- single-precision FFTW for the supplied LOSS configurations;
- zlib, GNU Make, and Python;
- Python with `h5py` only for the supplied HDF5 validators and analysis
  helpers, not for simulation runtime.

MPI, HDF5, FFTW, and the compiler must target the same architecture. Mixing
Intel and ARM Homebrew prefixes on macOS is unsupported.

## Supported build profiles

### Apple Silicon or Intel macOS with Homebrew

Install the dependencies and build the smoke configuration from the
repository root:

```sh
brew install open-mpi hdf5 gsl fftw python
make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke
```

`Darwin-Homebrew` resolves the active Homebrew prefix at build time and asks
`xcrun` for the active macOS SDK. The generated executable is native to the
architecture of the selected compiler and libraries. The older upstream
`Darwin` profile remains available for MacPorts installations under
`/opt/local`.

Build the reference LOSS configuration with:

```sh
make -j 8 SYSTYPE=Darwin-Homebrew CONFIG=examples/LOSS/Config.sh BUILD_DIR=build-loss EXEC=AsymptoticGadget4-LOSS
```

The full configuration's `NGENIC=1024` displacement mesh can require far more
memory than the reduced smoke test. For cross-platform validation and release
reproduction, prefer the archived initial-condition file instead of
regenerating it on every platform.

### Linux and other Unix systems with system libraries

When `mpicxx` is available and HDF5, GSL, FFTW, and zlib are visible on the
compiler's default search paths, use:

```sh
make -j 4 SYSTYPE=Generic-system-gcc DIR=examples/LOSS-smoke
```

HPC systems using environment modules or nonstandard library prefixes should
copy an existing `buildsystem/Makefile.path.*` file, define a site-specific
`SYSTYPE` in the top-level Makefile, and record the loaded module versions.
`Generic-gcc` is the upstream profile for libraries staged inside this source
tree; it is distinct from `Generic-system-gcc`.

## Smoke validation

From `examples/LOSS-smoke`, run:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --requirement ../../requirements-validation.txt
mpirun -np 2 ./Gadget4 param.txt
mpirun -np 2 ./Gadget4 param.txt 8 0
python validate_outputs.py output
```

The validator checks the HDF5 metadata groups, the four added turnaround
datasets, the absence of stored Lagrangian-radius fields, and the tree payload.
It reports object counts but deliberately does not treat them as fixed golden
values: this smoke case generates its ICs during the run and small numerical
changes can move marginal eight-particle groups across its deliberately low
threshold. The tiny catalogue contains no satellite tree rows, so
zero-initialization of real satellites still requires a multi-snapshot
regression catalogue.

## Archived LOSS initial-condition validation

The generated-IC smoke test checks the executable and output interfaces. The
publication-critical test uses the exact archived thesis ICs and demonstrates
that a user can initialize this tagged code from them and evolve forward.

The data release must provide checksums plus two ready-to-run parameter files:
the preserved full production configuration and an acceptance-test variant
that changes only the output location/schedule and stopping point needed to
write an affordable early checkpoint. It must not regenerate the ICs.

The acceptance run passes only if the executable reads the complete IC set,
logs the expected format, cosmology, units, starting time, particle counts and
types, preserves the expected ID inventory, advances beyond initialization,
and writes a readable snapshot. FOF/SUBFIND should then produce a readable
catalogue with the documented custom schema. Record the source commit,
parameter-file hash, IC manifest hash, platform and dependency versions, MPI
layout, resource use, and numerical summaries.

This archived-IC test must be run on Apple Silicon macOS and Linux x86-64
before the public release. Group catalogues and merger trees are comparison and
analysis products; they are not required to start ordinary forward evolution.

## Verification matrix

Status as of 2026-08-24:

| Platform | Build | Generated-IC smoke | Archived LOSS IC startup | FOF/SUBFIND | Trees and schema | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Apple Silicon macOS, Apple Clang 17, Open MPI 5.0.7 | pass | pass at 1 and 2 ranks | not yet run | pass | pass | interface verified; archived IC pending |
| Intel macOS | not run | not run | not run | not run | not run | expected, unverified |
| Linux x86-64 | not run on this branch | not run | not run | not run | not run | upstream-supported, fork unverified |
| Linux ARM64 | not run | not run | not run | not run | not run | source-compatible, unverified |
| Other Unix/HPC systems | site profile required | not run | not run | not run | not run | unverified |

The `Darwin-Homebrew` profile compiled both the reduced smoke configuration
and the full reference LOSS configuration. Its documented two-rank smoke run
produced 37 FOF groups and five one-halo trees, and the HDF5 schema validator
passed. An earlier `-O2` build of the same interface test produced 26 groups
and four tree halos. This difference is why generated-IC object counts are
diagnostic rather than the scientific cross-platform oracle. Build success on
one platform is not a claim of scientific equivalence across every platform.

## Automated validation

`.github/workflows/ci.yml` runs the Python helper tests and a Linux x86-64
compile, two-rank simulation, FOF/SUBFIND pass, merger-tree assembly, and HDF5
schema validation on release-line pushes and pull requests. The macOS build job
is manually dispatched so its runner architecture is recorded and private-repo
runner costs remain an explicit release decision.

The CI smoke run generates reduced ICs and therefore cannot replace the
archived LOSS IC acceptance test. That data-dependent test is run during the
release rehearsal and its evidence is deposited with the LOSS data record.

## Numerical comparison policy

Cross-compiler and cross-MPI runs need not be byte-for-byte identical.
Floating-point reduction order, compiler optimization, and MPI decomposition
can produce small roundoff changes that later grow in nonlinear evolution.
`PRESERVE_SHMEM_BINARY_INVARIANCE` stabilizes a specific shared-memory summation
case but does not guarantee identical results across CPU architectures or
toolchains.

For cosmological-background test suites:

1. use the same archived initial conditions, compile-time configuration,
   runtime parameters, output epochs, and FOF linking length;
2. record OS/architecture, compiler flags, MPI rank and thread layout, and
   HDF5/GSL/FFTW versions;
3. compare particle and tree IDs exactly where applicable;
4. compare floating fields with stated absolute and relative tolerances;
5. compare halo counts, tree topology, and final science statistics separately;
6. diagnose disagreements before changing a tolerance.

The reduced smoke test establishes interface portability. It is not a
convergence test and does not reproduce the full LOSS result.
