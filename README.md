# AsymptoticGadget4

AsymptoticGadget4 is an unofficial research fork of GADGET-4 developed by
Bryen Irving for thesis work with the LOSS cosmological simulations. It is a
modified scientific codebase, not an official GADGET-4 distribution and not a
replacement for the upstream project.

The LOSS modifications began from a GADGET-4 source copy made in summer 2023.
For publication, the relevant changes were reviewed and ported onto official
GADGET-4 commit `2046797b578a3be27433a23a9ba912715a829626` so the research
extensions can be distributed with a clear, current upstream base. The change
map is maintained in [`MODIFICATIONS.md`](MODIFICATIONS.md).

## What this fork adds

The primary scientific additions are two FOF-group spherical-overdensity
boundaries:

- `Group_M_Turnaround` and `Group_R_Turnaround`, using
  `Delta = (3 pi / 4)^2` relative to the mean matter density;
- `Group_M_TurnLambda` and `Group_R_TurnLambda`, using the
  cosmological-constant force-balance threshold
  `Delta = 2 OmegaLambda a^3 / Omega0`.

Standard and added FOF properties are copied onto the main subhalo of each
group in merger-tree output. Satellite tree rows use zero sentinels for these
group-only fields. Lagrangian radii are not stored because they can be derived
from halo mass and the cosmology/unit metadata already present in the HDF5
files.

The publication branch also includes:

- preservation of the snapshot `Acceleration` field across an `RST_FOF`
  read/write pass;
- portable macOS/Homebrew and generic Unix/HPC build profiles;
- a reduced MPI, FOF/SUBFIND, and merger-tree validation workflow;
- field-level HDF5 validators, release-manifest tooling, and an audited
  Graphify code graph;
- a documented LOSS configuration with `FOF_LINKLENGTH=0.28`.

Changing the linking length to the upstream default of 0.2 is supported, but
it defines a different halo population and does not reproduce the LOSS
catalogues. Full definitions, sentinels, and data flow are documented in
[`documentation/12_asymptotic_extensions.md`](documentation/12_asymptotic_extensions.md).

## Relationship to the LOSS data release

The coordinated software and data records have different provenance.

The LOSS halo-catalogue record contains standard-SO catalogues produced by
upstream GADGET-4 commit
`1e171a4a679d30ac1e6accabe8a76a037ccbacac`. Those preserved files predate
AsymptoticGadget4 and do not contain Turnaround, TurnLambda, or stored
Lagrangian-radius datasets. The data record contains `fof_subhalo_tab`,
`subhalo_desc`, and `subhalo_prog` products through snapshot 074; users can
analyze them directly or rebuild native GADGET-4 merger trees.

The catalogue record intentionally excludes initial conditions, particle
snapshots, assembled trees, and tree-link outputs. Exact archived LOSS initial
conditions remain preserved validation inputs outside that record. The
AsymptoticGadget4 candidate successfully initialized and advanced the exact
256-cubed LOSS IC on Linux x86-64 with all 16,777,216 particle IDs preserved at
the validation checkpoint.

See the [release plan](documentation/13_loss_data_release.md) and
[catalogue data dictionary](documentation/18_loss_catalogue_data_dictionary.md)
for the exact boundary, schema, units, link semantics, and archive-validation
evidence.

## Build and validate

AsymptoticGadget4 requires a C++11 compiler, MPI-3, HDF5, GSL, FFTW, zlib, GNU
Make, and Python for generated build configuration. The repository provides:

- `Darwin-Homebrew` for native Apple Silicon and Intel macOS builds;
- `Generic-system-gcc` for Unix systems whose dependencies are on the
  compiler's normal search path;
- GADGET-4's `OLDSTYLE_SHARED_MEMORY_ALLOCATION` option for older glibc systems
  where the default `memfd_create` backend is unavailable.

For a reduced validation build on a Homebrew-equipped Mac:

```sh
brew install open-mpi hdf5 gsl fftw python
make -j 4 SYSTYPE=Darwin-Homebrew DIR=examples/LOSS-smoke
```

For the full LOSS reference configuration, select the appropriate build
profile and run from the repository root:

```sh
make -j 8 \
  SYSTYPE=YOUR_SYSTEM_TYPE \
  CONFIG=examples/LOSS/Config.sh \
  BUILD_DIR=build-loss \
  EXEC=AsymptoticGadget4-LOSS
```

The reference inputs and run notes are in [`examples/LOSS`](examples/LOSS).
The complete dependencies, commands, platform matrix, and numerical comparison
policy are in the [build portability guide](documentation/15_build_portability.md).

## Validation status

The publication candidate has passed:

- Apple Silicon compilation and reduced one- and two-rank MPI workflows;
- Linux x86-64 compilation and the complete two-rank CI smoke workflow;
- exact archived 256-cubed LOSS IC initialization on Linux/HPC;
- real-satellite catalogue-to-tree field regression;
- production-scale tree rebuilds from flat and 16-piece catalogue layouts;
- clean extraction and file-by-file hashing of all five fixed-scope catalogue
  archives.

Open release gates—such as macOS exact-IC validation, the 1024-cubed primary
acceptance run, release metadata, and author approvals—are tracked in the
[publication checklist](documentation/16_release_checklist.md). Passing the
reduced smoke test establishes interface compatibility; it is not a claim of
bitwise equivalence with a complete historical production run.

## Documentation and code graph

Project-specific documentation begins at
[`documentation/12_asymptotic_extensions.md`](documentation/12_asymptotic_extensions.md).
The inherited GADGET-4 manual remains under `documentation/01` through `11` as
upstream reference material; it should not be read as documentation of the
local scientific additions.

The deterministic Graphify audit is recorded in
[`documentation/14_graphify_audit.md`](documentation/14_graphify_audit.md) and
can be regenerated with [`tools/run_graphify.sh`](tools/run_graphify.sh).
Generated graph artifacts are intentionally ignored because the reproducible
recipe and audit are the release sources.

## Upstream GADGET-4

GADGET-4 is developed principally by Volker Springel, with major contributions
from Ruediger Pakmor, Oliver Zier, Martin Reinecke, and the other upstream
contributors represented in its history. AsymptoticGadget4 retains upstream
copyright notices, the `DEVELOPERS` file, and Git provenance.

For the unmodified code, official manual, and baseline algorithms, use the
[official GADGET-4 website](https://wwwmpa.mpa-garching.mpg.de/gadget4/) and
cite the [GADGET-4 code paper](https://doi.org/10.1093/mnras/stab1855).

## Citation, license, and contributions

This modified source retains the GNU GPL version 3; see [`LICENSE`](LICENSE).
Scientific work using it should cite both the immutable AsymptoticGadget4
software release and the upstream GADGET-4 paper. Draft machine-readable
metadata is in [`CITATION.cff`](CITATION.cff); release identifiers and author
details that still require approval remain unset.

Project attribution and lineage are summarized in [`AUTHORS.md`](AUTHORS.md).
Contribution and validation expectations are in
[`CONTRIBUTING.md`](CONTRIBUTING.md).
