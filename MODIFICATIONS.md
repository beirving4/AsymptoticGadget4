# AsymptoticGadget4 modifications

## Provenance

This branch starts from official GADGET-4 commit
`2046797b578a3be27433a23a9ba912715a829626` (2026-08-05). The historical LOSS
source remains on the repository's `main` branch at
`7165fdc0d6e34078bbb1836d6ee878c63600405d`.

The historical source was copied from GADGET-4 in summer 2023. Its closest
identified upstream source state is
`4ff3d310646fec4efb5cac8b91c10b399e339b02` (2023-04-29). The scientific
extensions were ported onto current upstream rather than replacing current
files with the historical copies.

## Scientific extensions

### Turnaround spherical-overdensity definitions

`src/subfind/subfind_so.cc` extends the standard four-definition SO loop with:

1. `Turnaround`: `Delta = (3 pi / 4)^2`, relative to the mean matter density.
   This is exact for Einstein-de Sitter and is used here as a constant LCDM
   approximation.
2. `TurnLambda`: `Delta = 2 OmegaLambda a^3 / Omega0`, the force-balance
   threshold for a cosmological constant. It is not a general constant-w
   dark-energy implementation.

Low-density definitions receive a wider initial radial bracket. Failed
high-density crossings can expand the bracket up to six times, with all
searches capped at `0.45 * BoxSize`. A group with no valid crossing inside the
cap retains the standard zero mass/radius sentinel.

### Group catalogue fields

The HDF5 `/Group` table adds:

- `Group_M_Turnaround`
- `Group_R_Turnaround`
- `Group_M_TurnLambda`
- `Group_R_TurnLambda`

No `Group_R_Lag_*` datasets are stored. The HDF5 writer already records the
cosmology and unit inputs in `/Parameters`; `examples/LOSS/derive_lagrangian_radii.py`
derives comoving Lagrangian radii without duplicating per-group data.

### Merger-tree payload

The main subhalo (`SubRankInGr == 0`) of every FOF group receives:

- `GroupMass`
- mass and radius for Mean200, Crit200, Crit500, and TopHat200
- mass and radius for Turnaround and TurnLambda

Satellites are explicitly initialized to zero for every group-only field.
Descendant matching, progenitor selection, tree topology, and main-branch
selection remain upstream algorithms. Merger-tree and tree-link HDF5 files
record `Git_commit` and `Git_date` in `/Header`, matching the provenance
available in snapshots and group catalogues.

### Acceleration round-trip

The snapshot `Acceleration` field is read when present. The read conversion
inverts the writer's scale-factor and normalization transform, allowing an
`RST_FOF` read/write postprocessing pass to preserve the stored acceleration.

## LOSS reference configuration

`examples/LOSS/Config.sh` sets `FOF_LINKLENGTH=0.28`, matching LOSS. Users may
select 0.2, but resulting catalogues represent a different FOF definition and
must be labelled separately. The configuration also enables `SUBFIND_HBT` and
`MERGERTREE`, both standard GADGET-4 capabilities.

The release `Config.sh` preserves the active scientific options from the
historical source while omitting `NUMBER_OF_MPI_LISTENERS_PER_NODE`,
`HOST_MEMORY_REPORTING`, and `ENABLE_HEALTHTEST`, which select communication or
diagnostic behavior rather than the LOSS model. The historical runtime
parameter file and input power spectrum are retained byte-for-byte. Release
copy checksums are recorded in `examples/LOSS/INPUTS.sha256`.

## Compatibility

- Existing HDF5 initial conditions remain accepted by current upstream I/O.
- Historical group files containing `Group_R_Lag_*` remain usable by external
  analysis tools; the clean port simply does not produce those datasets.
- Current snapshot, catalogue, merger-tree, and tree-link output embeds the
  applicable `/Header`, `/Parameters`, and `/Config` metadata, including the
  source commit and run configuration needed to interpret the products.
- Numerical equivalence with historical full-production runs must be
  established by the planned small end-to-end and preserved-output regression
  tests. Updating the upstream base is not claimed to be bitwise neutral.

## Portable build profiles

- `Darwin-Homebrew` selects Apple Clang through the Homebrew MPI wrapper and
  locates HDF5, GSL, FFTW, and optional hwloc formulae without embedding a
  machine-specific Homebrew prefix.
- `Generic-system-gcc` uses `mpicxx` and libraries visible on the compiler's
  default include and link paths, as is common for Linux packages and HPC
  environment modules.
- Command-line `SYSTYPE=<name>` is normalized by the top-level Makefile, while
  the historical quoted values in `Makefile.systype` remain supported.

These profiles only select a toolchain and library search paths. They do not
change `Config.sh`, runtime parameters, catalogue definitions, or tree
semantics. See `documentation/15_build_portability.md` for tested platforms
and numerical-reproducibility limits.
