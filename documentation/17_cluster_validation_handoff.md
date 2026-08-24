# Cluster validation handoff

This handoff validates that the exact archived LOSS initial conditions can be
read and evolved by the publication candidate on a Linux/HPC system, while
staging the evidence and data products needed for the Zenodo rehearsal. It is
an acceptance run, not authorization to launch the full production simulation
or upload a public data record.

## Pinned software candidate

- repository: `beirving4/AsymptoticGadget4` (currently private);
- branch: `codex/updated-asymptotic-gadget4`;
- tested commit: `8355241e142e264f93abfdb6ea36209bb2e877df`;
- reference FOF linking length: `0.28`.

The pinned commit passed the Python/release checks and the Linux x86-64,
two-rank MPI smoke workflow in
[GitHub Actions run 32735673723](https://github.com/beirving4/AsymptoticGadget4/actions/runs/32735673723).
Use that exact commit for the cluster acceptance run. Later documentation-only
commits do not change the candidate being tested.

The repository does not need to be public for this test. Prefer a private,
single-branch SSH clone. If the cluster cannot authenticate to GitHub, transfer
a Git bundle containing only the candidate branch and still check out the
pinned commit. Do not solve an authentication failure by changing repository
visibility.

## Copy-paste handoff prompt

```text
You are running the Linux/HPC archived-initial-condition acceptance test for
AsymptoticGadget4 and preparing a reviewable Zenodo staging area.

Repository: git@github.com:beirving4/AsymptoticGadget4.git
Branch: codex/updated-asymptotic-gadget4
Required commit: 8355241e142e264f93abfdb6ea36209bb2e877df
FOF_LINKLENGTH: 0.28

Objective:
Prove that the exact archived LOSS initial conditions integrate with the pinned
code by reading the complete IC set, advancing beyond initialization to a small
checkpoint, producing a readable snapshot and FOF/SUBFIND catalogue, and
recording enough evidence to reproduce and package the run for Zenodo.

Non-negotiable constraints:
1. Treat the archived ICs and preserved production inputs as immutable. Never
   edit, rename, truncate, or overwrite them.
2. Do not invoke restartflag 6 and do not regenerate ICs as a substitute. If
   the exact archived ICs cannot be found or identified, stop and report that
   as the blocker.
3. Do not launch the full production evolution. Prepare and submit only the
   short acceptance job unless the user separately authorizes the full run.
4. Do not upload to Zenodo, make the GitHub repository public, change its
   default branch, or create a release/tag.
5. Do not commit credentials, allocation/account names, usernames, private
   filesystem paths, machine-local module settings, build products, ICs, or
   simulation outputs to Git.
6. Work in a new run/staging directory. Never point OutputDir at a source-data
   directory or an existing production run.
7. Make no unexplained scientific changes. The acceptance parameter file may
   change paths, I/O layout, resource limits, output schedule, and stopping
   point, but it must preserve cosmology, units, initial time, force/softening
   choices, and the 0.28 FOF definition. Record a diff from the preserved
   production parameter file.

Workflow:

A. Preflight and storage safety
- Identify the scheduler (for example SLURM or PBS), compute architecture,
  available allocation, filesystem quotas, scratch-retention policy, and
  expected wall-time limits.
- Before copying or running anything, report free space and estimate the space
  needed for ICs, the acceptance snapshot/catalogue, logs, restart safety
  files, and the eventual Zenodo staging products.
- Create separate read-only-input, run-output, evidence, and zenodo-stage
  locations under an approved project/scratch root. Use explicit paths; do not
  delete or clean any pre-existing directory.

B. Acquire and pin the source
- Prefer:
    git clone --single-branch --branch codex/updated-asymptotic-gadget4 \
      git@github.com:beirving4/AsymptoticGadget4.git
    cd AsymptoticGadget4
    git checkout --detach 8355241e142e264f93abfdb6ea36209bb2e877df
    git rev-parse HEAD
- Require the final command to equal the required commit exactly. If private
  authentication is unavailable, stop and request a candidate-branch Git
  bundle; do not request that the repository be made public.
- Verify examples/LOSS/INPUTS.sha256 before building.

C. Inventory the exact archived ICs
- Locate the IC set only within user-approved data locations. Do not infer that
  examples/LOSS/loss_param_sandbox.txt points to it: that historical file uses
  dummy.dat and the N-GenIC generation path.
- Record every IC filename, byte size, SHA-256, format, file-piece count,
  particle counts by type, ID inventory/range, cosmology, units, initial scale
  factor/redshift, and available creation provenance.
- Verify that all file pieces agree. If any checksum, header, particle count,
  or parameter value is missing or inconsistent, stop before simulation.
- Copy or link inputs into the run layout without modifying the source, then
  verify the staged checksums against the source inventory.

D. Record and build the environment
- Capture date/time, hostname class (sanitized for the public evidence),
  uname/architecture, scheduler, compiler and flags, MPI implementation,
  Python, HDF5, GSL, FFTW, zlib, loaded modules, rank/thread layout, and storage
  filesystem. Keep private account and allocation identifiers out of public
  evidence.
- Build the full examples/LOSS configuration. Start with
    make --jobs 4 SYSTYPE=Generic-system-gcc DIR=examples/LOSS PYTHON=python3
  when dependencies are on standard paths. Otherwise create an untracked,
  site-specific build profile and record it in the evidence directory.
- Record the build log, executable SHA-256, and exact Git commit. Do not commit
  the executable or build directory.

E. Create two archived-IC parameter files outside the preserved inputs
- production-ready variant: points to the staged archived ICs and otherwise
  preserves the intended full scientific run;
- acceptance variant: writes to a fresh acceptance OutputDir and stops after a
  small, affordable checkpoint while preserving the scientific initial state.
- Confirm InitCondFile, ICFormat, file counts, TimeBegin, cosmology, units,
  BoxSize, particle/softening settings, output list, and 0.28 FOF definition
  against the IC inventory and production inputs. Save parameter-file hashes
  and a diff. Do not overwrite examples/LOSS/loss_param_sandbox.txt.

F. Run only the short acceptance job
- Prepare a scheduler script with conservative resources and a unique output
  directory. Include a preflight that refuses to run if OutputDir already
  contains data.
- Run the executable normally from the archived ICs; do not pass restartflag 6.
- Capture scheduler ID, start/end timestamps, ranks, threads, peak memory,
  wall time, exit status, stdout/stderr, GADGET logs, and parameters-usedvalues.
- Require the run to read every IC piece, report the expected initial state,
  advance beyond initialization, and write a readable validation checkpoint.

G. Validate integration and catalogue output
- Verify finite particle fields, exact particle counts/types and ID inventory,
  expected cosmology/units, and readable HDF5 metadata at the checkpoint.
- Confirm FOF/SUBFIND output exists and contains Group_M_Turnaround,
  Group_R_Turnaround, Group_M_TurnLambda, and Group_R_TurnLambda, with no stored
  R_Lag datasets. Record counts and numerical summaries.
- If enough snapshots/link files exist, assemble trees with restartflag 8 and
  validate provenance and tree fields. Use tools/validate_loss_tree_fields.py
  only when the fixture contains satellite rows; otherwise use the smoke schema
  validator and state the limitation.
- Require output Git_commit to equal the pinned commit and FOF_LINKLENGTH to
  equal 0.28.

H. Stage, manifest, and verify—do not upload
- Stage immutable copies of the exact ICs, portable parameter/configuration
  inputs, catalogues, trees and desc/prog/treelink files when available, logs,
  environment/build evidence, validation summaries, and README instructions in
  the product groups defined by documentation/13_loss_data_release.md.
- Exclude unnecessary full snapshots and restart files unless the user approves
  them for the data record. Never exclude the exact ICs or validation evidence.
- From the repository root run:
    python3 tools/build_release_manifest.py ZENODO_STAGE \
      --output ZENODO_STAGE/MANIFEST.json
    python3 tools/build_release_manifest.py ZENODO_STAGE \
      --output ZENODO_STAGE/MANIFEST.json --verify
- Re-verify the original IC checksums after the acceptance run. The before and
  after manifests must match.

Stop conditions:
- wrong Git commit or FOF link length;
- exact IC set unavailable or ambiguous;
- inconsistent/missing IC pieces or metadata;
- insufficient storage/quota or unclear scratch retention;
- parameter mismatch in cosmology, units, TimeBegin, BoxSize, or particle
  inventory;
- any command would overwrite existing data;
- build/run failure, non-finite output, provenance mismatch, or manifest
  verification failure.

Final report to the user:
1. PASS/FAIL/BLOCKED for source pinning, IC inventory, build, initialization,
   checkpoint, FOF/SUBFIND schema, optional trees, and manifest verification.
2. Exact commit, executable hash, IC-manifest hash, parameter hashes, platform,
   MPI layout, resource use, output counts, and staging size.
3. Paths to the private evidence and Zenodo staging directories, plus a
   sanitized public evidence summary with no credentials or private paths.
4. Every deviation from preserved inputs and whether it is scientific,
   portability-related, or acceptance-test-only.
5. A clear recommendation on whether the data package is ready for a clean
   download rehearsal. Do not upload or launch production without approval.
```

## Completion criteria

The cluster gate passes only when the pinned executable reads the exact IC set,
advances beyond initialization, writes and reopens a validation checkpoint,
produces the documented catalogue schema at `FOF_LINKLENGTH=0.28`, and leaves a
verified Zenodo staging manifest. A successful build without the archived ICs
is not a pass. IC regeneration is a separate experiment and is not accepted as
evidence for this gate.

Making the repository public is a later release action. Before changing
visibility, audit the historical default branch and all other reachable
branches/tags, preserve the legacy line under approved names, switch the
default branch intentionally, complete citation/DOI metadata, and review the
public landing page from a clean browser session.
