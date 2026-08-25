# AsymptoticGadget4 modifications

## Provenance

This branch starts from official GADGET-4 commit
`2046797b578a3be27433a23a9ba912715a829626` (2026-08-05). The historical LOSS
source is preserved on the repository's `legacy/historical-main` branch at
`7165fdc0d6e34078bbb1836d6ee878c63600405d`. The reviewed publication lineage
is now the repository's default `main` branch; the two histories were not
merged.

The historical source was copied from GADGET-4 in summer 2023. Its closest
identified upstream source state is
`4ff3d310646fec4efb5cac8b91c10b399e339b02` (2023-04-29). The scientific
extensions were ported onto current upstream rather than replacing current
files with the historical copies.

## Relationship to the LOSS catalogue data record

The LOSS catalogue data record being prepared alongside this software is a
separate provenance object. Its standard FOF/SUBFIND catalogues and
descendant/progenitor link files were produced by upstream GADGET-4 commit
`1e171a4a679d30ac1e6accabe8a76a037ccbacac`, not by AsymptoticGadget4. They do
not contain the custom turnaround fields described below. The fork can read
those standard catalogues and rebuild native `trees` products from their link
files, but absent custom quantities cannot be reconstructed from the archived
catalogue fields alone. See `documentation/18_loss_catalogue_data_dictionary.md`
for the deposited schema and `documentation/13_loss_data_release.md` for the
record boundary.

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
- The exact archived 256-cubed LOSS initial conditions pass the Linux/HPC
  startup acceptance run with all particle IDs and required PartType1 datasets
  preserved at the checkpoint. Production-scale native tree rebuilds also
  pass for both flat and 16-piece standard-catalogue layouts.
- These acceptance tests establish input compatibility and standard-field
  transfer; updating the upstream base is still not claimed to be bitwise
  neutral over a complete cosmological production run.

## Portable build profiles

- `Darwin-Homebrew` selects Apple Clang through the Homebrew MPI wrapper and
  locates HDF5, GSL, FFTW, and optional hwloc formulae without embedding a
  machine-specific Homebrew prefix.
- `Generic-system-gcc` uses `mpicxx` and libraries visible on the compiler's
  default include and link paths, as is common for Linux packages and HPC
  environment modules.
- Linux systems with glibc older than 2.27 can select GADGET-4's existing
  `OLDSTYLE_SHARED_MEMORY_ALLOCATION` option instead of the `memfd_create`
  backend. Its shared-memory reservation follows `MaxMemSize` per MPI rank and
  therefore needs scheduler-aware sizing.
- Command-line `SYSTYPE=<name>` is normalized by the top-level Makefile, while
  the historical quoted values in `Makefile.systype` remain supported.

These profiles only select a toolchain and library search paths. They do not
change `Config.sh`, runtime parameters, catalogue definitions, or tree
semantics. See `documentation/15_build_portability.md` for tested platforms
and numerical-reproducibility limits.
