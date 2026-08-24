# LOSS reproducibility data release

The software release and simulation data should be separate, cross-linked
Zenodo records. The software DOI identifies the exact source tag. The data DOI
identifies immutable initial conditions and derived products.

## Primary reproduction claim

The essential release test is not merely that the small generated-IC example
runs. A user must be able to download the exact archived LOSS initial
conditions, verify them, initialize the tagged AsymptoticGadget4 executable
from those files, and simulate forward. The group catalogues, trees, and link
files are reference and analysis products; they are not prerequisites for
ordinary time integration from the ICs.

The data record must therefore include a ready-to-run archived-IC parameter
file in addition to the preserved production parameter file. Its
`InitCondFile`, `ICFormat`, file-count settings, cosmology, units, starting
time, and output schedule must match the deposited ICs without requiring a
user to infer or regenerate missing values.

## Required data products

1. Exact initial-condition file, plus its SHA-256 checksum.
2. `examples/LOSS` inputs: compile configuration, runtime parameters, output
   epochs, power spectrum, and IC-generation seed/settings.
3. Complete `groups_XXX/fof_subhalo_tab_XXX` hierarchy.
4. Final `treedata/trees*` output.
5. `subhalo_desc_*` and `subhalo_prog_*` inputs needed to repeat final tree
   assembly, plus the resulting `subhalo_treelink_*` audit products, without
   the full particle snapshot series.
6. `parameters-usedvalues`, build/compiler/library information, launch layout,
   and representative runtime logs.
7. Machine-readable file inventory with byte sizes and SHA-256 checksums.
8. A small validation product and expected schema/object-count summary.
9. A ready-to-run archived-IC parameter file and a shorter acceptance-test
   variant that writes an early validation checkpoint without changing the
   preserved production configuration.

Full particle snapshots and restart files are optional. They are not required
for the stated reproduction path when users can start from the archived ICs
and the descendant/tree products are supplied.

## Archived-IC acceptance test

Before publishing the data record:

1. verify every IC file against the published SHA-256 manifest after a clean
   download and unpack;
2. build the exact candidate software tag with the released LOSS `Config.sh`;
3. start through the supplied archived-IC parameter file, without invoking
   restartflag 6 or regenerating the ICs;
4. confirm the logged format, file count, cosmology, units, starting time,
   particle counts, particle types, and ID inventory against the manifest;
5. advance beyond initialization to the early validation checkpoint and
   verify that its particle fields are finite and its snapshot is readable;
6. run FOF/SUBFIND at the validation output and verify the documented HDF5
   schema, including the added turnaround fields;
7. record the executable commit, dependency versions, MPI layout, resource
   use, exit status, and output checksums or numerical summaries.

Repeat this acceptance test on Apple Silicon macOS and at least one Linux
x86-64 environment. Passing the generated-IC smoke test alone is insufficient
for the publication claim.

The local thesis-workspace inventory found parameter files configured to
generate their initial conditions at startup (`ICFormat=1`,
`InitCondFile=./dummy.dat`) but did not find the exact archived raw IC files.
That inventory is not evidence that the ICs are unavailable elsewhere; it
means the archived-IC acceptance gate remains open until the deposited files
and their matching parameter file are staged.

The Linux/HPC execution and evidence-staging procedure is provided as a
copy-paste handoff in `17_cluster_validation_handoff.md`. It pins an already
CI-validated source commit, prohibits IC regeneration as substitute evidence,
requires before/after IC checksums, and stops after a small validation
checkpoint. This data-dependent workflow remains manual: the archived ICs and
cluster credentials must never be placed in GitHub Actions.

## Preserved-catalogue tree regression

Before depositing the reference trees, repeat tree assembly from the staged
`fof_subhalo_tab_*`, `subhalo_desc_*`, and `subhalo_prog_*` inputs. Then run:

```sh
python3 tools/validate_loss_tree_fields.py STAGED_OUTPUT/treedata/trees.hdf5 \
  --catalogue-dir STAGED_OUTPUT \
  --expected-commit "$(git rev-parse HEAD)" \
  --expected-fof-link-length 0.28 \
  --output STAGED_OUTPUT/tree-field-validation.json
```

Deposit the JSON summary with the input and output manifests. A passing result
shows exact field transfer and satellite initialization in the newly assembled
trees; it does not replace comparison with a preserved historical final tree,
which is needed to make a separate topology-equivalence claim.

## Packaging

Preserve the GADGET directory hierarchy in a small number of independently
downloadable archives:

- `loss-reproduction-inputs.tar.zst`
- `loss-initial-conditions.tar.zst`
- `loss-group-catalogues.tar.zst`
- `loss-merger-trees-and-links.tar.zst`
- `loss-validation-and-manifest.tar.zst`

Before deposit, build the inventory from the repository root:

```sh
python3 tools/build_release_manifest.py STAGED_DIRECTORY \
  --output STAGED_DIRECTORY/MANIFEST.json
```

After a clean download and unpack rehearsal, verify every file without
rewriting the expected manifest:

```sh
python3 tools/build_release_manifest.py STAGED_DIRECTORY \
  --output STAGED_DIRECTORY/MANIFEST.json --verify
```

At release time, recheck Zenodo's current record/file quota rather than relying
on a hard-coded limit in this repository. If multiple simulation variants do
not comfortably fit one record, use one linked data record per variant.

## Scientific labelling

Every catalogue manifest must record the exact source commit and
`FOF_LINKLENGTH`. The LOSS reference value is 0.28. Products generated with
0.2 are supported but scientifically distinct and must not be placed under the
same version label.
