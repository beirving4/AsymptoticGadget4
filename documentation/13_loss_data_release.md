# LOSS halo-catalogue and software release

The publication consists of two coordinated, cross-linked records with
different provenance:

1. a data record for the preserved LOSS FOF/SUBFIND catalogues and merger-link
   inputs produced by upstream GADGET-4;
2. a software record for AsymptoticGadget4, the research fork that adds the
   Turnaround and TurnLambda definitions.

Reserve both DOI fields before publication and add the reciprocal related-
identifier links together. Until then, repository metadata must retain DOI
placeholders rather than inventing identifiers.

## Provenance boundary

| Record | Producing source | Scientific contents |
| --- | --- | --- |
| LOSS halo catalogues | upstream GADGET-4 `1e171a4a679d30ac1e6accabe8a76a037ccbacac` plus each file's embedded `/Config` and `/Parameters` | Standard FOF/SUBFIND fields and Mean200, Crit200, Crit500, and TopHat200 SO definitions |
| AsymptoticGadget4 software | release candidate based on official GADGET-4 `2046797b578a3be27433a23a9ba912715a829626`; validated code pin `8355241e142e264f93abfdb6ea36209bb2e877df` | Source capable of producing the added Turnaround/TurnLambda catalogue and tree fields in new runs |

The released catalogue files predate AsymptoticGadget4. They contain no
Turnaround, TurnLambda, or stored Lagrangian-radius datasets and must never be
described as outputs of the software record. See
`18_loss_catalogue_data_dictionary.md` for the field-level schema.

## Fixed data scope

Five simulation archives contain only:

- `fof_subhalo_tab_000` through `fof_subhalo_tab_074`;
- `subhalo_desc_000` through `subhalo_desc_073`;
- `subhalo_prog_001` through `subhalo_prog_074`.

Snapshot 074 is the uniform cap, with `a=100.0` and `z=-0.99` in all five
simulations. The common epoch list assigns the same time to each snapshot index.

The data record intentionally excludes:

- assembled merger trees, because restart flag 8 rebuilds them exactly from
  the three shipped product families;
- `subhalo_treelink`, because it is an output of that rebuild;
- all particle snapshots and initial-condition files;
- derived analysis products;
- incompatible L32 `bak-*` links;
- snapshots later than 074 in simulations that continued farther.

The `bak-*` exclusion is required for correctness: the backup links and live
catalogue sequence are internally consistent sets but are mutually
incompatible. Archives were therefore built from explicit file lists rather
than by recursively packaging each source directory.

The exact archived ICs remain preserved validation inputs outside this Zenodo
catalogue record. The five IC sets were found and inventoried at 189.7 GB total;
their absence from this record is an explicit scope choice, not a failed search.
Consequently, this data record supports direct halo analysis and exact tree
reassembly, but it is not a complete byte-for-byte initial-condition package
for rerunning all five simulations from the beginning.

## Completed validation

### Exact-IC software acceptance on Linux x86-64

The pinned AsymptoticGadget4 candidate read the exact 256-cubed LOSS IC,
advanced beyond initialization, wrote a checkpoint at `a=0.0105`, and reopened
it successfully. All 16,777,216 type-1 particles and all eight particle
datasets were present, finite, and ID-set exact; the mass table was preserved.
The archived IC SHA-256 remained
`c8966ce8611c78ec9e208a043f97c3cfdb59d81d67d1601e01e1db413855b25b`
before and after the run. No IC-generation path was compiled or invoked.

This discharges the Linux integration gate for the tested IC. A macOS run and
an exact-IC acceptance run on one 1024-cubed primary box remain separate release
checks.

### Production-scale tree rebuild

Restart flag 8 was tested on both storage layouts without particle snapshots:

| Simulation/layout | Rebuilt `Nhalos_Total` | Result |
| --- | ---: | --- |
| L512, flat files | 95,522,988 | exit 0; every catalogue subhalo represented; `LastSnapShotNr=74`; field validation pass |
| L128, 16-piece files | 68,612,094 | exit 0; every catalogue subhalo represented; `LastSnapShotNr=74`; field validation pass |

The release invariant is
`Nhalos_Total == sum(Nsubhalos_Total for snapshots 000–074)`. In a multifile
snapshot, `Nsubhalos_Total` is global and repeated in every piece, so it must be
read once; only `Nsubhalos_ThisFile` is piece-local.

A preserved sandbox `trees.hdf5` was also checked and matches neither catalogue
sequence currently on disk. It is an orphan artifact and is not used as a
correctness oracle.

### Archive integrity

Five gzip-compressed tar archives contain 7,805 files: 100.18 GB uncompressed
and 40.08 GB compressed. Every archive was extracted into a clean location and
all 7,805 files matched the pre-compression SHA-256 inventory, with zero scope
leakage and exactly one top-level simulation directory per archive.

`LOSS_RELEASE_MANIFEST.json` is the machine-readable release inventory. Its
SHA-256 is
`b4d02e6c92e37c95e3a6a587ff6c82c579454f56552c3272bb81446636b7249b`.
It records per-archive sizes/hashes, every released file hash, provenance, scope,
and the tree-rebuild invariant.

## Draft upload and publication gates

The archives may be transferred directly from the cluster to an unpublished
Zenodo draft so the user does not need local disk for a 40 GB round trip. An
unpublished draft is not a durable backup and must not be the only non-scratch
copy. The irreversible Zenodo publish action requires separate explicit
approval.

The author must decide whether the five archives appear in one combined data
record or five per-simulation records. Both layouts use the same immutable
archives and manifest; the choice affects titles, citations, related
identifiers, and upload scripting, not scientific scope.

Before publication, obtain author approval for:

- license for each record;
- creator list, order, affiliations, ORCIDs, preferred citation, and contact;
- combined versus per-simulation data-record layout;
- first public software version;
- the Tier C science statistic and tolerance, defined before running it;
- intended fixed-amplitude/phase-matched use of seed `181170`;
- exclusion of the other simulation suites from this release;
- the macOS acceptance-test venue and result.

## Tree rebuild and software relationship

Users can rebuild native GADGET-4 `trees` and `subhalo_treelink` outputs by
placing the three shipped input families under the configured output hierarchy
and running restart flag 8 through snapshot 74. `full_tree*` is not a native
GADGET-4 basename; it is a post-hoc rename and is not used in this record.

The AsymptoticGadget4 candidate can read these upstream catalogues and transfers
the nine available standard group/SO fields exactly. Because the four custom
catalogue datasets are absent, the corresponding custom tree fields remain
zero. Users who need scientifically measured Turnaround/TurnLambda values must
run AsymptoticGadget4 FOF/SUBFIND from particle data; tree assembly cannot
derive them from the standard catalogues.

## Scientific labelling

Every catalogue self-records `FOF_LINKLENGTH=0.28`, the upstream Git commit,
runtime parameters, cosmology, and units. A rerun with link length 0.2 is a
different halo definition and must not be labelled as reproducing this data
record.
