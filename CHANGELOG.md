# Changelog

All notable AsymptoticGadget4 changes relative to upstream GADGET-4 are
recorded here. This project intends to use semantic version tags for public
software releases.

## Unreleased

### Added

- `Turnaround` and `TurnLambda` spherical-overdensity mass and radius fields in
  FOF group catalogues.
- Standard and custom FOF group properties on the main-subhalo rows of merger
  trees, with explicit zero initialization for satellite rows.
- Portable `Darwin-Homebrew` and `Generic-system-gcc` build profiles.
- A reduced LOSS MPI/FOF/SUBFIND/merger-tree smoke test and HDF5 schema
  validator.
- A reference LOSS configuration, a derived Lagrangian-radius helper, and
  deterministic release-manifest tooling.
- Git commit/date provenance in merger-tree and tree-link HDF5 headers, plus a
  real-satellite tree-field regression validator.
- Reproducible Graphify extraction instructions and an audited graph summary.
- Documentation for scientific definitions, output compatibility, build
  portability, archived-IC validation, and the planned LOSS data release.

### Changed

- Rebased the publication line onto official GADGET-4 commit
  `2046797b578a3be27433a23a9ba912715a829626` rather than copying historical
  source files over a newer tree.
- Snapshot input now reads `Acceleration` when present and inverts the output
  conversion so an `RST_FOF` post-processing pass preserves the stored field.
- The LOSS reference FOF linking length remains `0.28`; users may select other
  values, but resulting products must be labelled as different halo
  definitions.

### Removed

- Stored per-group Lagrangian-radius datasets. These are algebraically derived
  from mass and the mean matter density using the supplied helper.

### Validation status

- Apple Silicon compilation and the generated-IC, two-rank MPI smoke workflow
  pass locally.
- Linux x86-64 compilation and the generated-IC, two-rank MPI smoke workflow
  pass in CI.
- A two-rank assembly of 75 preserved LOSS catalogues passes the real-satellite
  regression: all 13 group-only fields are zero on 258,947 satellite rows and
  all nine legacy group/SO fields match exactly on 1,521,937 central rows.
- Archived LOSS IC startup and comparison with a preserved historical final
  tree remain release gates. See `documentation/16_release_checklist.md`.

Full formulae, sentinels, search limits, data-flow details, and upstream
provenance are maintained in `MODIFICATIONS.md` and
`documentation/12_asymptotic_extensions.md`.
