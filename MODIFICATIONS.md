# AsymptoticGadget4 modifications

## Provenance

AsymptoticGadget4 is an unofficial research fork of GADGET-4. The publication
line ports the local scientific extensions onto a reviewed official GADGET-4
source base. The earlier source line is preserved as
`legacy/historical-main`; it was not merged into the publication history.

Git history, release tags, and retained source-file notices are the
authoritative detailed provenance records.

## Relationship to standard catalogues

Preserved LOSS catalogues associated with this project were produced by
upstream GADGET-4 and contain the standard FOF/SUBFIND and
spherical-overdensity fields. They are not outputs of AsymptoticGadget4 and do
not contain the custom turnaround fields described below.

AsymptoticGadget4 can read those standard catalogues and rebuild native merger
trees from their descendant/progenitor link files. Custom quantities absent
from an input catalogue cannot be reconstructed during tree assembly. The
catalogue files record their own source, configuration, runtime parameters,
cosmology, and units in HDF5 metadata.

## Scientific extensions

### Turnaround spherical-overdensity definitions

`src/subfind/subfind_so.cc` extends the standard spherical-overdensity loop
with:

1. `Turnaround`: `Delta = (3 pi / 4)^2`, relative to the mean matter density.
   This is exact for Einstein-de Sitter and is used as a constant LCDM
   approximation.
2. `TurnLambda`: `Delta = 2 OmegaLambda a^3 / Omega0`, the force-balance
   threshold for a cosmological constant. It is not a general constant-w
   dark-energy implementation.

Low-density definitions receive a wider initial radial bracket. Failed
high-density crossings can expand the bracket up to six times, with searches
capped at `0.45 * BoxSize`. A group with no valid crossing retains the standard
zero mass/radius sentinel.

### Group catalogue fields

The HDF5 `/Group` table adds:

- `Group_M_Turnaround`
- `Group_R_Turnaround`
- `Group_M_TurnLambda`
- `Group_R_TurnLambda`

No `Group_R_Lag_*` datasets are stored. The HDF5 writer already records the
cosmology and units in `/Parameters`; `examples/LOSS/derive_lagrangian_radii.py`
derives comoving Lagrangian radii without duplicating per-group data.

### Merger-tree payload

The main subhalo (`SubRankInGr == 0`) of every FOF group receives:

- `GroupMass`;
- mass and radius for Mean200, Crit200, Crit500, and TopHat200;
- mass and radius for Turnaround and TurnLambda.

Satellites are explicitly initialized to zero for every group-only field.
Descendant matching, progenitor selection, tree topology, and main-branch
selection remain upstream algorithms. Merger-tree and tree-link HDF5 files
record source provenance in `/Header`.

### Acceleration round-trip

The snapshot `Acceleration` field is read when present. The read conversion
inverts the writer's scale-factor and normalization transform so an `RST_FOF`
read/write post-processing pass preserves the stored field.

## Reference configuration

`examples/LOSS/Config.sh` sets `FOF_LINKLENGTH=0.28`. Users may select another
value, but resulting catalogues represent a different FOF definition and must
be labelled separately. The configuration enables standard GADGET-4 SUBFIND
and merger-tree capabilities alongside the local fields.

The reference configuration omits host-specific diagnostics and communication
tuning. Site-specific performance options belong in local configuration files,
not in the scientific reference configuration.

## Compatibility

- Existing GADGET-compatible HDF5 initial conditions remain accepted.
- Historical group files containing `Group_R_Lag_*` remain usable by external
  analysis tools; the publication line simply does not produce those datasets.
- Standard catalogues without the optional custom fields can be read and used
  for native tree assembly; absent custom tree values retain zero sentinels.
- Snapshot, catalogue, and tree products embed the metadata needed to identify
  the source and run configuration.
- The included tests establish interface compatibility and field-transfer
  behavior, not bitwise equivalence for a complete production simulation.

## Portable build profiles

- `Darwin-Homebrew` selects Apple Clang through the Homebrew MPI wrapper and
  discovers common Homebrew dependencies without embedding a machine-specific
  prefix.
- `Generic-system-gcc` uses `mpicxx` and libraries visible on the compiler's
  normal include and link paths.
- GADGET-4's `OLDSTYLE_SHARED_MEMORY_ALLOCATION` option remains available for
  Unix systems where the default shared-memory backend is unavailable.

These profiles select toolchains and library paths. They do not alter the
scientific configuration, catalogue definitions, or tree semantics.
