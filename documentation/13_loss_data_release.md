# LOSS catalogue and software records

The catalogue data and AsymptoticGadget4 software are separate research
objects with different provenance.

## Provenance boundary

The preserved LOSS catalogues were produced by upstream GADGET-4. Each HDF5
catalogue records its source revision, compile-time configuration, runtime
parameters, cosmology, and units in `/Header`, `/Config`, and `/Parameters`.
These files contain standard FOF/SUBFIND properties and the standard Mean200,
Crit200, Crit500, and TopHat200 spherical-overdensity definitions.

AsymptoticGadget4 is the software extension capable of producing the added
Turnaround and TurnLambda catalogue and tree fields in new runs. The preserved
standard catalogues predate those extensions and must not be described as
outputs of this fork.

## Catalogue scope

The catalogue record contains three product families through its documented
final snapshot:

- `fof_subhalo_tab` group and subhalo catalogues;
- `subhalo_desc` descendant links;
- `subhalo_prog` progenitor links.

It intentionally excludes particle snapshots, initial conditions, assembled
merger trees, tree-link outputs, derived analysis products, backup link sets,
and products beyond the common catalogue endpoint.

The exclusion of backup links is scientifically important: backup and active
link sequences may each be internally consistent while remaining incompatible
with one another. Release archives should therefore be created from explicit
file inventories.

## Tree reconstruction

Users can rebuild native GADGET-4 `trees` and `subhalo_treelink` outputs with
restart flag 8 using the three catalogue/link families. Particle snapshots and
particle IDs are not required for this operation.

For a reconstructed tree, the global halo count must equal the sum of the
catalogue `Nsubhalos_Total` values across snapshots. In multifile catalogues,
`Nsubhalos_Total` is a global value repeated in every piece and must be counted
once per snapshot; `Nsubhalos_ThisFile` is piece-local.

When AsymptoticGadget4 reads these standard catalogues, available standard
group fields transfer to tree rows. Optional Turnaround/TurnLambda tree fields
remain zero because the source datasets are absent. A zero in this situation
is a sentinel, not a reconstructed measurement.

## Integrity and citation

The data deposit should include a machine-readable manifest containing the
archive inventory, file sizes, checksums, and scope statement. Integrity
identifiers belong in that deposit and its release metadata rather than in the
software repository landing page.

The software and catalogue records should cite and link one another while
retaining their distinct provenance. Use the field-level
`18_loss_catalogue_data_dictionary.md` when interpreting the released HDF5
products.

Every released catalogue records `FOF_LINKLENGTH=0.28`. A rerun with a
different linking length uses a different halo definition and must be labelled
accordingly.
