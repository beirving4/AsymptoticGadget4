# Changelog

Notable AsymptoticGadget4 changes relative to upstream GADGET-4 are recorded
here. The project intends to use semantic version tags for public releases.

## Unreleased

### Added

- `Turnaround` and `TurnLambda` spherical-overdensity mass and radius fields in
  FOF group catalogues.
- Standard and custom FOF properties on main-subhalo merger-tree rows, with
  explicit zero initialization for satellite rows.
- Portable macOS/Homebrew and generic Unix build profiles.
- Reduced MPI, FOF/SUBFIND, and merger-tree smoke validation.
- Catalogue/tree validators, release-manifest tooling, and a Lagrangian-radius
  derivation helper.
- Reproducible Graphify extraction instructions and an audited graph summary.
- Public documentation for the scientific definitions, output schema, build
  portability, and catalogue compatibility.

### Changed

- The scientific extensions were ported onto a reviewed official GADGET-4
  source base rather than publishing a historical source copy as the primary
  line.
- Snapshot input reads `Acceleration` when present and preserves it through an
  `RST_FOF` read/write pass.
- The reference FOF linking length remains `0.28`. Runs using another value,
  including the common `0.2` choice, represent a different halo definition.
- The repository landing page now describes AsymptoticGadget4 directly while
  retaining clear upstream attribution and licensing.
- The reviewed publication lineage is the default `main` branch.

### Removed

- Stored per-group Lagrangian-radius datasets. They are algebraically derived
  from mass and the mean matter density using the supplied helper.

### Validation

- macOS and Linux builds pass the reduced validation workflow.
- MPI simulation, FOF/SUBFIND, tree assembly, schema validation, standard-field
  transfer, and satellite sentinels are covered by automated or reproducible
  tests.
- Updating the upstream base is not claimed to be bitwise neutral over a full
  production simulation.

Formulae, sentinels, data flow, and compatibility details are maintained in
`MODIFICATIONS.md` and the project documentation.
