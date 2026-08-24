# Publication release checklist

This checklist separates completed engineering work from author approvals and
data-dependent validation. A public tag must not be created while a required
item remains unchecked.

## Source and provenance

- [x] Port the LOSS extensions onto a named official GADGET-4 commit.
- [x] Preserve GPLv3, upstream notices, `DEVELOPERS`, and Git provenance.
- [x] Document the closest historical 2023 upstream source state and the
  preserved historical LOSS commit.
- [x] Maintain a file/symbol-level change map in `MODIFICATIONS.md` and the
  extension guide.
- [ ] Author approves the scientific definitions, bracket limits, sentinels,
  FOF linking length, and tree payload.

## Build and automated validation

- [x] Build the smoke and reference LOSS configurations on Apple Silicon.
- [x] Run the generated-IC smoke simulation at one and two MPI ranks.
- [x] Produce FOF/SUBFIND catalogues and assemble merger trees.
- [x] Validate the added HDF5 fields and absence of stored Lagrangian radii.
- [x] Add CI for Python helpers, Linux compilation, MPI smoke execution,
  FOF/SUBFIND, tree assembly, and schema validation.
- [ ] Observe the new CI workflow passing on the pushed release-candidate
  branch.
- [ ] Run a real multi-subhalo fixture and confirm every group-only tree field
  is zero on satellite rows.
- [ ] Compare a small result with preserved historical catalogue/tree output,
  defining exact and floating-point comparison levels in advance.

## Archived initial conditions and LOSS data

- [ ] Stage the exact LOSS initial-condition files and record SHA-256, byte
  size, format, file count, particle inventory, and creation provenance.
- [ ] Create a ready-to-run production parameter file for the archived ICs.
- [ ] Create a short archived-IC acceptance parameter file without modifying
  the preserved production configuration.
- [ ] From a clean download, initialize and advance the archived ICs to a
  readable validation checkpoint on Apple Silicon macOS.
- [ ] Repeat the archived-IC acceptance run on Linux x86-64.
- [ ] Validate the first snapshot and FOF/SUBFIND catalogue and record resource
  use, dependency versions, hashes, and numerical summaries.
- [ ] Package and verify catalogues, trees, descendant/tree-link files,
  manifests, configurations, and representative logs as described in
  `13_loss_data_release.md`.

## Documentation, citation, and release metadata

- [x] Identify the project prominently as an unofficial research fork of
  GADGET-4 developed for thesis work with the LOSS simulations.
- [x] Document macOS/Unix builds, custom output schema, Graphify limitations,
  and the archived-IC reproduction path.
- [x] Add draft `CITATION.cff`, authorship, changelog, and contribution files.
- [ ] Author confirms name spelling, contributor order, institution, thesis
  title/link, ORCID, preferred citation, and contact route.
- [ ] Choose the first public semantic version and add it to `CITATION.cff`.
- [ ] Reserve and add the software and LOSS data DOIs; cross-link both records.
- [x] Validate the DOI-free draft `CITATION.cff` against CFF 1.2.0.
- [ ] Revalidate `CITATION.cff` and any Zenodo-specific metadata after adding
  the approved author and release fields.
- [ ] Regenerate Graphify after the final release commit and update the audit
  with the immutable revision.

## GitHub and immutable release

- [ ] Push the cleanup line as a release-candidate branch without force.
- [ ] Preserve historical `main` (`7165fdc0d6e34078bbb1836d6ee878c63600405d`)
  under an approved legacy branch and annotated tag.
- [ ] Review the candidate diff and CI evidence before changing the default
  branch; the historical and updated lines have unrelated Git ancestry.
- [ ] Confirm there are no secrets, private paths, executables, object files,
  generated graphs, or large simulation outputs in the tag.
- [ ] Create an annotated release tag, generate release notes/source archive,
  and rehearse a clean download/build/validation before publication.
- [ ] Make the repository public, publish the GitHub release, archive it with
  Zenodo, and verify the DOI resolves to the exact tag.
