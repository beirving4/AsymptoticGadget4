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
- [x] Observe the new CI workflow passing on the pushed release-candidate
  branch ([run 32736885950](https://github.com/beirving4/AsymptoticGadget4/actions/runs/32736885950)).
- [x] Run a real multi-subhalo fixture and confirm every group-only tree field
  is zero on satellite rows.
- [x] Compare the nine legacy group/SO payload fields exactly between preserved
  historical catalogues and newly assembled trees.
- [x] Rebuild production-scale trees from the flat L512 and 16-piece L128
  layouts and verify `Nhalos_Total == sum(Nsubhalos_Total)` through snapshot 74.
- [x] Establish that the preserved sandbox tree is an orphan that matches
  neither live catalogue sequence and exclude it as a correctness oracle.

## Archived initial conditions and LOSS data

- [x] Stage the five exact LOSS initial-condition sets and record SHA-256, byte
  size, format, file count, particle inventory, and creation provenance.
- [ ] Create a ready-to-run production parameter file for the archived ICs.
- [x] Create a short archived-IC acceptance parameter file without modifying
  the preserved production configuration.
- [ ] From a clean download, initialize and advance the archived ICs to a
  readable validation checkpoint on Apple Silicon macOS.
- [x] Initialize and advance the exact 256-cubed IC on Linux x86-64; reopen the
  checkpoint with finite fields and exact particle-ID equality.
- [ ] Repeat Tier A on one 1024-cubed primary IC set.
- [x] Add a pinned Linux/HPC handoff that protects the original ICs, captures
  platform/resource evidence, and stages a verified Zenodo manifest.
- [x] Execute that handoff on the cluster and verify the original IC checksums
  before and after the acceptance run.
- [x] Validate the first snapshot and FOF/SUBFIND catalogue and record resource
  use, dependency versions, hashes, and numerical summaries.
- [x] Package the fixed catalogue/descendant/progenitor scope into five
  archives and byte-verify all 7,805 files after clean extraction.
- [ ] Copy the five archives and manifest from purgeable scratch to durable
  group storage; an unpublished Zenodo draft is not a backup.
- [ ] Rehearse the 216 MB sandbox archive upload on Zenodo's sandbox service.
- [ ] Upload the five immutable archives and manifest to an unpublished Zenodo
  draft. Do not invoke the irreversible publish action without sign-off.

## Documentation, citation, and release metadata

- [x] Identify the project prominently as an unofficial research fork of
  GADGET-4 developed for thesis work with the LOSS simulations.
- [x] Document macOS/Unix builds, custom output schema, Graphify limitations,
  exact-IC validation, and the fixed halo-catalogue release scope.
- [x] Add the released HDF5 data dictionary with types, units, scale-factor and
  `h` conversions, sentinels, multifile indexing, and link semantics.
- [x] Add draft `CITATION.cff`, authorship, changelog, and contribution files.
- [ ] Author selects the software and data-record licenses.
- [ ] Author confirms name spelling, contributor order, institution, thesis
  title/link, ORCID, preferred citation, and contact route.
- [ ] Author chooses one combined data record or five per-simulation records.
- [ ] Author confirms that seed `181170` intentionally defines the shared
  phase-matched, fixed-amplitude design.
- [ ] Author confirms that all other simulation suites are out of scope for
  this release and records whether they are candidates for later deposits.
- [ ] Define the Tier C science statistic and tolerance before running it.
- [ ] Choose the first public semantic version and add it to `CITATION.cff`.
- [ ] Reserve and add the software and LOSS data DOIs; cross-link both records.
- [x] Validate the DOI-free draft `CITATION.cff` against CFF 1.2.0.
- [ ] Revalidate `CITATION.cff` and any Zenodo-specific metadata after adding
  the approved author and release fields.
- [ ] Regenerate Graphify after the final release commit and update the audit
  with the immutable revision.

## GitHub and immutable release

- [x] Push the cleanup line as the
  `codex/updated-asymptotic-gadget4` release-candidate branch without force.
- [ ] Preserve historical `main` (`7165fdc0d6e34078bbb1836d6ee878c63600405d`)
  under an approved legacy branch and annotated tag.
- [ ] Review the candidate diff and CI evidence before changing the default
  branch; the historical and updated lines have unrelated Git ancestry.
- [x] Confirm there are no secrets, private paths, executables, object files,
  generated graphs, or large simulation outputs in the tag.
- [ ] Audit historical `main`, every other reachable branch/tag, and repository
  history before changing the repository from private to public.
- [ ] Create an annotated release tag, generate release notes/source archive,
  and rehearse a clean download/build/validation before publication.
- [ ] Make the repository public, publish the GitHub release, archive it with
  Zenodo, and verify the DOI resolves to the exact tag.
